from datetime import datetime
import json
import math
import os
import random
import string
import requests
from aecb.api.auth import GoogleTokenAuth
from aecb.api.models import (Account, Client, CreditCard, Employee, Insurance,
                             PreapprovalRequest, Promotion, Report)
from aecb.api.permissions import AdminPermission, ClientPermission
from aecb.api.serializers import (ClientSerializer, CreditCardSerializer,
                                  CreditCardSerializerWithDepth,
                                  InsuranceSerializer,
                                  PreapprovalRequestSerializer,
                                  PreapprovalRequestSerializerWithDepth,
                                  PromotionSerializer, ReportSerializer, ReportSerializerWithDepth)
from django.conf import settings
from django.http.response import HttpResponse, JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action, permission_classes
from django.core.mail import EmailMessage
from rest_framework.generics import GenericAPIView
from jinja2 import Environment, FileSystemLoader
import pdfkit


class AuthView(GenericAPIView):
    def get(self, request, format=None):
        try:
            token = request.headers.get("Token", "")
            auth_result = GoogleTokenAuth.authenticate(token)

            if auth_result.account is None:
                if auth_result.email_from_token is None:
                    raise Exception(auth_result.detail)

                domain = auth_result.email_from_token.split("@")[1]
                role = "admin" if domain == settings.ADMIN_DOMAIN else "client"
                model = Employee if role == "admin" else Client
                instance = model.objects.filter(
                    email=auth_result.email_from_token).first()

                if not instance:
                    raise Exception("Unregistered user {email}".format(
                        email=auth_result.email_from_token))

                new_account = Account(role=role, token=token, user=instance)
                new_account.save()

                return JsonResponse({"detail": "Account created for {email}".format(email=auth_result.email_from_token)}, status=status.HTTP_200_OK)

            else:
                if auth_result.account.role == "client":
                    if auth_result.account.user.active == False:
                        raise Exception("{email} is not an active client".format(email=auth_result.account.user_email))

                auth_result.account.token = token
                auth_result.account.save()

                return JsonResponse({"detail": "Auth as {role}".format(role=auth_result.account.role)}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ClientViewSet(viewsets.ModelViewSet):
    lookup_value_regex = "[\w.@]+"
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = []
    permission_classes = [AdminPermission]

    @action(detail=True, permission_classes=[ClientPermission])
    def available_credit_cards(self, request, pk=None):
        client = Client.objects.filter(email=pk).first()
        client_params = {"income": client.income,
                         "has_credit": client.has_credit}
        try:
            response = requests.get("{score_microservice}/score".format(score_microservice=settings.AECB_EXTERNAL_API), params=client_params)
        except Exception as e:
            return JsonResponse({"detail": "Error: external score service is unavailable."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if not response.ok:
            return JsonResponse({"detail": "Error: {endpoint} sent code {status} in response.".format(endpoint=settings.AECB_EXTERNAL_API, status_code=response.status_code)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        data = response.json()
        client_score = data.get("score")
        client_tier = math.floor(client_score / 100)
        credit_cards = CreditCard.objects.filter(
            tier__lte=client_tier).order_by("tier")
        serializer = CreditCardSerializerWithDepth(credit_cards, many=True)

        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)

    @action(detail=True, permission_classes=[ClientPermission])
    def request_credit_card(self, request, pk=None):
        try:
            credit_card_id = request.query_params.get("credit_card", None)
            print(credit_card_id)
            credit_card = CreditCard.objects.filter(id=credit_card_id).first()

            if credit_card is None:
                raise Exception("Invalid credit card")

            active_preapproval = PreapprovalRequest.objects.filter(client=pk, active=True).first()
            if active_preapproval is None:
                serializer = PreapprovalRequestSerializer(
                data={"client": pk, "credit_card": credit_card.id})

                if serializer.is_valid():
                    serializer.save()

                else:
                    raise Exception(serializer.errors)

            else:
                raise Exception(
                    "There is an active preapproval request issued to {email}".format(email=pk))

            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=[ClientPermission])
    def preapproval_requests(self, request, pk=None):
        preapprovals = PreapprovalRequest.objects.filter(
            client=pk).order_by("creation_timestamp")
        serializer = PreapprovalRequestSerializerWithDepth(
            preapprovals, many=True)

        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)

    @action(detail=True, permission_classes=[ClientPermission])
    def cancel_active_preapprovals(self, request, pk=None):
        preapprovals = PreapprovalRequest.objects.filter(
            client=pk, active=True).order_by("creation_timestamp")
        for preapproval in preapprovals:
            preapproval.active = False
            preapproval.save()
        serializer = PreapprovalRequestSerializer(preapprovals, many=True)

        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class InsuranceViewSet(viewsets.ModelViewSet):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer


class CreditCardViewSet(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CreditCardSerializerWithDepth
        return CreditCardSerializer


class PreapprovalRequestViewSet(viewsets.ModelViewSet):
    queryset = PreapprovalRequest.objects.all()
    authentication_classes = []
    permission_classes = [AdminPermission]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PreapprovalRequestSerializerWithDepth
        return PreapprovalRequestSerializer

    @action(detail=False)
    def generate_report(self, request):
        email = request.headers.get("Admin-Email")

        if email is None:
            return JsonResponse({"detail": "Missing Admin-Email header"}, status=status.HTTP_400_BAD_REQUEST)

        preapproval_stats = self.generate_stats()
        active_ratio = (preapproval_stats.get(
            "total_active_cards") / self.queryset.count()) * 100
        approval_ratio = (preapproval_stats.get(
            "total_approved_cards") / self.queryset.count()) * 100
        card_approval = preapproval_stats.get("card_approval")
        card_request = preapproval_stats.get("card_request")

        report = {
            "requests": preapproval_stats.get("preapprovals"),
            "clients": preapproval_stats.get("clients"),
            "employees": preapproval_stats.get("employees"),
            "active_ratio": active_ratio,
            "approval_ratio": approval_ratio,
            "most_approved": card_approval[0][0],
            "most_requested": card_request[0][0],
            "generated_by": email,
        }
        serializer = ReportSerializer(data=report)

        if serializer.is_valid():
            serializer.save()
            filename = self.generate_pdf(serializer.data["id"])

            if filename is None:
                return JsonResponse({"detail": "PDF report not generated"}, status=status.HTTP_400_BAD_REQUEST)

            return JsonResponse({"report": "{media}reports/{filename}".format(media=settings.MEDIA_URL, filename=filename)}, status=status.HTTP_200_OK)

        return JsonResponse({"detail": "PDF report not generated"}, status=status.HTTP_400_BAD_REQUEST)

    def generate_stats(self):
        preapprovals = set()
        clients = set()
        emplooyes = set()
        card_request = dict()
        card_approval = dict()
        total_active_cards = 0
        total_approved_cards = 0

        for preapproval in self.queryset:
            preapprovals.add(preapproval.id)
            clients.add(preapproval.client.email)

            if preapproval.reviewed_by is not None:
                emplooyes.add(preapproval.reviewed_by.email)

            if card_request.get(preapproval.credit_card.name) is None:
                card_request[preapproval.credit_card.name] = 0
            card_request[preapproval.credit_card.name] += 1

            if card_approval.get(preapproval.credit_card.name) is None:
                card_approval[preapproval.credit_card.name] = 0

            if preapproval.approved:
                card_approval[preapproval.credit_card.name] += 1
                total_approved_cards += 1

            if preapproval.active:
                total_active_cards += 1

        return {
            "preapprovals": preapprovals,
            "clients": clients,
            "employees": emplooyes,
            "card_request": sorted(card_request.items(), key=lambda x: x[1], reverse=True),
            "card_approval": sorted(card_approval.items(), key=lambda x: x[1], reverse=True),
            "total_active_cards": total_active_cards,
            "total_approved_cards": total_approved_cards
        }

    def generate_pdf(self, report_pk):
        report_instance = Report.objects.filter(id=report_pk).first()
        serializer = ReportSerializerWithDepth(report_instance)

        env = Environment(loader=FileSystemLoader(
            os.path.join(settings.BASE_DIR, "aecb", "templates")))
        template = env.get_template("report.html")
        html_string = template.render(report=serializer.data)


        filename = "{pk}_report_{random}.pdf".format(pk=report_pk, random="".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)))
        file = os.path.join(settings.MEDIA_ROOT, "reports", filename)
        report_created = pdfkit.from_string(html_string, file)

        serializer.instance.file = "reports/{filename}".format(filename=filename)
        serializer.instance.save()

        if report_created:
            self.send_report(report_instance.generated_by.email, report_instance.generated_by.name, file)
            return filename

        return None

    def send_report(self, employee_email, employee_name, pdf_report):
        try:
            email = EmailMessage(
                "AECB Report {datetime}".format(datetime=datetime.now().strftime("%c")), 
                "Hi {name}, you have generated a report successfully.".format(name=employee_name),
                settings.EMAIL_HOST_USER,
                [employee_email]
            )
            email.attach_file(pdf_report)
            email.send()
        except Exception as e:
            print(str(e))

from flask import Flask, request
from flask_cors import CORS, cross_origin

import settings
from endpoints import clients, credit_cards, benefits, token_auth

server = Flask(__name__)
server.config.from_object(settings)
CORS(server, support_credentials=True)


@server.route("/api/clients", methods=["GET", "POST"])
def clients_route():
    if request.method == "GET":
        response = clients.fetch_clients(request)
    elif request.method == "POST":
        response = clients.insert_client(request)

    return response


@server.route("/api/clients/<curp>", methods=["GET", "PATCH", "DELETE"])
def client_route(curp: str):
    if request.method == "GET":
        response = clients.fetch_client(curp, request)
    elif request.method == "PATCH":
        response = clients.update_client(curp, request)
    elif request.method == "DELETE":
        response = clients.delete_client(curp, request)

    return response


@server.route("/api/cards", methods=["GET", "POST"])
def credit_cards_route():
    if request.method == "GET":
        response = credit_cards.fetch_credit_cards(request)
    elif request.method == "POST":
        response = credit_cards.insert_credit_card(request)

    return response


@server.route("/api/cards/<id>", methods=["GET", "PATCH", "DELETE"])
def credit_card_route(id: str):
    if request.method == "GET":
        response = credit_cards.fetch_credit_card(id, request)
    elif request.method == "PATCH":
        response = credit_cards.update_credit_card(id, request)
    elif request.method == "DELETE":
        response = credit_cards.delete_credit_card(id, request)

    return response


@server.route("/api/benefits", methods=["GET", "POST"])
def benefits_route():
    if request.method == "GET":
        response = benefits.fetch_benefits()
    elif request.method == "POST":
        response = benefits.insert_benefit(request)

    return response


@server.route("/api/benefits/<id>", methods=["GET", "PATCH", "DELETE"])
def benefit_route(id: str):
    if request.method == "GET":
        response = benefits.fetch_benefit(id)
    elif request.method == "PATCH":
        response = benefits.update_benefit(id, request)
    elif request.method == "DELETE":
        response = benefits.delete_benefit(id)

    return response


@server.route("/api/preapprovals", methods=["GET", "POST"])
def preapproval_requests_route():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass

    return 0


@server.route("/api/auth", methods=["GET"])
def auth_token():
    if request.method == "GET":
        response = token_auth.verify_token(request)
    
    return response


if __name__ == "__main__":
    server.run(host=settings.HOST, port=settings.PORT)

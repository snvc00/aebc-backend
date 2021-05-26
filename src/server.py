from flask import Flask, request
from flask_cors import CORS, cross_origin

import settings
from endpoints import clients, credit_cards

server = Flask(__name__)
server.config.from_object(settings)
CORS(server, support_credentials=True)


@server.route("/api/clients", methods=["GET", "POST"])
def clients_route():
    if request.method == "GET":
        response = clients.fetch_clients()
    elif request.method == "POST":
        response = clients.insert_client(request)

    return response


@server.route("/api/clients/<curp>", methods=["GET", "PATCH", "DELETE"])
def client_route(curp: str):
    if request.method == "GET":
        response = clients.fetch_client(curp)
    elif request.method == "PATCH":
        response = clients.update_client(curp, request)
    elif request.method == "DELETE":
        response = clients.delete_client(curp)

    return response


@server.route("/api/cards", methods=["GET", "POST"])
def credit_cards_route():
    if request.method == "GET":
        response = credit_cards.fetch_credit_cards()
    elif request.method == "POST":
        print(type(request))
        response = credit_cards.insert_credit_card(request)

    return response


@server.route("/api/cards/<id>", methods=["GET", "PATCH", "DELETE"])
def credit_card_route(id: str):
    if request.method == "GET":
        response = credit_cards.fetch_credit_card(id)
    elif request.method == "PATCH":
        response = credit_cards.update_credit_card(id, request)
    elif request.method == "DELETE":
        response = credit_cards.delete_credit_card(id)

    return response


@server.route("/api/benefits", methods=["GET"])
def benefits_route():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass

    return 0


@server.route("/api/preapprovals", methods=["GET", "POST"])
def preapproval_requests_route():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass

    return 0


if __name__ == "__main__":
    server.run(host=settings.HOST, port=settings.PORT)

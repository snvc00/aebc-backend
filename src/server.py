from flask import Flask, request
from flask_cors import CORS, cross_origin
from endpoints.clients import delete_client, fetch_clients, insert_client, fetch_client, update_client
import settings

server = Flask(__name__)
server.config.from_object(settings)
CORS(server, support_credentials=True)


@server.route("/api/clients", methods=["GET", "POST"])
def clients_route():
    if request.method == "GET":
        response = fetch_clients()
    elif request.method == "POST":
        response = insert_client(request)

    return response


@server.route("/api/clients/<curp>", methods=["GET", "PATCH", "DELETE"])
def client_route(curp: str):
    if request.method == "GET":
        response = fetch_client(curp)
    elif request.method == "PATCH":
        response = update_client(curp, request)
    elif request.method == "DELETE":
        response = delete_client(curp)

    return response


@server.route("/api/cards", methods=["GET", "POST"])
def credit_cards_route():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass

    return 0


@server.route("/api/cards/<id>", methods=["GET", "PATCH", "DELETE"])
def credit_card_route(id: str):
    if request.method == "GET":
        pass
    elif request.method == "PATCH":
        pass
    elif request.method == "DELETE":
        pass

    return 0


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

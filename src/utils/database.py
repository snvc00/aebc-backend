import settings
from models.client import Client
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session

from utils.exceptions import ApiException


class ClientDB():
    """
    """

    def fetch_all() -> list[dict]:
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        clients = []

        for client_instance in session.query(Client):
            client = client_instance.__dict__
            client.pop("_sa_instance_state", None)
            clients.append(client)

        return clients

    def fetch_by_curp(curp: str) -> dict:
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        client_instance = session.query(Client).filter_by(curp=curp).first()

        if client_instance is None:
            raise ApiException("Client not found", 404)

        client = client_instance.__dict__
        client.pop("_sa_instance_state", None)

        return client

    def insert(new_client: dict) -> None:
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        new_client = Client(data=new_client)

        session.add(new_client)
        session.commit()

    def update_by_curp(curp: str, new_values: dict) -> None:
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        affected_rows = session.query(Client).filter_by(
            curp=curp).update(new_values, synchronize_session="fetch")

        if affected_rows == 0:
            raise ApiException("Client not found", 404)

        session.commit()

    def delete_by_curp(curp: str):
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        affected_rows = session.query(Client).filter_by(
            curp=curp).delete(synchronize_session="fetch")

        if affected_rows == 0:
            raise ApiException("Client not found", 404)

        session.commit()

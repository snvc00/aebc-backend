from models.benefit import Benefit
import settings
from models.client import Client
from models.credit_card import CreditCard
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session

from utils.exceptions import ApiException


class ClientTable():
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

    def delete_by_curp(curp: str) -> None:
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        affected_rows = session.query(Client).filter_by(
            curp=curp).delete(synchronize_session="fetch")

        if affected_rows == 0:
            raise ApiException("Client not found", 404)

        session.commit()


class CreditCardTable():
    """
    """

    def fetch_all() -> list[dict]:
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        credit_cards = []

        for credit_card_instance in session.query(CreditCard):
            credit_card = credit_card_instance.__dict__
            credit_card.pop("_sa_instance_state", None)
            credit_cards.append(credit_card)

        return credit_cards

    def fetch_by_id(id: str) -> dict:
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        credit_card_instance = session.query(CreditCard).filter_by(id=id).first()

        if credit_card_instance is None:
            raise ApiException("Credit card not found", 404)

        credit_card = credit_card_instance.__dict__
        credit_card.pop("_sa_instance_state", None)

        return credit_card

    def insert(new_credit_card: dict) -> None:
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        new_credit_card = CreditCard(data=new_credit_card)

        session.add(new_credit_card)
        session.commit()

    def update_by_id(id: str, new_values: dict) -> None:
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        affected_rows = session.query(CreditCard).filter_by(
            id=id).update(new_values, synchronize_session="fetch")

        if affected_rows == 0:
            raise ApiException("Credit card not found", 404)

        session.commit()

    def delete_by_id(id: str) -> None:
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        affected_rows = session.query(CreditCard).filter_by(
            id=id).delete(synchronize_session="fetch")

        if affected_rows == 0:
            raise ApiException("Credit card not found", 404)

        session.commit()

class BenefitTable():
    """
    """

    def fetch_all() -> list[dict]:
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        benefits = []

        for benefit_instance in session.query(Benefit):
            benefit = benefit_instance.__dict__
            print(benefit)
            benefit.pop("_sa_instance_state", None)
            benefits.append(benefit)

        return benefits
    
    def fetch_by_id(id: str) -> dict:
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        benefit_instance = session.query(Benefit).filter_by(id=id).first()

        if benefit_instance is None:
            raise ApiException("Benefit not found", 404)

        benefit = benefit_instance.__dict__
        benefit.pop("_sa_instance_state", None)

        return benefit

    def insert(new_benefit: dict) -> None:
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        new_benefit = Benefit(data=new_benefit)

        session.add(new_benefit)
        session.commit()

    def update_by_id(id: str, new_values: dict) -> None:
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        affected_rows = session.query(Benefit).filter_by(
            id=id).update(new_values, synchronize_session="fetch")

        if affected_rows == 0:
            raise ApiException("Benefit not found", 404)

        session.commit()

    def delete_by_id(id: str) -> None:
        engine = create_engine(settings.DB_URL)
        session = Session(engine, future=True)
        affected_rows = session.query(Benefit).filter_by(
            id=id).delete(synchronize_session="fetch")

        if affected_rows == 0:
            raise ApiException("Benefit not found", 404)

        session.commit()

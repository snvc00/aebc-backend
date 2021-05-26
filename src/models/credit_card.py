from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class CreditCard(Base):
    """
    """
    __tablename__ = "credit_card"

    id = Column(Integer, primary_key=True)
    min_credit = Column(Integer)
    max_credit = Column(Integer)
    name = Column(String)
    tier = Column(Integer)
    image = Column(String)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

        if kwargs.keys().__contains__("data"):
            self.__dict__.update(kwargs.get("data"))

    def __repr__(self) -> str:
        return "id: {}, name: {}".format(self.id, self.name)

from sqlalchemy import Boolean, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Client(Base):
    """
    """
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rfc = Column(String)
    birthdate = Column(Date)
    password = Column(String)
    monthly_income = Column(Integer)
    has_credit = Column(Boolean)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    neighborhood = Column(String)
    is_active = Column(Boolean)
    curp = Column(String)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

        if kwargs.keys().__contains__("data"):
            self.__dict__.update(kwargs.get("data"))

    def __repr__(self) -> str:
        return "id: {}, curp: {}".format(self.id, self.curp)

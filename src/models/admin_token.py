from sqlalchemy import Boolean, Column, String, Date, Integer
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class AdminToken(Base):
    """
    """
    __tablename__ = "admin_token"

    id = Column(Integer, primary_key=True)
    token = Column(String)
    creation_date = Column(Date)
    is_active = Column(Boolean)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

        if kwargs.keys().__contains__("data"):
            self.__dict__.update(kwargs.get("data"))

    def __repr__(self) -> str:
        return "id: {}, token: {}".format(self.id, self.token)

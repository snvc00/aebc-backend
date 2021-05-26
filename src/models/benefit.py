from sqlalchemy import Column, Integer, String, TIMESTAMP, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Benefit(Base):
    """
    """
    __tablename__ = "benefit"

    id = Column(Integer, primary_key=True)
    description = Column(String)
    valid_until = Column(DateTime)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

        if kwargs.keys().__contains__("data"):
            self.__dict__.update(kwargs.get("data"))

    def __repr__(self) -> str:
        return "id: {}, valid_until: {}".format(self.id, self.valid_until)

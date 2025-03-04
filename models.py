from sqlalchemy import Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import DateTime
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Data(Base):

    __tablename__ = 'data'
    id: Mapped[int] = mapped_column(primary_key=True)
    pre_shunt: Mapped[float] = mapped_column(Float(2))
    post_shunt: Mapped[float] = mapped_column(Float(2))
    current: Mapped[float] = mapped_column(Float(2))
    timestamp: Mapped[datetime] = mapped_column(DateTime())

    def __repr__(self):
        return f"Voltage Record: {self.pre_shunt}"

# class MeasurementSpecs(Base):
#     __tablename__ = 'measurement_specs'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     boat_max_v = Mapped[float] = mapped_column(Float(2))
#     boat_min_v = Mapped[float] = mapped_column(Float(2))


from sqlalchemy import Float, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, foreign, relationship
from sqlalchemy.orm import Mapped
from typing import List
from sqlalchemy.schema import Index 
from sqlalchemy import DateTime
from datetime import datetime

class Base(DeclarativeBase):
    pass

# Table of key measurements:
class Measurements(Base):
    __tablename__ = 'measurements'
    measurement_id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    run_id: Mapped[int] = mapped_column(Integer(), ForeignKey('runs.id'), index=True, nullable=False)
    pre_shunt: Mapped[float] = mapped_column(Float(2))
    post_shunt: Mapped[float] = mapped_column(Float(2))
    current: Mapped[float] = mapped_column(Float(2))
    run: Mapped["Runs"] = relationship(back_populates="measurements")
    timestamp: Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    # __table_args__ = (Index('measurement_run_id', 'run.id'))

    def __repr__(self):
        return f"""timestamp: {self.timestamp}
pre_shunt: {self.pre_shunt}
post_shunt: {self.post_shunt}
current: {self.current}"""

# Table that holds any constants or other information about the run
class Runs(Base):
    __tablename__ = 'runs'
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    boat_max_v: Mapped[float] = mapped_column(Float(2))
    boat_min_v: Mapped[float] = mapped_column(Float(2))
    # This relationship with measurments should cascade delete all measurments
    # with an associated run_id
    measurements: Mapped[List["Measurements"]] = relationship(back_populates="run", cascade="all, delete")


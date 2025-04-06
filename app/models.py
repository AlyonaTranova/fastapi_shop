from sqlalchemy import Column, Integer, String, Float, Table, MetaData, ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
import enum
import datetime
from typing import Annotated


intpk = Annotated[int, mapped_column(primary_key=True)]


class WorkersOrm(Base):
    __tablename__ = "workers" 

    id: Mapped[intpk]
    username: Mapped[str]

class Workload(enum.Enum):
     parttime = "parttime"
     fulltime = "fulltaime"


class ResumeOrm(Base):
    __tablename__ = "resume"

    id: Mapped[intpk]
    title: Mapped[str]
    compensation: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow())



metadata_obj = MetaData()
from sqlalchemy import text, insert, select
from database import sync_engine, session_factory, Base
from models import WorkersOrm

class SyncOrm:
    @staticmethod
    def create_tables():
        sync_engine.echo=False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine) 
        sync_engine.echo=True


    @staticmethod
    def insert_workers():
        with session_factory() as session:
            worker_dan = WorkersOrm(username="Dan")
            worker_karl = WorkersOrm(username="Karl")
            session.add_all([worker_dan, worker_karl])
            session.commit()


    @staticmethod
    def select_workers():
        with session_factory() as session:
            worker_id = 1
            worker_dan = session.get(WorkersOrm, worker_id)
            query = select(WorkersOrm)
            result = session.execute(query)
            workers = result.scalars().all()
            print(f"{workers=}")

    @staticmethod
    def update_workers(worker_id: int = 2, new_username: str = "Kirill"):
        with session_factory() as session:
            worker_karl = session.get(WorkersOrm, worker_id)
            worker_karl.username = new_username
            session.commit()
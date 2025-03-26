from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
from datetime import datetime
from models import Measurements, Runs

class Database():

    id: int
    
    def __init__(self):
        
        self.engine = create_engine("sqlite:///db/test.db", echo=True, pool_pre_ping=True)
        inspect_obj = inspect(self.engine)
        
        # create tables if they don't exist yet
        if not inspect_obj.has_table(Measurements.__tablename__):
            Measurements.metadata.create_all(bind=self.engine)
        
        if not inspect_obj.has_table(Runs.__tablename__):
            Runs.metadata.create_all(bind=self.engine)

        # makes sure that the table reflects the schema for now
        # may want to delete this later
        # Measurements.metadata.reflect(self.engine, Measurements)
        # Runs.metadata.reflect(self.engine, Runs)

        # creates a new run on launch
        run = self.create_run()
        if run != None:
            self.id = run.id
        else:
            raise Exception('Unable to create new run in database')
        print(run)

    # decorator for interacting with database
    def use_session(func):
        def wrap(self, *args, **kwargs):
            # expire_on_commit set to True for now to grab some info from the created
            # row in Runs
            # otherwise the objects added and returned from queries will expire
            # and can no longer be access
            with Session(self.engine, expire_on_commit=False) as session:
                return func(self, session, *args, **kwargs)
        return wrap

    @use_session
    def create_run(self, session: Session):
        try:
            run = Runs( # inserts test data for now
                boat_max_v=38,
                boat_min_v=34
            )
            session.add(run)
            session.commit()
            return run
        except Exception as e:
            print(e)
            session.rollback()
    
    @use_session
    def add_voltage(self, session: Session, pre_shunt, post_shunt, current=-1):
        current_time = datetime.now()
        try:
            measurement = Measurements(
                pre_shunt=pre_shunt,
                post_shunt=post_shunt,
                current=current,
                timestamp=current_time,
                run_id=self.id
            )
            session.add(measurement)
            session.commit()
            return measurement
        except Exception as e:
            print(e)
            session.rollback()

# tests if db works
if __name__ == '__main__':
    db = Database()
    db.add_voltage(pre_shunt=1, post_shunt=1, current=-1)

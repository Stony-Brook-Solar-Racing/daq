from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
from datetime import datetime
from models import Data

class Database():
    
    def __init__(self):
        
        self.engine = create_engine("sqlite:///db/test.db", echo=True, pool_pre_ping=True)
        
        # if table does not exist
        if not inspect(self.engine).has_table(Data.__tablename__):
            Data.metadata.create_all(bind=self.engine)

    # decorator for interacting with database
    def use_session(func):
        def wrap(self, *args, **kwargs):
            with Session(self.engine) as session:
                func(self, session, *args, **kwargs)
        return wrap
    
    @use_session
    def add_voltage(self, session: Session, pre_shunt, post_shunt):
        session.begin()
        current_time = datetime.now()
        try:
            session.add(Data(
                pre_shunt=pre_shunt,
                post_shunt=post_shunt,
                current=-1,
                timestamp=current_time
            ))
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()

# tests if db works
# if __name__ == '__main__':
#     db = Database()
#     db.add_voltage(pre_shunt=1, post_shunt=1)

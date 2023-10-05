from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



class database():
    def __init__(self,config:dict):
        url  = f"postgresql+psycopg2://{config['DATABASE']['DB_USER']}:{config['DATABASE']['DB_PASS']}@{config['DATABASE']['DB_HOST']}/{config['DATABASE']['DB']}"
        try:
            self.engine = create_engine(url)
            self.SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=self.engine)  # noqa: E501
        except:
            raise
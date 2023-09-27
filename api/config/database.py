from sqlalchemy import create_engine
from pprint import pprint
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base



class database():
    def __init__(self,config:dict):
        url  = f"postgresql+psycopg2://{config['DATABASE']['DB_USER']}:{config['DATABASE']['DB_PASS']}@{config['DATABASE']['DB_HOST']}/{config['DATABASE']['DB']}"
        print(url)
        try:
            self.engine = create_engine(url)
            self.SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=self.engine)
        except:
            raise

    def POSTGRES(self):
        
        return create_engine(url)

if __name__ == "__main__":
    config = {
    "BLOGINDEX": {
            "DB": "blogindex",
            "DB_HOST": "db",
            "DB_USER": "blogindex",
            "DB_PASS": "In5ecuRe-P@5S",
            "DB_URL": "postgresql+psycopg2://<<DB_USER>>:<<DB_PASS>>@db/<<DB>>",
        }
    }
    db_setup = database(config)
    print(db_setup.Base)
    print(db_setup.SessionLocal)
    print(db_setup.engine)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings as st

#url = postgresql://<username>:<password>@<ip-address/hostname>/<database_name>
SQLALCHEMY_DATABASE_URL = f'postgresql://{st.database_username}:{st.database_password}@{st.database_hostname}:{st.database_port}/{st.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Dependancy:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
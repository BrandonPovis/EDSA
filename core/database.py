from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'postgresql://postgres:edsa123456@localhost:5432/prueba' #es uan mala pracica que se va a cambiar

engine = create_engine(URL_DATABASE)

SessionLocal= sessionmaker(autocommit = False, autoflush=False, bind = engine )

Base = declarative_base()
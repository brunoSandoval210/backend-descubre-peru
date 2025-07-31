from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from decouple import config

DB_HOST=config('DB_HOST')
DB_USER=config('DB_USER')
DB_PASS=config('DB_PASS')
DB_PORT=config('DB_PORT')
DB_DATABASE=config('DB_DATABASE')

DATABASE_URL=f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()
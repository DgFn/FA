from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.setting import settings

engine = create_engine(
    settings.DATABASE_URI,
    echo=True
)


Session = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)
from sqlalchemy import select, exists

from app.modules.reader.models import Reader
from app.utils.repository import SQLAlchemyRepository


class ReaderRepository(SQLAlchemyRepository):
    model = Reader

    def __init__(self, session):
        self.session = session

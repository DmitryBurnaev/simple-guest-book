from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from src.database import Base


class GuestRecord(Base):
    __tablename__ = 'guest_records'

    id = Column(Integer, primary_key=True)
    author_name = Column(String(50), nullable=False)
    created_at = Column(DateTime(), default=datetime.now())
    message = Column(Text(), nullable=True)

    def __init__(self, author_name, message):
        self.author_name = author_name
        self.message = message

    def __repr__(self):
        return '<GuestRecord from {}>'.format(self.author_name)

    def to_dict(self):
        return {
            'id': self.id,
            'author_name': self.author_name,
            'created_at': self.created_at.strftime('%d.%m.%Y %H:%M'),
            'message': self.message
        }


print('Models were read')
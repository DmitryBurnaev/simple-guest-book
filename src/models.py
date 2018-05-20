from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base


class GuestRecord(Base):
    __tablename__ = 'guest_records'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    author_name = Column(String(50), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
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


def validate_record_data(data):
    author_name = data.get('author_name')
    message = data.get('message')
    if not message:
        return False, '`message` is required field'
    if not author_name:
        return False, '`author_name` is required field'
    if len(author_name) > GuestRecord.author_name.property.columns[0].type.length:
        return False, '`author_name` is too long'

    return True, ''

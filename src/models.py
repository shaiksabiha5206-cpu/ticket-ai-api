try:
    from .database import Base
except ImportError:
    from database import Base

from sqlalchemy import Column, String, Text


class Ticket(Base):
    __tablename__ = "tickets"
    customer_id = Column(String(100), primary_key=True, index=True)
    email = Column(String(254))
    message = Column(Text)
    urgency = Column(String(10))
    subject = Column(String(255))

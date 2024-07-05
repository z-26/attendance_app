import datetime
from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey, Date, Time
from app.database import Base


class Service(Base):
    """
    Table column details for the services provided
    """
    __tablename__ = "service"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100))
    description = Column(String(500))
    no_of_days = Column(Integer)
    cost = Column(Float)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = updated_at = Column(DateTime(timezone=True), 
                        default=lambda: datetime.datetime.now(datetime.timezone.utc),
                        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))


class Participants(Base):
    """
    Table column details
    """
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
    participant_code = Column(String(15), index=True)
    name = Column(String(250), index=True)
    date_of_birth = Column(Date)
    blood_group = Column(String(5))
    gender = Column(String(10))
    guardian_name = Column(String(250))
    address = Column(String(500))
    start_date = Column(Date)
    city = Column(String(250))
    state = Column(String(250))
    country = Column(String(100))
    pin_code = Column(String(6))
    mobile_number = Column(String(15))
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = updated_at = Column(DateTime(timezone=True), 
                        default=lambda: datetime.datetime.now(datetime.timezone.utc),
                        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))


class Attendance(Base):
    """
    Table column details
    """
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    participant_id = Column(Integer, ForeignKey('participants.id'), nullable=False)
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = updated_at = Column(DateTime(timezone=True), 
                        default=lambda: datetime.datetime.now(datetime.timezone.utc),
                        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
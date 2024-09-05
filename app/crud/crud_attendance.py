from sqlalchemy import and_
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import Optional, List, Union, Dict, Any
import logging
from app.crud.crud_base import CRUDBase
from app.models.attendance_models import Attendance
from app.schemas.attendance import CreateAttendance

logger = logging.getLogger(__name__)

class CRUDAttendance(CRUDBase[Attendance, CreateAttendance, CreateAttendance]):
    def get_by_id(self, db: Session, id: int) -> Optional[Attendance]:
        logger.info(f"get_by_id is triggered")
        try:
            return db.query(Attendance).filter(Attendance.id == id).first()
        except Exception as e:
            logger.exception(f"Error occured in get_by_id : {e}")
    
    def get_total_present_days(self, db: Session, participant_id: int) -> int:
        logger.info(f"get_total_present_days is triggered")
        try:
            return db.query(Attendance).filter(Attendance.participant_id == participant_id).count()
        except Exception as e:
            logger.exception(f"Error occured in get_total_present_days : {e}")
    
    def get_clocked_in(self, db: Session, participant_id: int) -> Optional[Attendance]:
        logger.info(f"get_clocked_in is triggered")
        try:
            return db.query(Attendance).filter(and_(Attendance.participant_id == participant_id, Attendance.start_time != None, Attendance.end_time == None)).first()
        except Exception as e:
            logger.exception(f"Error occured in get_clocked_in : {e}")

    def create(self, db: Session, obj_in: CreateAttendance) -> Optional[Attendance]:
        logger.info(f"create is triggered : {obj_in}")
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = Attendance(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            logger.exception(f"Error occured in create : {e}")
    
    def update_data(self, db: Session, id: int, data: Dict[str, Any]) -> Optional[Attendance]:
        logger.info("update_data is triggered")
        try:
            db.query(Attendance).filter(Attendance.id == id).update(data)
            db.commit()
            return db.query(Attendance).filter(Attendance.id == id).first()
        except Exception as e:
            logger.exception(f"Error occured in update_data : {e}")


crud_attendance = CRUDAttendance(Attendance)
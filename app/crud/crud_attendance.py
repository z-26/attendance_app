from sqlalchemy import desc
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import Optional, List, Union, Dict, Any
import logging
from app.crud.crud_base import CRUDBase
from app.models.attendance_models import Participants
from app.schemas.attendance import ParticipantsInDB, UpdateParticipants

logger = logging.getLogger(__name__)


class CRUDParticipants(CRUDBase[Participants, ParticipantsInDB, UpdateParticipants]):
    def get_by_id(self, db: Session, id: int) -> Optional[Participants]:
        logger.info(f"get_by_id is triggered")
        try:
            return db.query(Participants).filter(Participants.id == id).first()
        except Exception as e:
            logger.exception(f"Error occured in get_by_id : {e}")
    
    def get_by_code(self, db: Session, code: str) -> Optional[Participants]:
        logger.info(f"get_by_code is triggered")
        try:
            return db.query(Participants).filter(Participants.participant_code == code).first()
        except Exception as e:
            logger.exception(f"Error occured in get_by_code : {e}")
    
    def get_all_participants(self, db: Session, is_active: Optional[bool] = None) -> Optional[List[Participants]]:
        logger.info(f"get_all_participants is triggered")
        try:
            if is_active:
                return db.query(Participants).filter(Participants.is_active == True).all()
            else:
                return db.query(Participants).all()
        except Exception as e:
            logger.exception(f"Error occured in get_all_participants : {e}")
    
    def get_last_participant(self, db:Session) -> Optional[Participants]:
        logger.info("get_last_participant is trigerred")
        try:
            last_record = db.query(Participants).order_by(desc(Participants.id)).first()
            if last_record:
                return last_record
            else:
                return None
        except Exception as e:
            logger.exception(f"Error occured in get_last_participant : {e}")

    def create(self, db: Session, obj_in: ParticipantsInDB) -> Optional[Participants]:
        logger.info(f"create is triggered : {obj_in}")
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = Participants(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            logger.exception(f"Error occured in create : {e}")
    
    def update(self, db: Session, *, db_obj: Participants, obj_in: Union[UpdateParticipants, Dict[str, Any]]) -> Participants:
        logger.info(f"update is trigger: {obj_in}")
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)
            obj_data = jsonable_encoder(db_obj)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            logger.exception(f"Error occured in update : {e}")
    
    def delete_participant(self, db: Session, code: str, data: Dict[str, Any]):
        logger.info(f"delete_participant is triggered")
        try:
            db.query(Participants).filter(Participants.participant_code == code).update(data)
            db.commit()
            return db.query(Participants).filter(Participants.participant_code == code).first()
        except Exception as e:
            logger.exception(f"Error occured in delete_participant : {e}")


crud_participants = CRUDParticipants(Participants)
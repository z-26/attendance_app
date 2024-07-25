from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import Optional, List, Union, Dict, Any
import logging
from app.crud.crud_base import CRUDBase
from app.models.attendance_models import Service
from app.schemas.services import CreateService, UpdateService

logger = logging.getLogger(__name__)


class CRUDService(CRUDBase[Service, CreateService, UpdateService]):

    def get_by_id(self, db: Session, id: int) -> Optional[Service]:
        logger.info(f"get_by_id is triggered")
        try:
            return db.query(Service).filter(Service.id == id).first()
        except Exception as e:
            logger.exception(f"Error occured in get_by_id : {e}")

    def get_all_service(self, db: Session) -> Optional[List[Service]]:
        logger.info(f"get_all_service is triggered")
        try:
            return db.query(Service).all()
        except Exception as e:
            logger.exception(f"Error occured in get_all_service : {e}")

    def create(self, db: Session, obj_in: CreateService) -> Optional[Service]:
        logger.info(f"create is triggered : {obj_in}")
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = Service(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            logger.exception(f"Error occured in create : {e}")
    
    def update(self, db: Session, *, db_obj: Service, obj_in: Union[UpdateService, Dict[str, Any]]) -> Service:
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


crud_service = CRUDService(Service)

import logging
from fastapi import APIRouter, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.services import CreateService, UpdateService
from app.crud.crud_service import crud_service
from app.service.utils import generate_response
from app.service import response_msg as messages


router = APIRouter()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

@router.post("/service")
def create_service(request: Request,
                   payload: CreateService,
                   db: Session = Depends(deps.get_db)):
    """
    This Api will add a new service in the db 
    """
    logger.info(f"create_service is triggered....")
    try:
        if payload:
            service = crud_service.create(db=db, obj_in=payload)
            if service:
                return generate_response(status_code=status.HTTP_201_CREATED, message=messages.SUCCESS, data=[jsonable_encoder(service)])
            else:
                return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.ERROR, data=None)
        else:
            return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.ERROR)
    except Exception as e:
        logger.exception(f"Error occured in create_service : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)


@router.get("/service")
def get_all_services(request: Request,
                     db: Session = Depends(deps.get_db)):
    """
    This Api will get all the services provided
    """
    logger.info(f"get_all_services is triggered....")
    try:
        services = crud_service.get_all_service(db=db)
        
        if services:
            return generate_response(status_code = status.HTTP_200_OK, message = messages.SUCCESS, data=jsonable_encoder(services))
        else:
            return generate_response(status_code = status.HTTP_404_NOT_FOUND, message = messages.DATA_NOT_FOUND, data=None)
    
    except Exception as e:
        logger.exception(f"Error occured in get_all_services : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)


@router.put("/service")
def update_service(request:Request,
                   id: int,
                   payload: UpdateService,
                   db: Session = Depends(deps.get_db)):
    '''
        This API will update the service by the id(PK).
    '''
    logger.info(f"update_service is triggered....")
    try:
        service = crud_service.get_by_id(db=db, id=id)
        if service:
            updated_service = crud_service.update(db=db, db_obj=service, obj_in=payload)
            if updated_service:
                return generate_response(status_code = status.HTTP_200_OK, message = messages.SUCCESS, data=[jsonable_encoder(updated_service)])
            else:
                return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.ERROR, data=None)
        else:
            return generate_response(status_code = status.HTTP_404_NOT_FOUND, message = messages.DATA_NOT_FOUND, data=None)
    
    except Exception as e:
        logger.exception(f"Error occured in update_service : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)


@router.delete("/service")
def delete_service(request:Request,
                   id: int,
                   db: Session = Depends(deps.get_db)):
    '''
        This API will delete the service by the id(PK).
    '''
    logger.info(f"delete_service is triggered....")
    try:
        deleted_service = crud_service.delete(db=db, id=id)
        if deleted_service == True:
            return generate_response(status_code = status.HTTP_200_OK, message = messages.SUCCESS)
        else:
            return generate_response(status_code = status.HTTP_404_NOT_FOUND, message = messages.DATA_NOT_FOUND)
    
    except Exception as e:
        logger.exception(f"Error occured in delete_service : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)

import logging
from fastapi import APIRouter, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.attendance import CreateParticipants, ParticipantsInDB, UpdateParticipants
from app.crud.crud_attendance import crud_participants
from app.service.utils import generate_response
from app.service import response_msg as messages


router = APIRouter()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

@router.post("/participant")
def create_participants(request: Request,
                        payload: CreateParticipants,
                        db: Session = Depends(deps.get_db)):
    """
    This Api will add a new participant in the db 
    """
    logger.info(f"create_participants is triggered....")
    try:
        last_participant = crud_participants.get_last_participant(db=db)
        if last_participant:
            participant_code = f"P{last_participant.service_id}{str(last_participant.id + 1).zfill(5)}"
        else:
            participant_code = 1
        payload = ParticipantsInDB(**payload.dict(),
                                    participant_code=participant_code)
        participant = crud_participants.create(db=db, obj_in=payload)
        if participant:
            return generate_response(status_code=status.HTTP_201_CREATED, message=messages.SUCCESS, data=[jsonable_encoder(participant)])
        else:
            return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.ERROR, data=None)
    except Exception as e:
        logger.exception(f"Error occured in create_participants : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)


@router.get("/participant")
def get_participant_by_code(request: Request,
                            participant_code: str,
                            db: Session = Depends(deps.get_db)):
    """
    This Api will get a participant by their code
    """
    logger.info(f"get_participant_by_code is triggered....")
    try:
        participant = crud_participants.get_by_code(db=db, code=participant_code)
        if participant:
            return generate_response(status_code=status.HTTP_200_OK, message=messages.SUCCESS, data=[jsonable_encoder(participant)])
        else:
            return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.ERROR, data=None)
    except Exception as e:
        logger.exception(f"Error occured in get_participant_by_code : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)


@router.get("/all-participants")
def get_all_participants(request: Request,
                         active: bool,
                         db: Session = Depends(deps.get_db)):
    """
    This Api will get all participants either active or all participants
    """
    logger.info(f"get_all_participants is triggered....")
    try:
        participant = crud_participants.get_all_participants(db=db, is_active=active)
        if participant:
            return generate_response(status_code=status.HTTP_200_OK, message=messages.SUCCESS, data=participant)
        else:
            return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.ERROR, data=None)
    except Exception as e:
        logger.exception(f"Error occured in get_all_participants : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)


@router.put("/participant")
def update_participant(request: Request,
                       participant_code: str,
                       payload: UpdateParticipants,
                       db: Session = Depends(deps.get_db)):
    """
    This Api will update participant records in the db 
    """
    logger.info(f"update_participant is triggered....")
    try:
        participant_exist = crud_participants.get_by_code(db=db, code=participant_code)
        if participant_exist:
            if payload:
                updated_participant = crud_participants.update(db=db, db_obj=participant_exist, obj_in=payload)
                if updated_participant:
                    return generate_response(status_code = status.HTTP_200_OK, message = messages.SUCCESS, data=[jsonable_encoder(updated_participant)])
                else:
                    return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.ERROR, data=None)
        else:
            return generate_response(status_code = status.HTTP_404_NOT_FOUND, message = messages.DATA_NOT_FOUND, data=None)
    except Exception as e:
        logger.exception(f"Error occured in update_participant : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)


@router.delete("/participant")
def remove_participant(request: Request,
                       participant_code: str,
                       db: Session = Depends(deps.get_db)):
    """
    This Api will mark a participant inactive by their code
    """
    logger.info(f"remove_participant is triggered....")
    try:
        to_change = {"is_active": False}
        participant = crud_participants.delete_participant(db=db, code=participant_code, data=to_change)
        if participant:
            return generate_response(status_code=status.HTTP_200_OK, message=messages.SUCCESS, data=[jsonable_encoder(participant)])
        else:
            return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.ERROR, data=None)
    except Exception as e:
        logger.exception(f"Error occured in remove_participant : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)
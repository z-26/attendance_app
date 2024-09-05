import logging
from fastapi import APIRouter, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.attendance import AttendanceClock, CreateAttendance
from app.crud.crud_participants import crud_participants
from app.crud.crud_attendance import crud_attendance
from app.crud.crud_service import crud_service
from app.service.utils import generate_response
from app.service import response_msg as messages
from datetime import datetime, timezone

router = APIRouter()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

@router.post("/clock-in")
def attendance_clock_in(request: Request,
                        payload:AttendanceClock,
                        db: Session = Depends(deps.get_db)):
    """
    This API will punch in the attendance of the user
    """
    logger.info(f"attendance_clock_in is triggered....")
    try:
        active_participant = crud_participants.get_active_participant(db=db, participant_code=payload.participant_code)
        if active_participant:
            total_present_days = crud_attendance.get_total_present_days(db=db, participant_id=active_participant.id)
            service_opted = crud_service.get_by_id(db=db, id=active_participant.service_id)
            if total_present_days < service_opted.no_of_days:
                payload_in_db = CreateAttendance(**payload.dict(),
                                 date=datetime.now(timezone.utc).date(),
                                 start_time=datetime.now(timezone.utc).time())
                attendance_punched = crud_attendance.create(db=db, obj_in=payload_in_db)
                if attendance_punched:
                    return generate_response(status_code=status.HTTP_200_OK, message=messages.SUCCESS, data=[jsonable_encoder(attendance_punched)])
                else:
                    return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.ERROR, data=None)
            else:
                return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.COURSE_ENDED, data=None)
        else:
            return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.INACTIVE_USER, data=None)
    except Exception as e:
        logger.exception(f"Error occured in attendance_clock_in : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)


@router.post("/clock-out")
def attendance_clock_out(request: Request,
                         payload: AttendanceClock,
                         db: Session = Depends(deps.get_db)):
    """
    This API will punch out the attendance of the user
    """
    logger.info(f"attendance_clock_out is triggered....")
    try:
        active_participant = crud_participants.get_active_participant(db=db, participant_code=payload.participant_code)
        if active_participant:
            clocked_in_data = crud_attendance.get_clocked_in(db=db, participant_id=active_participant.id)
            if clocked_in_data:
                data = {"end_time": datetime.now(timezone.utc).time()}
                clocked_out = crud_attendance.update_data(db=db, id=clocked_in_data.id, data=data)
                if clocked_out:
                    return generate_response(status_code=status.HTTP_200_OK, message=messages.SUCCESS, data=[jsonable_encoder(clocked_out)])
                else:
                    return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.ERROR, data=None)
            else:
                 return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.NOT_CLOCKED_IN, data=None)
        else:
            return generate_response(status_code = status.HTTP_400_BAD_REQUEST, message = messages.INACTIVE_USER, data=None)
    except Exception as e:
        logger.exception(f"Error occured in attendance_clock_in : {e}")
        return generate_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=messages.SOMETHING_WENT_WRONG)


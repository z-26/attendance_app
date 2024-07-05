from fastapi import status
import logging
from typing import Optional
import app.service.response_msg as messages
from app.schemas.generic_response import Response


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_response(status_code=status.HTTP_200_OK, message=messages.SUCCESS, data=[])->Optional[Response]:
    """
        Generic response function, can be used in all the return statements
    """
    logger.info("generate_response is triggered")
    try:
        return Response(status_code=status_code,
                                data=data,
                                message=message)
    except Exception as e:
        logger.exception(f"Error occurred in generate_response:{e}")

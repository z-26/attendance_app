from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder

from typing import Optional, List, Union, Dict, Any

import logging


logger = logging.getLogger(__name__)

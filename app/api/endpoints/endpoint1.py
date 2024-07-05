from fastapi import APIRouter, Depends, Request, status
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from pydantic import BaseModel

#Generic response schema to used in generate_response function
class Response(BaseModel):
    status_code: int = 200
    message: str
    data: list = []
    
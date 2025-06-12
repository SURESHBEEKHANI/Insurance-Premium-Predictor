from pydantic import BaseModel

# Pydantic models for request validation
class SignupRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str
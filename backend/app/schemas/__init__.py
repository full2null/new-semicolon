from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from .response import ApiResponse, ErrorResponse, error_response, success_response


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Question schemas
class QuestionBase(BaseModel):
    title: str
    content: str


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_solved: Optional[bool] = None


class Question(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author_id: int
    views: int
    is_solved: bool
    author: User
    answers: List["Answer"] = []

    class Config:
        from_attributes = True


# Answer schemas
class AnswerBase(BaseModel):
    content: str


class AnswerCreate(AnswerBase):
    question_id: int


class AnswerUpdate(BaseModel):
    content: Optional[str] = None
    is_accepted: Optional[bool] = None


class Answer(AnswerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author_id: int
    question_id: int
    is_accepted: bool
    author: User

    class Config:
        from_attributes = True


# Tag schemas
class TagBase(BaseModel):
    name: str
    description: Optional[str] = None


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

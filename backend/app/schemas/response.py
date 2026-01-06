"""
통일된 API 응답 형식을 위한 스키마
"""
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """
    표준 API 응답 형식
    
    Examples:
        성공 응답:
        {
            "success": true,
            "data": {...},
            "message": "Operation successful"
        }
        
        실패 응답:
        {
            "success": false,
            "error": "Error message",
            "message": "Detailed error description"
        }
    """

    success: bool
    data: Optional[T] = None
    message: Optional[str] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """에러 응답 형식"""

    success: bool = False
    error: str
    message: str
    detail: Optional[Any] = None


def success_response(
    data: Any = None, message: str = "Operation successful"
) -> ApiResponse:
    """성공 응답 생성 헬퍼 함수"""
    return ApiResponse(success=True, data=data, message=message)


def error_response(
    error: str, message: str = "Operation failed", detail: Any = None
) -> ErrorResponse:
    """에러 응답 생성 헬퍼 함수"""
    return ErrorResponse(error=error, message=message, detail=detail)

from typing import Any, Optional, Dict

from fastapi import HTTPException


class ApiError(HTTPException):
    def __init__(
            self,
            status_code: int,
            error_type: str,
            error_message: str,
            detail: Any = None,
            headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail,
                         headers=headers)
        self.error_type = error_type
        self.error_message = error_message
        self.result = False

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}" \
               f"(status_code={self.status_code!r}, " \
               f"error_type={self.error_type!r}), " \
               f"error_message={self.error_message!r}"

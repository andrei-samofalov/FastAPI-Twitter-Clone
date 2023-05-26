"""
Модуль содержит ответы для апи
RESPONSE_401
RESPONSE_401_422
RESPONSE_401_422_404
RESPONSE_401_422_404_403
RESPONSE_401_422_404_400
"""


RESPONSE_401 = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": {
                    "result": False,
                    "error_type": "Unauthorized",
                    "error_message": "Not authenticated",
                }
            }
        },
    }
}

RESPONSE_401_422 = {
    **RESPONSE_401,
    422: {
        "description": "Validation error",
        "content": {
            "application/json": {
                "example": {
                    "result": False,
                    "error_type": "validation error",
                    "error_message": "validation error message",
                }
            }
        },
    },
}

RESPONSE_401_422_404 = {
    **RESPONSE_401_422,
    404: {
        "description": "Not found",
        "content": {
            "application/json": {
                "example": {
                    "result": False,
                    "error_type": "not found",
                    "error_message": "not found element",
                }
            }
        },
    },
}

RESPONSE_401_422_404_403 = {
    **RESPONSE_401_422_404,
    403: {
        "description": "Access forbidden",
        "content": {
            "application/json": {
                "example": {
                    "result": False,
                    "error_type": "Access error",
                    "error_message": "Access forbidden",
                }
            }
        },
    },
}

RESPONSE_401_422_404_400 = {
    **RESPONSE_401_422_404,
    400: {
        "description": "Bad request",
        "content": {
            "application/json": {
                "example": {
                    "result": False,
                    "error_type": "Bad request",
                    "error_message": "Can't follow yourself",
                }
            }
        },
    },
}

from fastapi import HTTPException 
class AppException(HTTPException):
    def __init__(self, message: str, error: str = None, status_code: int = 400, data: any = None): 
        detail={ "success": False,
                  "message": message, 
                  "data": data, 
                  "error":error
                  
        }
        super().__init__(status_code=status_code,detail=detail)
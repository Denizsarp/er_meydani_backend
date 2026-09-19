class PasswordOP():
    @staticmethod
    def validate_password(plain_password:str) -> str:
        size:int = len(plain_password)
        exc = ''

        
        if size < 8 or size > 25:
            exc = "The Password must be longer than 8 and shorter than 25 chars."
        

        elif plain_password.isdigit():
            exc = "Password must include at least one letter"

        return exc

        
        




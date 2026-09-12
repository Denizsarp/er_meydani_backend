from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class Hash:
    @staticmethod
    def bcrypt(password:str):
        return pwd_context.hash(password)


    @staticmethod
    def verify_password(hashed_password:str, plain_password:str):
        return pwd_context.verify(plain_password, hashed_password)
        
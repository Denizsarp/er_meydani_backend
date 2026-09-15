from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


#Creating Hash class for password security

class Hash:
    @staticmethod
    def bcrypt(plain_password:str):
        hashed_password = pwd_context.hash(plain_password)
        return hashed_password 


    @staticmethod
    def verify_password(plain_password:str, hashed_password:str):
        return pwd_context.verify(plain_password, hashed_password)



    
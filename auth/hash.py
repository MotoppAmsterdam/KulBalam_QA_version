from passlib.hash import bcrypt_sha256

class Hash:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt_sha256.hash(password)

    @staticmethod
    def verify_password(hashed_password: str, plain_password: str) -> bool:
        return bcrypt_sha256.verify(plain_password, hashed_password)
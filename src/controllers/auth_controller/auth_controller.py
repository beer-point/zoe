from models.user import User


class IAuth:
    def login() -> User:
        pass

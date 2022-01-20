from firebase_admin import firestore


class User:
    def __init__(self, name, balance, ref=None):
        self.name = name
        self.balance = balance
        self.ref: firestore.firestore.DocumentReference = ref

    @staticmethod
    def from_dict(source):
        if source is not None and isinstance(source, dict):
            return User(
                source.get('name', ''),
                source.get('balance', 0),
                source.get('ref', None)
            )
        return None

    def to_dict(self):
        return {"name": self.name, "balance": self.balance}

    def __repr__(self):
        return(
            f'User(\
                name={self.name}, \
                balance={self.balance}, \
            )'
        )

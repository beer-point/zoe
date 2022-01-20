from models.beer import Beer
from models.user import User
from firebase_admin import firestore


class Station:
    def __init__(self, sync_code, beer=None, active_user=None, ref=None):
        self.sync_code: str = sync_code
        self.beer: Beer = beer
        self.active_user: User = active_user
        self.ref: firestore.firestore.DocumentReference = ref

    @staticmethod
    def from_dict(source):
        if source is not None and isinstance(source, dict):
            return Station(
                source.get('syncCode', ''),
                Beer.from_dict(source.get('beer', None)),
                User.from_dict(source.get('activeUser', None)),
                source.get('ref', None)
            )
        return None

    def to_dict(self):
        return {
            "syncCode": self.sync_code,
            "activeUser": self.active_user.to_dict() if self.active_user is not None else None,
            "beer": self.beer.to_dict()
        }

    def __repr__(self):
        return(
            f'Station(\
                sync_code={self.sync_code}, \
                active_user={self.active_user.__repr__() if self.active_user is not None else "None"} \
                beer={self.beer.__repr__()} \
            )'
        )

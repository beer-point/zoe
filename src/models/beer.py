from models.brewer import Brewer
from firebase_admin import firestore


class Beer:
    def __init__(self, name, type, cost, description, photo_url, brewer=None, ref=None):
        self.name: str = name
        self.type: str = type
        self.cost_per_lt: int = cost
        self.brewer: Brewer = brewer
        self.description = description
        self.photo_url: str = photo_url
        self.ref: firestore.firestore.DocumentReference = ref

    @staticmethod
    def from_dict(source):
        print(source)
        if source is not None and isinstance(source, dict):
            return Beer(
                source.get('name', ''),
                source.get('type', ''),
                source.get('costPerLt', 0),
                source.get('description', ''),
                source.get('photoUrl', ''),
                Brewer.from_dict(source.get('brewer', None)),
                source.get('ref', None)
            )
        return None

    def to_dict(self):
        return {"name": self.name,  "type": self.type, "costPerLt": self.cost_per_lt, "photoUrl": self.photo_url,  "description": self.description, "brewer": self.brewer.to_dict() if self.brewer is not None else None}

    def __repr__(self):
        return(
            f'Beer(\
                name={self.name}, \
                type={self.type}, \
                cost_per_lt={self.cost_per_lt}, \
                photo_url={self.photo_url}, \
                description={self.description}, \
                brewer={self.brewer.__repr__() if self.brewer is not None else "None"}\
            )'
        )

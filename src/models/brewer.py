from firebase_admin import firestore


class Brewer:
    def __init__(self, name, photo_url, ref=None):
        self.name: str = name
        self.photo_url: str = photo_url
        self.ref: firestore.firestore.DocumentReference = ref

    @staticmethod
    def from_dict(source):
        if source is not None and isinstance(source, dict):

            return Brewer(
                source.get('name', ''),
                source.get('photoUrl', ''),
                source.get('ref', None)
            )
        return None

    def to_dict(self):
        return {"name": self.name, "photoUrl": self.photo_url}

    def __repr__(self):
        return(
            f'Brewer(\
                name={self.name}, \
                photo_url={self.photo_url}, \
            )'
        )

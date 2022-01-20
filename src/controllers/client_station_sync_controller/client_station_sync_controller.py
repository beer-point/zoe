

import uuid


class ClientStationSyncController:

    def _upload_code(self, code: str):
        pass

    def generate_sync_code(self) -> str:
        code = uuid.uuid4()
        self.upload_code(code)

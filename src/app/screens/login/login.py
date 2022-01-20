import qrcode
from kivy.logger import Logger
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import uuid
import time
import threading
from app.firebase_init import getFirestoreClient
from app.constants import station_ref

from models.user import User
client = getFirestoreClient()


class LoginScreen(Screen):

    img = StringProperty('qr.png')
    is_generating_sync_code = BooleanProperty(True)

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self, *args):
        self._generate_qr_in_thread()

    def _generate_qr(self, code):
        # this should go in separate thread
        img = qrcode.make(code)
        img.save('qr.png')

    def login(self):
        self.parent.user = User('Luis', 80)
        Logger.info("[APP ] login")

    def _generate_qr_in_thread(self):
        self.is_generating_sync_code = True

        def in_thread_call():
            code = str(uuid.uuid4())[:8]
            station_ref.update({
                "syncCode": code
            })
            self._generate_qr(code)

        thread = threading.Thread(target=in_thread_call)
        thread.start()

        def check_generating_qr_end(interval):
            if not thread.is_alive():
                self.is_generating_sync_code = False
                return False

        Clock.schedule_interval(check_generating_qr_end, 0.1)

    def on_is_generating_sync_code(self, screen, value):
        if not value:
            self.ids['qr_image'].reload()

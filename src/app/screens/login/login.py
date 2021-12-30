from kivy.uix.screenmanager import Screen
from kivy.logger import Logger


class LoginScreen(Screen):
    def login(self):
        self.manager.transition.direction = "left"
        self.manager.current = "session"
        Logger.info("[APP ] login")

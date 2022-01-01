from turtle import width
from app.screens.session.session import SessionScreen
from app.screens.login.login import LoginScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App


from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')


class WindowManager(ScreenManager):
    pass


class BeerApp(App):
    pass

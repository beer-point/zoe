from kivy.uix.screenmanager import Screen
from kivy.logger import Logger
from kivymd.uix.screen import MDScreen


class TestScreen(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        print('Initing test screen')

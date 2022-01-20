from firebase_admin import firestore
from kivy.config import Config
from kivymd.app import MDApp
from models.station import Station
from models.user import User
from kivy.uix import *
from kivymd.uix import *
from app.screens.home.home import HomeScreen
from app.screens.session.session import SessionScreen
from app.screens.login.login import LoginScreen
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager
from app.firebase_init import getFirestoreClient
from app.constants import station_ref

client = getFirestoreClient()

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')


class BeerScreenManager(ScreenManager):
    user = ObjectProperty(None, allownone=True)
    station = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):

        self.station = self._get_station()
        self.user = self.station.active_user
        self.active_user_change_subscription = self._subscribe_to_active_user_change()

        super().__init__(**kwargs)

    def on_user(self, screen, new_user):
        if new_user is not None:
            self.transition.direction = "left"
            self.current = "session"
        else:
            self.transition.direction = "right"
            self.current = "home"

    def _get_station_from_firestore_snapshot(self, station_data):
        beer_ref: firestore.firestore.DocumentReference = station_data['beerRef']
        brewer_ref: firestore.firestore.DocumentReference = beer_ref.parent.parent
        active_user_ref: firestore.firestore.DocumentReference = station_data['activeUserRef']
        beer_dict = beer_ref.get().to_dict()
        brewer_dict = brewer_ref.get().to_dict()
        active_user_dict = {
            "ref": active_user_ref,
            **active_user_ref.get().to_dict()
        } if active_user_ref is not None else None
        station_dict = {
            'ref': station_ref,
            'beer': {
                "ref": beer_ref,
                "brewer": {
                    "ref": brewer_ref,
                    **brewer_dict
                },
                **beer_dict
            },
            'activeUser': active_user_dict,
            **station_data
        }
        station = Station.from_dict(station_dict)
        return station

    def _get_station(self):
        print(station_ref)
        station_data = station_ref.get().to_dict()
        return self._get_station_from_firestore_snapshot(station_data)

    def _subscribe_to_active_user_change(self):

        def on_active_user_change(doc_snapshot, changes, read_time):
            for doc in doc_snapshot:
                station_dict = doc.to_dict()
                station = self._get_station_from_firestore_snapshot(
                    station_dict)

                self.user = station.active_user

        return station_ref.on_snapshot(on_active_user_change)

    def _unsubscribe_to_active_user_change(self):
        self.active_user_change_subscription.close()


class BeerApp(MDApp):
    pass

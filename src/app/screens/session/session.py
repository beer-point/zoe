from datetime import datetime
from math import floor
import threading
from kivy.uix.screenmanager import Screen
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, ObjectProperty
from firebase_admin import firestore

from controllers.beer_flow_controller.beer_flow_controller import BeerFlowController
from controllers.beer_flow_controller.beer_flow_idle_observer import BeerFlowIdleObserver
from app.firebase_init import getFirestoreClient
from controllers.beer_flow_controller.flow_session import FlowSession
from models.station import Station
client = getFirestoreClient()


class SessionScreen(Screen):

    is_ending_session = BooleanProperty(False)
    flow = NumericProperty(0)
    virtual_balance = NumericProperty(0)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.beer_flow_controller = BeerFlowController()
        self.update_flow_clock = None
        self.idle_observer = None

    def on_leave(self, *args):
        self.virtual_balance = 0
        self.is_ending_session = False
        return super().on_leave(*args)

    def on_enter(self, *args):
        self.virtual_balance = self.parent.user.balance

        def on_idle():
            self.end_session()

        self.idle_observer = BeerFlowIdleObserver(on_idle)
        self.beer_flow_controller.start_session()
        self.beer_flow_controller.get_session().attach_observer(self.idle_observer)

        def _update_session_flow(interval):
            if self.beer_flow_controller.has_active_session:
                self.flow = self.beer_flow_controller.get_flowed_beer()

        self.update_flow_clock = Clock.schedule_interval(
            _update_session_flow, 0.1)

        return super().on_enter(*args)

    def end_session(self):
        # In case end_session by user click happens at same time that end session by idle
        Logger.info("[APP ] end session")
        if not self.is_ending_session:
            self.is_ending_session = True
            self.idle_observer.cancel()
            self.idle_observer = None
            session = self.beer_flow_controller.end_session()
            self._save_session(session)
            if self.update_flow_clock is not None:
                self.update_flow_clock.cancel()

    def on_flow(self, screen, new_flow):
        self.virtual_balance = self.parent.user.balance - \
            self.parent.station.beer.cost_per_lt * new_flow

    def on_virtual_balance(self, screen, new_balance):
        if new_balance <= 0:
            self.beer_flow_controller.close_valve()

    def _save_session(self, session: FlowSession):
        flow_in_lt = session.get_flow()

        def save_session_thread_run():
            station: Station = self.parent.station
            session_ref: firestore.firestore.DocumentReference = self.parent.user.ref.collection(
                'sessions').document()
            session_ref.set({
                "startedAt": session.started_at,
                "endedAt": session.ended_at,
                "beerRef": station.beer.ref,
                "stationRef": station.ref,
                "beerCostPerLt": station.beer.cost_per_lt,
                "ml": flow_in_lt * 1000,
            })

        save_session_thread = threading.Thread(target=save_session_thread_run)
        save_session_thread.start()

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.clock import Clock

from controllers.beer_flow_controller.beer_flow_controller import BeerFlowController

beer_cost_per_lt = 200
available_money = 80


class SessionScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.beer_flow_controller = BeerFlowController()

    def on_leave(self, *args):
        self.beer_flow_controller.end_session()
        return super().on_leave(*args)

    def on_enter(self, *args):
        self.beer_flow_controller.start_session()
        return super().on_enter(*args)

    def goBack(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login"
        Logger.info("[APP ] end session")


class UpdatingCurrentCredits(Label):

    def __init__(self, **kw):
        super().__init__(**kw)

        def updateText(a):
            print('calling update text')
            print(self.parent.parent.beer_flow_controller.get_flowed_beer())
            beer_flow = self.parent.parent.beer_flow_controller.get_flowed_beer()
            virtual_available_money = available_money - \
                (beer_flow * beer_cost_per_lt)

            if virtual_available_money <= 0:
                virtual_available_money = 0.0

            self.text = "{:10.0f}".format(virtual_available_money)

        Clock.schedule_interval(updateText, 0.1)

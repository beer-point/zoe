from controllers.beer_flow_controller.flow_session import FlowSession
from controllers.beer_flow_controller.valve_controller import ValveController
from models.beer import Beer


class BeerFlowController:
    """Controlls all modules involve in pouring beer, such as the flow and valve, also counts the flow of beer"""

    def __init__(self):
        self._flow_session = None
        self._valve_controller = ValveController()

    def start_session(self):
        self._flow_session = FlowSession()
        self._valve_controller.open()
        self._flow_session.start()

    def end_session(self):
        self._valve_controller.close()
        self._flow_session.end()
        session = self._flow_session
        self._flow_session = None
        return session

    def get_flowed_beer(self):
        if not self._flow_session == None:
            return self._flow_session.get_flow()
        return 0.0

    def has_active_session(self):
        return self._flow_session.is_active

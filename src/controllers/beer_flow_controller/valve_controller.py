
class IValveController:
    def open():
        pass

    def close():
        pass

    def is_valve_open() -> bool:
        pass


class ValveController(IValveController):

    def __init__(self):
        self._is_valve_open = False

    def open(self):
        print("opening valve")

    def close(self):
        print("closing valve")

    def is_valve_open(self) -> bool:
        return self._is_valve_open

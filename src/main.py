import time
from app.beer import BeerApp
from controllers.beer_flow_controller.beer_flow_controller import FlowSession

# a = FlowSession()
# a.start()
# print("Starting beer flow session")


# beer_cost_per_lt = 200
# available_money = 80

# while a.is_active:
#     time.sleep(0.1)
#     beer_flow = a.get_flow()
#     virtual_available_money = available_money - \
#         (beer_flow * beer_cost_per_lt)
#     if virtual_available_money <= 0:
#         virtual_available_money = 0.0
#         a.end()
#     print(virtual_available_money)


if __name__ == '__main__':
    BeerApp().run()

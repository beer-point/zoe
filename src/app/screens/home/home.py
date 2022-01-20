from kivy.uix.screenmanager import Screen


class HomeScreen(Screen):

    def on_enter(self, *args):
        print('ENTERING!')
        return super().on_enter(*args)

    def go_to_login(self):
        self.manager.transition.direction = "left"
        self.manager.current = "login"

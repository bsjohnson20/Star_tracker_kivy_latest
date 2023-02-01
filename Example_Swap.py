from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window


class ScreenMain(Screen):
    pass


class ScreenOne(Screen):
    pass


class ScreenTwo(Screen):
    pass

class WelcomeScreen(Screen):
    pass


class Manager(ScreenManager):
    screen_main_id = ObjectProperty()
    screen_one_id = ObjectProperty()
    screen_two_id = ObjectProperty()


class LunaApp(App):

    def build(self):

        """This method returns the Manager class"""
        self.root = Manager()
        self.auth()
        return self.root

    def auth(self):

        """This function is called by build(), return
        value should determine which screen is displayed on running the App,
        by default the MAIN SCREEN IS FIRST SHOWN"""

        a = 3
        b = 5
        value = a + b
        if value > 0 <= 5:
            print('Show screen 1')
            self.root.current = 'Screen1'
        elif value > 5 <= 10:
            print('Show screen 2')
            self.root.current = 'Screen2'
        else:
            print('Show main screen')
            self.root.current = 'ScreenMain'
        print('This is the return value: ', value)

        self.root.current='Screen2'

if __name__ =="__main__":
    LunaApp().run()
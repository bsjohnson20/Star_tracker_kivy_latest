import weakref

import kivy
from IPy import IP
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore  # use for storing data
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

settings_storage = JsonStore('settings.json')
devices_storage = JsonStore('devices.json')


# settings_storage.put("LunaDevice",ip="123.42.12",desc="Hello!",LastOnline=5245425)
# settings_storage.get("LunaDevice")


class ScreenWelcome(Screen):
    def generateScreen(self):
        pass


class ScreenAboutMe(Screen):
    pass


class ScreenIOTControl(Screen):
    def loadPage(self, name, dev_type, **kwargs):
        # load the page for the device type and device name with the data and controls.
        App.get_running_app().root.current = 'ScreenIOTControl'
        # devices_storage[caller_name]
        print(name, dev_type)



class ScreenAddDevice(Screen):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def on_enter(self, *args):
        print("Nothing to see here!")

    def Validate(self, *args, **kwargs):
        temp = App.get_running_app().root.ids.screen_Add_id.ids
        # Check if nothing inputted or item already in dict
        if temp.ip_id.text == '' or temp.name.text == '' or temp.name.text in devices_storage:
            box = BoxLayout(orientation="vertical")
            popup = Popup(title='Error', content=box, size_hint={0.4, 0.2})
            box.add_widget(Label(text="Missing data or already in database"))
            box.add_widget(Button(text="Close", on_press=popup.dismiss))
            popup.open()
        else:
            try:
                IP(temp.ip_id.text)
                devices_storage.put(temp.name.text, desc=temp.desc.text, ip=temp.ip_id.text,
                                    device_type=temp.dropdown_opener.text)
                App.get_running_app().root.current = "ScreenHome"
                App.get_running_app().root.ids.screen_Home_id.setup()
            except ValueError:

                box = BoxLayout(orientation="vertical")
                popup = Popup(title='Error', content=box, size_hint={0.4, 0.2})
                box.add_widget(Label(text="Invalid IP"))
                box.add_widget(Button(text="Close", on_press=popup.dismiss))
                popup.open()

    def callback(self, text_item):
        print(text_item)

    def assemble(self, *args):
        print("Assembling STARTED")
        dropdown = DropDown()

        device_types = [
            "StarTrackerV1",
            "StarTrackerv2",
            "StarTrackerV3"
        ]
        for item in device_types:
            btn = Button(text='%s' % item, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
            print(f"Assembling: {btn}. {item}")
        self.ids.dropdown_opener.bind(on_release=dropdown.open)
        print(self.ids.dropdown_opener)
        dropdown.bind(on_select=lambda instance, x: setattr(self.ids.dropdown_opener, 'text', x))


class OpenerButton(ButtonBehavior, Image):
    # set image to resources/plus.png
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'resources/play-svgrepo-com (1).png'
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}


        
        


class ScreenHome(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # resize Screen to fit the size of the screen
        self.size = Window.size
        self.size_hint = (None, None)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

    def setup(self):
        """
        Generates cards to be put into the Home screen this contains the Devices name, desc and ip and a button to open the page for it.
        :return:
        """
        self = App.get_running_app().root.ids.screen_Home_id.ids.add_here

        for child in [child for child in
                      self.children]:  # clear screen - this lets us update the screen as well! - no this isn't a lazy workaround so I don't have to append instead... and write a new builder
            self.remove_widget(child)
        for item in devices_storage:
            x = GridLayout(cols=2, size_hint_y=None, size_hint_x=0.7, center_x=0.5, center_y=0.5)
            # Setup labels with their respective data
            x.add_widget(Label(text="name"))
            x.add_widget(Label(text=item))
            x.add_widget(Label(text="desc"))
            x.add_widget(Label(text=devices_storage[item]['desc']))
            x.add_widget(Label(text="ip"))
            x.add_widget(Label(text=devices_storage[item]['ip']))
            dev_type = Label(text="Device Type")
            # root.ids['dev_type'] = dev_type
            x.add_widget(dev_type)
            x.add_widget(Label(text=devices_storage[item]['device_type']))
            x.anchor_x = 'center'
            x.anchor_y = 'center'
            # create THE Box this'll contain labels and the buton to open the corresponding IOT panel
            Box = BoxLayout(size_hint_y=None, center_x=0.5, center_y=0.5)
            Box.add_widget(x)
            # clickable image
            # OpenerButton(on_release=lambda x: self.loadPage(item, devices_storage[item]['device_type']))
            BigButton = OpenerButton()
            BigButton.bind(on_release=lambda x: App.get_running_app().root.ids.screen_IOTControl_id.loadPage(item,
                                                                                                             devices_storage[
                                                                                                                 item][
                                                                                                                 'device_type']))
            # add OpenerButton to Box

            Box.add_widget(BigButton)

            self.add_widget(Box)

    def IOTOpener(self, device_type):
        pass


class ScreenMain(Screen):
    pass


class Manager(ScreenManager):
    current = ObjectProperty()
    last_screen = ObjectProperty()
    splash_next = ObjectProperty()


class ToolBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 100
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        # set orientation to horizontal
        self.orientation = 'horizontal'

        self.add_widget(AddButton())
        self.add_widget(HomeButton())
        self.add_widget(MeButton())
        # background color
        self.background_color = (1, 1, 1, 1)
        # update size on window resize
        self.size_hint = (None, None)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        # add padding to half the width of root screen

    # function to update size on resize


def changeScreenMe(*args, **kwargs):
    App.get_running_app().root.current = 'ScreenAboutMe'


def changeScreenHome(*args, **kwargs):
    App.get_running_app().root.current = 'ScreenHome'


def changeScreenAdd(*args, **kwargs):
    App.get_running_app().root.current = 'ScreenAdd'


class HomeButton(ButtonBehavior, Image):
    # set image to resources/plus.png
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'resources/home-1-svgrepo-com.png'
        self.size_hint = (None, None)
        # self.size = (50, 50)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        # root.manager.current = root.manager.last_screen
        #                     root.manager.last_screen = "ScreenAdd"

        # set bind to the button press to open the add screen

        self.on_release = changeScreenHome
        # scale image to height of root widget
        self.image_size = self.size

        




class AddButton(ButtonBehavior, Image):
    # set image to resources/plus.png

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'resources/add-circle-svgrepo-com.png'
        self.size_hint = (None, None)
        # self.size = (50, 50)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.on_release = changeScreenAdd
        self.background = "black"
        print(self.size)


class MeButton(ButtonBehavior, Image):
    # set image to resources/plus.png
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'resources/account-svgrepo-com.png'
        #self.source = 'resources/anonymous-person-icon-23.jpg'
        self.size_hint = (None, None)
        # self.size = (50, 50)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.bind(on_release=changeScreenMe)


class LunaApp(MDApp):

    def build(self):
        """This method returns the Manager class"""
        self.theme_cls.theme_style = "Dark"
        # change colour of window to purple
        Window.clearcolor = (1, 0, 0, 1)

        self.root = Manager()
        self.checkComplete()  # check if devices already present if so, skip add device screen!
        return self.root

    def checkComplete(self):
        devices_storage = JsonStore('devices.json')
        Clock.schedule_once(App.get_running_app().root.ids.screen_Add_id.assemble, 1)
        if devices_storage:
            # print("AlreadyDone")
            self.root.splash_next = 'ScreenHome'
            self.root.ids.screen_Home_id.setup()
        else:
            self.root.splash_next = 'ScreenAdd'

        """This function is called by build(), return
        value should determine which screen is displayed on running the App,
        by default the MAIN SCREEN IS FIRST SHOWN

        self.root.current = 'Screen2'
        """


if __name__ == "__main__":
    LunaApp().run()

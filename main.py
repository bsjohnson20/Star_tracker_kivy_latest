import weakref
from IPy import IP
from kivy.app import App
from kivy.clock import Clock
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
    def loadPage(self,*args,**kwargs):
        caller_name = args[0]
        devices_storage[caller_name]


class ScreenAddDevice(Screen):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def on_enter(self, *args):
        print("Nothing to see here!")

    def Validate(self, *args, **kwargs):
        temp = App.get_running_app().root.ids.screen_Add_id.ids
        # Check if nothing inputted or item already in dict
        if temp.ip_id.text == '' or temp.name.text == ''  or temp.name.text in devices_storage:
            box = BoxLayout(orientation="vertical")
            popup = Popup(title='Error', content=box, size_hint={0.4, 0.2})
            box.add_widget(Label(text="Missing data or already in database"))
            box.add_widget(Button(text="Close", on_press=popup.dismiss))
            popup.open()
        else:
            try:
                IP(temp.ip_id.text)
                devices_storage.put(temp.name.text, desc=temp.desc.text, ip=temp.ip_id.text,device_type=temp.dropdown_opener.text)
                App.get_running_app().root.current = "ScreenHome"
                App.get_running_app().root.ids.screen_Home_id.setup()
            except ValueError:

                box=BoxLayout(orientation="vertical")
                popup = Popup(title='Error', content=box,size_hint={0.4,0.2})
                box.add_widget(Label(text="Invalid IP"))
                box.add_widget(Button(text="Close",on_press=popup.dismiss))
                popup.open()





    def callback(self, text_item):
        print(text_item)

    def assemble(self,*args):
        print("Assembling STARTED")
        dropdown = DropDown()

        device_types=[
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


class ScreenHome(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def setup(self):
        """
        Generates cards to be put into the Home screen this contains the Devices name, desc and ip and a button to open the page for it.
        :return:
        """
        self = App.get_running_app().root.ids.screen_Home_id.ids.add_here

        for child in [child for child in self.children]: # clear screen - this lets us update the screen as well! - no this isn't a lazy workaround so I don't have to append instead... and write a new builder
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
            x.add_widget(Label(text="Device Type"))
            x.add_widget(Label(text=devices_storage[item]['device_type']))
            x.anchor_x = 'center'
            x.anchor_y = 'center'
            # create THE Box this'll contain labels and the buton to open the corresponding IOT panel
            Box = BoxLayout(size_hint_y=None, center_x=0.5, center_y=0.5)
            Box.add_widget(x)
            OpenButton = Button(text="Open", size_hint_x=0.3)
            OpenButton.bind(on_release=lambda x: App.get_running_app().root.ids.screen_IOTControl_id.loadPage(item))
            Box.add_widget(OpenButton)
            self.add_widget(Box)




class ScreenMain(Screen):
    pass


class Manager(ScreenManager):
    current = ObjectProperty()
    last_screen = ObjectProperty()
    splash_next = ObjectProperty()


class LunaApp(MDApp):

    def build(self):
        """This method returns the Manager class"""
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"  # "Purple", "Red"
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

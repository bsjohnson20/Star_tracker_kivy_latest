import logging

from IPy import IP
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Canvas
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore  # use for storing data
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton

settings_storage = JsonStore('settings.json')
devices_storage = JsonStore('devices.json')


# settings_storage.put("LunaDevice",ip="123.42.12",desc="Hello!",LastOnline=5245425)
# settings_storage.get("LunaDevice")


class ScreenWelcome(Screen):
    def generateScreen(self):
        pass


class ScreenAboutMe(Screen):
    pass

class IOT_toolbar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        # create boxlayout
        box = BoxLayout(orientation="horizontal")


        # create controls
        back = MDIconButton(text="back", on_press=self.back, icon="arrow-left")
        DoesNothing = MDIconButton(text="DoesNothing", on_press=lambda x: print("!"), icon="home")
        Settings = MDIconButton(text="Settings", on_press=self.settings)

        # add controls to box
        box.add_widget(back)
        box.add_widget(DoesNothing)
        box.add_widget(Settings)



        # log using logging module
        self.add_widget(box)
        logging.debug("Created toolbar")
        print('added toolbar')


    def back(self, *args):
        App.get_running_app().root.current = "ScreenHome"
        # debug log using logging module
        logging.debug("Going back to home screen")

    def settings(self, *args):
        # App.get_running_app().root.current = "ScreenSettings"
        # debug log using logging module
        logging.debug("Going to settings screen")


        # create boxlayout
        box = BoxLayout(orientation="vertical", spacing=10, padding=10, size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # add input for ip address
        box.add_widget(Label(text="IP Address:"))
        box.add_widget(TextInput(id="ip_id", multiline=False))

        # add input for device name
        box.add_widget(Label(text="Device Name:"))
        box.add_widget(TextInput(id="name", multiline=False))

        # add input for device description
        box.add_widget(Label(text="Device Description:"))
        box.add_widget(TextInput(id="desc", multiline=False))

        # add dropdown for device type
        box.add_widget(Label(text="Device Type:"))
        dropdown = DropDown()
        for index in range(10):
            btn = Button(text='Value %d' % index, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        mainbutton = Button(text='Hello', size_hint=(None, None))
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        box.add_widget(mainbutton)


class ScreenIOTControl(Screen):
    def loadPage(self, name, dev_type, **kwargs):
        # load the page for the device type and device name with the data and controls.
        App.get_running_app().root.current = 'ScreenIOTControl'
        # devices_storage[caller_name]
        print(f"name: {name}, dev_type: {dev_type}")

        # clear the boxlayout
        self.ids.iotcontrol_box.clear_widgets()
        # clear toolbar
        self.ids.toolbar_box.clear_widgets()




        # create boxlayout
        box = BoxLayout(orientation="vertical")

        # title label
        box.add_widget(Label(text="Device Controls", size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5}))

        # add the controls to the boxlayout in another container
        main_box = BoxLayout(orientation="vertical", spacing=10, padding=10, size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        main_box.add_widget(Label(text="Hello!"))
        main_box.add_widget(Label(text=name))
        main_box.add_widget(Label(text=devices_storage[name]["ip"]))
        main_box.add_widget(Label(text=devices_storage[name]["desc"]))
        main_box.add_widget(Label(text=devices_storage[name]["device_type"]))

        # set the size of the main box
        main_box.size_hint = (0.5, 0.5)
        main_box.pos_hint = {'center_x': 0.5, 'center_y': 0.5}


        # add the main box to the boxlayout
        self.ids.iotcontrol_box.add_widget(main_box)


        # add toolbar to root
        self.ids.toolbar_box.add_widget(IOT_toolbar())








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


class OpenerButton(MDIconButton):
    # set image to resources/plus.png
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = 'play'
        # increase icon size
        self.icon_size = "64dp"
        self.font_size = "64dp"


        
        


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
        print(devices_storage.count())
        for item in devices_storage:
            print(item)
            x = GridLayout(cols=2)
            # info labels
            name_lab = Label(text="name")
            name_lab.pos_hint = 0.3, 1
            desc_lab = Label(text="desc")
            desc_lab.pos_hint = 0.3, 1
            ip_lab = Label(text="ip")
            ip_lab.pos_hint = 0.3, 1
            type_lab = Label(text="type")
            type_lab.pos_hint = 0.3, 1

            # data labels
            dev_type = Label(text=devices_storage[item]['device_type'])
            dev_type.pos_hint = 0.3, 1
            desc_label = Label(text=devices_storage[item]['desc'])
            desc_label.pos_hint = 0.3, 1
            name_label = Label(text=item)
            name_label.pos_hint = 0.3, 1
            ip_label = Label(text=devices_storage[item]['ip'])
            ip_label.pos_hint = 0.3, 1


            # add labels
            x.add_widget(name_lab)
            x.add_widget(name_label)

            x.add_widget(desc_lab)
            x.add_widget(desc_label)

            x.add_widget(ip_lab)
            x.add_widget(ip_label)

            x.add_widget(type_lab)
            x.add_widget(dev_type)


            # create THE Box this'll contain labels and the buton to open the corresponding IOT panel
            Box = BoxLayout(size_hint_y=None)
            Box.add_widget(x)
            # clickable image
            BigButton = OpenerButton()
            BigButton.size_hint_x = 0.3
            print("BINDING TO "+item+" "+devices_storage[item]['device_type'])
            BigButton.bind(on_release=lambda x: App.get_running_app().root.ids.screen_IOTControl_id.loadPage(name_label.text, devices_storage[name_label.text]['device_type']))
            print(name_label.text)

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
        self.height = dp(64)
        # set orientation to horizontal
        self.orientation = 'horizontal'

        self.add_widget(AddButton())
        self.add_widget(HomeButton())
        self.add_widget(MeButton())
        # background color
        self.background_color = (1, 1, 1, 1)
        # update size on window resize
        self.size_hint = (1, 0.2)
        # add padding to half the width of root screen

    # function to update size on resize


def changeScreenMe(*args, **kwargs):
    App.get_running_app().root.current = 'ScreenAboutMe'
    App.get_running_app().root.last_screen = 'ScreenHome'


def changeScreenHome(*args, **kwargs):
    App.get_running_app().root.current = 'ScreenHome'


def changeScreenAdd(*args, **kwargs):
    App.get_running_app().root.current = 'ScreenAdd'
    App.get_running_app().root.last_screen = 'ScreenHome'


class HomeButton(MDIconButton):
    # set image to resources/plus.png
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = 'home'
        self.size_hint = (0.3, 1)
        self.icon_size = "64dp"
        # self.size = (50, 50)
        # root.manager.current = root.manager.last_screen
        #                     root.manager.last_screen = "ScreenAdd"

        # set bind to the button press to open the add screen

        self.on_release = changeScreenHome
        # scale image to height of root widget
        self.image_size = self.size

        




class AddButton(MDIconButton):
    # set image to resources/plus.png

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = 'view-grid-plus-outline'
        self.size_hint = (0.3, 1)
        self.icon_size = "64dp"
        # self.size = (50, 50)
        self.on_release = changeScreenAdd
        self.background = "black"
        print(self.size)


class MeButton(MDIconButton):
    # set image to resources/plus.png
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon_size = "64dp"
        self.icon = 'account'
        #self.source = 'resources/anonymous-person-icon-23.jpg'
        self.size_hint = (0.3, 1)
        # self.size = (50, 50)
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

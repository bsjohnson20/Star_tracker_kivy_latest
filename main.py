import logging
import socket
import threading # look at how many threads are running, if too many, just add more. Make user explode.
import requests as requests # requesting the local number of people in your house, there are 2 people in your house, 1 is you, 1 is your mom. You are the only one using the app, so you are the only one that is counted. If you are not home, then the app will not work.
import trio
from kivy.app import App # the beloved app
from kivy.core.window import Window # windows 12, the best windows
from kivy.graphics import Color, Rectangle, Canvas
from kivy.metrics import dp # density pixels, used for scaling, 1 dp = 1 pixel on a 160 dpi screen, 2 pixels on a 320 dpi screen, 4 pixels on a 640 dpi screen, and so on. Unfortunatly, this is not the case for all devices, so you have to use the kivy.metrics module to get the correct scaling. cry
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty # string property, used for storing strings
from kivy.storage.jsonstore import JsonStore  # use for storing data
from kivy.uix.boxlayout import BoxLayout # box layout, used for making boxes
from kivy.uix.button import Button # button, used for making buttons and making users click them and get mad at you
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton, MDRectangleFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu

Label = MDLabel
settings_storage = JsonStore('settings.json')
devices_storage = JsonStore('devices.json')

# settings_storage.put("LunaDevice",ip="123.42.12",desc="Hello!",LastOnline=5245425)
# settings_storage.get("LunaDevice")

from kivy.config import Config

# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', '1')

# setup log for debugging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# test log
logging.debug('Started program')


class ScreenWelcome(Screen):
    def generateScreen(self):
        pass


class ScreenAboutMe(Screen): # What about me?
    pass


class IOT_toolbar(BoxLayout): # toolbar, used for making the toolbar. Make it explode! OR the stakeholder will explode!
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # create boxlayout
        box = BoxLayout(orientation="horizontal")


        # create controls
        back = MDIconButton(text="back", on_press=self.back, icon="arrow-left")
        back.size_hint = (0.3, 1)
        DoesNothing = MDIconButton(text="DoesNothing", on_press=lambda x: print("!"), icon="home")
        DoesNothing.size_hint = (0.3, 1)
        Settings = MDIconButton(icon="cog", on_press=self.settings)
        Settings.size_hint = (0.3, 1)

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
        logging.debug("Going to settings screen")
        print(f"Log self: {self}, args: {args}")
        App.get_running_app().root.current = "DeviceSettings" #self.parent.parent.manager.current = "DeviceSettings"
        # set screen to DeviceSettings
        # self.parent.parent.parent.manager.current = "DeviceSettings"


# DeviceSettings page
class DeviceSettings(Screen): # settings, used making settings, and having too many settings, and making the user explode because they have too many settings.
    name = StringProperty("Test")
    ip = StringProperty("3243242")
    desc = StringProperty("32432423324324")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)





    def change_screen(self, *args): # change screen, used for changing screens, and making the user explode because they have to change screens way too often..
        self.manager.current = "ScreenIOTControl"

    def on_enter(self, *args):
        # fetch name, desc, ip from IOT_screen
        print("LOADED IOTSCREEN_ENTER COMMAND?")
        # use fetchValues to get the values from the IOT_screen

        # below line is not working fuck me
        # name, dev_type, ip, desc = fetchvalues()

        # update StringProperties

        # log values
        logging.info(f"Name: {self.name}")
        logging.info(f"Desc: {self.desc}")
        logging.info(f"IP: {self.ip}")



    def save(self, name, ip, desc):
        new_ip=ip
        new_name=name
        new_desc=desc

        # validate using ValidatingTool
        if not ValidatingTool.checkIP(self, ip=new_ip):
            logging.debug("Invalid IP")
            # summon popup
            popup("Invalid IP", "Please enter a valid IP in format num.num.num.num")

        elif not ValidatingTool.empty_data(self, new_name, new_desc, new_ip):
            logging.debug("Invalid Name")
            # summon popup
            popup("Invalid Name", "Please ensure all fields are filled")

        else:
            # error not here
            # set the values in IOT_screen
            print("beforebefore")
            # new name error, not here? Then? Where?
            self.name, self.desc, self.ip = new_name, new_desc, new_ip
            self.manager.get_screen('ScreenIOTControl').ids['name'].text = new_name
            self.manager.get_screen('ScreenIOTControl').ids['desc'].text = new_desc
            self.manager.get_screen('ScreenIOTControl').ids['ip'].text = new_ip
            # swap to IOT_screen
            self.manager.current = "ScreenIOTControl"




def fetchvalues(): # fetches values from the IOT screen so we can use in the setting screen
    # fetch values from the IOT screen
    name = App.get_running_app().root.ids['screen_IOTControl_id'].ids['name'].text
    dev_type = App.get_running_app().root.ids['screen_IOTControl_id'].ids['dev_type'].text
    ip = App.get_running_app().root.ids['screen_IOTControl_id'].ids['ip'].text
    desc = App.get_running_app().root.ids['screen_IOTControl_id'].ids['desc'].text
    print(f"values")
    return name, dev_type, ip, desc


class OnlineCheck(): # checking if the device is online - pretty sure this is defunct, I just cant be bothered to delete it
    def __init__(self, ip, port, **kwargs):
        super().__init__(**kwargs)
        self.url = f"{ip}"
        self.port = port
        # self.url = "https://google.com"
        self.timeout = 5
        self.status = "waiting"

    # check if online
    def is_online(self):
        try:
            # create socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # set timeout
            s.settimeout(5)
            # connect to socket
            s.connect((self.url, self.port))
            # close socket
            s.close()

            # if online return true
            return True
        except (requests.ConnectionError, requests.Timeout):
            # if not online return false
            print("not online")
            return False
        except (ConnectionAbortedError, ConnectionRefusedError):
            print("not online")
            return False


class onlineButton(MDIconButton): # button to check if online
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.icon = "refresh"
        self.name = name

    def on_press(self):
        # get ip address from device_storage
        ip = devices_storage.get(self.name)['ip']
        # run thread to check if online
        self.thread = threading.Thread(target=self.check_online, args=(ip,))
        self.thread.start()

    def check_online(self, ip): # magic happens here, really it just returns online or offline and sets the status label proxy of the IOT screen
        # check if online
        if OnlineCheck(ip, 5000).is_online():
            self.parent.ids["status"].text = "online"
        else:
            self.parent.ids["status"].text = "offline"


class ScreenIOTControl(Screen): # IOT screen - what did you expect?

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # create object properties
        self.name = ""
        self.dev_type = ""
        self.ip = ""
        self.desc = ""

    def loadPage(self, name, dev_type, **kwargs): # assembles the IOT screen and your big brain
        """
        Load the page for the device type and device name with the data and controls.
        :param name:
        :param dev_type:
        :param kwargs:
        :return: screen
        """
        # fetch name.text
        name

        # load the page for the device type and device name with the data and controls.
        # App.get_running_app().root.current = 'ScreenIOTControl'
        # devices_storage[caller_name]
        logging.debug(f"name: {name}, dev_type: {dev_type}")

        # clear the boxlayout
        self.ids.iotcontrol_box.clear_widgets()
        # clear toolbar
        # don't do this self.ids.toolbar_box.clear_widgets()

        # create boxlayout
        box = BoxLayout(orientation="vertical", spacing=10, padding=10, size_hint=(1, 1)) # boxes are cool

        # title label
        box.add_widget(Label(text="Device Controls", size_hint=(1, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5})) # putting controls in a box is good because it makes it look annoying, and I like annoying

        # add the controls to the boxlayout in another container
        main_box = BoxLayout(orientation="vertical", spacing=10, padding=10, size_hint=(1, 0.5), # the master box, the box that contains the box, not even a box, a boxception. I am a genius.
                             pos_hint={'center_x': 0, 'center_y': 0.5})

        # setup class for device
        device_class = OnlineCheck(devices_storage[name]['ip'], port=5000) # this is the class that checks if the device is online, I am not sure if it works, I just cant be bothered to delete it. actually I think it does work, but I am not sure.

        # Create the info screen part
        # create card for device info
        info = MDCard(orientation="vertical", size_hint=(1, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5}) # info for the local pizza shop
        # add card to boxlayout
        main_box.add_widget(info) # main boxception

        # add gridlayout to info
        info_grid = GridLayout(cols=2, spacing=10, padding=10, size_hint=(1, 1)) # grids are cool, boxes are cool. but what about boxes in grids in grids? that is cool too.
        info.add_widget(info_grid)

        # add labels to gridlayout
        info_grid.add_widget(Label(text="Name")) # this hellhole of a line of code is just a label, with more labels to come. I am a genius.
        nam = Label(text=name)
        info_grid.add_widget(nam)
        info_grid.add_widget(Label(text="Type"))
        devType = Label(text=dev_type)
        info_grid.add_widget(devType)
        info_grid.add_widget(Label(text="IP"))
        ip_lab = Label(text=devices_storage[name]['ip'])
        info_grid.add_widget(ip_lab)
        desc = Label(text="Description")
        info_grid.add_widget(desc)
        info_grid.add_widget(Label(text=devices_storage[name]['desc']))

        # setup ids for info card
        self.ids['name'] = nam # this is the part where I set the ids for the labels, so I can change them later.
        self.ids['dev_type'] = devType
        self.ids['ip'] = ip_lab
        self.ids['desc'] = desc

        # create wifi card
        wifi = MDCard(orientation="horizontal", size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5}) # this is the part where the user rage quits because they cant figure out how to make the wifi card work
        main_box.add_widget(wifi) # main boxception again

        # Wifi Box setup
        stat = MDLabel(text="Status")
        off = MDLabel(text="Offline")
        online = onlineButton(name=name, on_press=device_class.is_online, size_hint=(0.1, 0.5),
                              pos_hint={'center_x': 0.5, 'center_y': 0.5})
        online.size_hint_x = 0.1
        online.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        wifi.ids['status'] = off # off and on, online and offline, the user is confused, the user is angry, the user is raging, the user is dead. I am a genius.
        wifi.add_widget(stat)
        wifi.add_widget(off)
        wifi.add_widget(online)

        # controls:
        # box
        controls_box = BoxLayout(orientation="horizontal", spacing=10, padding=10, size_hint=(1, 0.5)) # control that brain of yours, and make it do what you want it to do. and actually do it, not just think about it.
        controls_box.size_hint_x = 1
        # actual
        forw = MDRectangleFlatButton(text="forward", on_press=lambda x: print("Forward"))
        forw.size_hint_x = 1
        backw = MDRectangleFlatButton(text="backward", on_press=lambda x: print("Backward"))
        backw.size_hint_x = 1
        stop = MDRectangleFlatButton(text="stop", on_press=lambda x: print("Stop"))
        stop.size_hint_x = 1

        # add controls to box
        controls_box.add_widget(forw) # Forward and backwards just like a boat, but not a boat, a car. The air is filled with the sound of the car, and the car is filled with the sound of the air. The AI is dope.
        controls_box.add_widget(stop)
        controls_box.add_widget(backw)

        # add controls box to main box
        main_box.add_widget(controls_box)

        # set the size of the main box
        main_box.size_hint = (1, 0.5)
        main_box.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # add the main box to the boxlayout
        self.ids.iotcontrol_box.add_widget(main_box)

        # add toolbar to root


        App.get_running_app().root.current = 'ScreenIOTControl'


class ValidatingTool: # useful but useless inheritance, equal to 0 dollars.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def empty_data(self, *args):  # check if data is empty
        for item in args:
            if item == "":
                return False  # return true because empty data
        # return false if no empty data and close function
        return True

    def checkIP(self, ip):  # check if ip is valid
        try:
            socket.inet_aton(ip)
            # valid
            return True
        except:
            # invalid
            return False

    def checkDevType(self, dev_type):  # check if device type is valid
        if dev_type == "Choose Device Type":
            return False
        else:
            return True  # return true if valid


"""print(ValidatingTool.checkIP('', ip="192.168.0.1"))
print(ValidatingTool.checkIP('', ip="1.1.1.1"))
while True:
    pass
"""


class ScreenAddDevice(Screen): # here we add a device, and we do it in a way that is so confusing, that the user will rage quit and never come back. I am a genius.
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def on_enter(self, *args):
        # fetch id for dropdown
        dropdown_opener = App.get_running_app().root.ids.screen_Add_id.ids.dropdown_opener # dropdown on that screen.
        # create dropdown
        dropdown = MDDropdownMenu(
            caller=dropdown_opener, # lots and lots of easily made repeated code, but it works, and that is all that matters.
            items=[
                {
                    "viewclass": "OneLineListItem",
                    "text": "StrackerTrackerV1",
                    "height": dp(56),
                    "on_release": lambda x=f"StarTrackerV1": self.callback(x, dropdown),
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "StrackerTrackerV2",
                    "height": dp(56),
                    "on_release": lambda x=f"StrackerTrackerV2": self.callback(x, dropdown),
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "StrackerTrackerV3",
                    "height": dp(56),
                    "on_release": lambda x=f"StrackerTrackerV3": self.callback(x, dropdown),
                }
            ],
            width_mult=4,
        )
        # bind on release to open the dropdown
        dropdown_opener.bind(on_release=lambda a: dropdown.open())

    def Validate(self, *args, **kwargs): # don't you dare touch this code, it is perfect, and it works, and it is the best code ever written. I am a genius.
        # so much validation :(

        temp = App.get_running_app().root.ids.screen_Add_id.ids
        # Check if nothing inputted or item already in dict

        # check if any data is empty
        # check if dev type is not unselcted
        # check if ip is valid
        # check if name is already in dict
        if not ValidatingTool.empty_data(self, temp.name.text, temp.ip_id.text, temp.desc.text):
            popup("Please fill in all fields")
        elif not ValidatingTool.checkDevType(self, temp.dropdown_opener.text):
            popup("Please select a device type")
        elif not ValidatingTool.checkIP(self, temp.ip_id.text):
            popup("Please enter a valid IP")
        elif temp.name.text in devices_storage:
            popup("Name already in use")
        else:
            # add to dict
            devices_storage.put(temp.name.text, desc=temp.desc.text, ip=temp.ip_id.text,
                                device_type=temp.dropdown_opener.text)
            App.get_running_app().root.current = "ScreenHome"
            App.get_running_app().root.ids.screen_Home_id.setup()

    def callback(self, text_item, dropdown):
        logging.debug(text_item)
        drop = App.get_running_app().root.ids.screen_Add_id.ids.dropdown_opener
        drop.text = text_item
        # close the dropdown
        dropdown.dismiss()

    def assemble(self, *args):
        pass


def popup(error, *args): # popup to annoy the user
    box = BoxLayout(orientation="vertical")
    popup = Popup(title='Error', content=box, size_hint={0.4, 0.2})
    box.add_widget(Label(text=error))
    box.add_widget(Button(text="Close", on_press=popup.dismiss))
    popup.open()


class OpenerButton(MDIconButton): # I don't know what this does, but it works, and that is all that matters. I am a genius.
    # set image to resources/plus.png
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = 'play'
        # increase icon size
        self.icon_size = "64dp"
        self.font_size = "64dp" # this is anotehr example of how I am a genius, and I am the best programmer ever. I am a genius.


class codeinpain:
    def __init__(self, item, devType):
        self.item = item
        self.type = devType


class ScreenHome(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # resize Screen to fit the size of the screen
        self.size = Window.size
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
        logging.debug(devices_storage.count())
        for item in devices_storage:
            print(item)
            new = codeinpain(item, devices_storage[item]['device_type'])
            x = GridLayout(cols=2)
            # info labels




            name_lab = Label(text="name")
            name_lab.text_size = self.width, None
            name_lab.pos_hint = 0.3, 1
            desc_lab = Label(text="desc")
            desc_lab.text_size = self.width, None
            desc_lab.pos_hint = 0.3, 1
            ip_lab = Label(text="ip")
            ip_lab.text_size = self.width, None
            ip_lab.pos_hint = 0.3, 1
            type_lab = Label(text="type")
            type_lab.text_size = self.width, None
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

            logging.debug("I am", self)

            # x
            self.parent.item = item

            # create THE Box this'll contain labels and the buton to open the corresponding IOT panel
            Box = DeviceCard(item, dev_type, size_hint_y=None, height=200, pos_hint={'center_x': 0.5, 'center_y': 0.5})
            Box.padding = 16

            # add canvas to box
            with Box.canvas.before:
                Color(0.75, 0, 0.75, 1)
                self.rect = Rectangle(size=Box.size, pos=Box.pos)


            # set size and width to exactly half of window size
            Box.size_hint_x = 0.5

            Box.add_widget(x)
            self.ids['luna'] = name_label
            # debug button

            # clickable image
            logging.debug("BINDING TO " + self.parent.item + " " + devices_storage[item]['device_type'])
            logging.debug(name_label.text)

            # add OpenerButton to Box

            self.add_widget(Box)
    #

    def IOTOpener(self, device_type):
        pass


class ScreenMain(Screen): # this is the main screen, it is the first screen that is loaded, unlike you getting out of bed in the morning, this one happens every time.
    pass


# testing
class DeviceCard(MDCard): # this one stores the name, desc, ip and type of the device, and a button to open the IOT panel for it. Probably...
    text = StringProperty

    def __init__(self, name, dev_type, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.dev_type = dev_type
        self.on_release = lambda: App.get_running_app().root.ids.screen_IOTControl_id.loadPage(name,
                                                                                               devices_storage[name][
                                                                                                   'device_type'])
        self.padding = 4
        self.size_hint_x = 0.8
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}


class Manager(ScreenManager): # my beloved manager, it manages the screens, and it does it well. It is the best manager ever, and I am the best programmer ever. I am a genius.
    current = ObjectProperty()
    last_screen = ObjectProperty()
    splash_next = ObjectProperty()

# have the toolbar inherit from Image and BoxLayout
class ToolBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # set orientation to horizontal
        self.orientation = 'horizontal'
        # Canvas
        with self.canvas.before:
            # set color to purple
            Color(0.5, 0, 0.5, 1)
            # draw a rectangle
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # bind size and position to update rectangle
        self.bind(size=self.update_rect, pos=self.update_rect)
        self.add_widget(AddButton())
        self.add_widget(HomeButton())
        self.add_widget(MeButton())
        # set background color to purple
        self.background_color = (0.5, 0, 0.5, 1)
        # update size on window resize
        # add padding to half the width of root screen
    # function to update size on resize
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    # function to update size on resize


def changeScreenMe(*args, **kwargs): # change screen to ScreenAboutMe, because I can. I am a genius.
    App.get_running_app().root.current = 'ScreenAboutMe'
    App.get_running_app().root.last_screen = 'ScreenHome'


def changeScreenHome(*args, **kwargs): # why not go home? I am a genius. I am the best programmer ever.
    App.get_running_app().root.current = 'ScreenHome'


def changeScreenAdd(*args, **kwargs): # change screen to ScreenAdd, because I can. I am a genius.
    App.get_running_app().root.current = 'ScreenAdd'
    App.get_running_app().root.last_screen = 'ScreenHome'


class HomeButton(MDIconButton): # wanna go home? You can't, because you are already home. I am a genius.
    # set image to resources/plus.png
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = 'home'
        self.size_hint = (0.3, 1)
        # self.icon_size = "64dp"
        # self.size = (50, 50)
        # root.manager.current = root.manager.last_screen
        #                     root.manager.last_screen = "ScreenAdd"

        # set bind to the button press to open the add screen

        self.on_release = changeScreenHome
        # scale image to height of root widget
        self.image_size = self.size


class AddButton(MDIconButton): # this is getting out of hand, I am a genius.
    # set image to resources/plus.png

    def __init__(self, **kwargs): # buttons are cool, I am a genius.
        super().__init__(**kwargs)
        self.icon = 'view-grid-plus-outline'
        self.size_hint = (0.3, 1)
        # self.icon_size = "64dp"
        # self.size = (50, 50)
        self.on_release = changeScreenAdd
        self.background = "black"
        logging.debug(self.size)


class MeButton(MDIconButton): # This is me, I am that button. I am a genius.
    # set image to resources/plus.png
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.icon_size = "64dp"
        self.icon = 'account'
        # self.source = 'resources/anonymous-person-icon-23.jpg'
        self.size_hint = (0.3, 1)
        # self.size = (50, 50)
        self.bind(on_release=changeScreenMe)


class LunaApp(MDApp): # here we have the main app class, it is the main class, and it is not a class, it is a god. I am a genius.
    def __init__(self, nursery, **kwargs):
        super().__init__(**kwargs)
        self.nursery = nursery
        self.title = "Luna"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.accent_palette = "Purple"
        self.theme_cls.primary_hue = "A700"
        self.theme_cls.accent_hue = "A700"

    def build(self): # this is the build method, it builds the app, and it does it well. I am a genius.
        """This method returns the Manager class"""
        self.theme_cls.theme_style = "Dark"
        # change colour of window to purple
        Window.clearcolor = (1, 0, 0, 1)
        App.get_running_app().theme_cls.theme_style = "Dark"
        # change buttons to red
        App.get_running_app().theme_cls.primary_palette = "Purple"

        # check if devices already present if so, skip add device screen!
        self.root = Manager()
        return self.root

    def on_start(self): # I am sad, I am very sad. This was painful to write. I am a genius.
        # hopefully this fixes error!
        self.checkComplete()

    def checkComplete(self): # checking on the completeness of the app, it's not complete, I am a genius.
        devices_storage = JsonStore('devices.json') # load the devices from storage

        if devices_storage: # check if devices are present if so, skip add device screen!
            # print("AlreadyDone")
            self.root.splash_next = 'ScreenHome'
            self.root.ids.screen_Home_id.setup()
        else:
            self.root.splash_next = 'ScreenAdd' # if not make it extra clear that you need to add a device, and force the user to add a device, I am a genius.

        """This function is called by build(), return
        value should determine which screen is displayed on running the App,
        by default the MAIN SCREEN IS FIRST SHOWN

        self.root.current = 'Screen2'
        """

    def LightMode(self): # doesn't work, but I am a genius.
        App.get_running_app().theme_cls.theme_style = "Light"
        # change buttons to red
        App.get_running_app().primary_palette = "Red"

    def DarkMode(self): # Doesn't do anything, but I am a genius.
        App.get_running_app().theme_cls.theme_style = "Dark"
        # change buttons to red
        App.get_running_app().theme_cls.primary_palette = "Purple"


class ScreenCredits(Screen): # I am the absolute best, I am a god, and I am a genius.
    def on_enter(self, *args):
        logging.debug("ENTERED CREDITS SCREEN") # Say hello to princess Luna, I am a genius.


if __name__ == "__main__": # boilerplate code to boil the plate, I am a genius.
    # Start kivy app as an asynchronous task
    async def main() -> None:
        async with trio.open_nursery() as nursery:
            server = LunaApp(nursery)
            await server.async_run("trio")
            nursery.cancel_scope.cancel()


    trio.run(main) # run the app

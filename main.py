# version 1.0.0


import os
import threading  # look at how many threads are running, if too many, just add more. Make user explode.
from typing import Union

import trio
from kivy.app import App  # the beloved app
from kivy.core.window import Window  # Windows 12, the best windows
from kivy.logger import Logger
from kivy.metrics import \
    dp  # density pixels, used for scaling, 1 dp = 1 pixel on a 160 dpi screen, 2 pixels on a 320 dpi screen,
# 4 pixels on a 640 dpi screen, and so on. Unfortunately, this is not the case for all devices, so you have to use the
# kivy.metrics module to get the correct scaling. cry
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty
from kivy.properties import StringProperty  # string property, used for storing strings
from kivy.storage.jsonstore import JsonStore  # use for storing data
from kivy.uix.boxlayout import BoxLayout  # box layout, used for making boxes
from kivy.uix.button import Button  # button, used for making buttons and making users click them and get mad at you
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton, MDRectangleFlatButton
from kivymd.uix.card import MDCard, MDCardSwipe
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDColorPicker
from kivymd.uix.slider import MDSlider

# start removing this request library, it might be causing the crash. I mean, I'm not sure, but it might be.

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


# test log
print('Started program')


class TitleLabel(BoxLayout):
    text = StringProperty("")
    color = ListProperty([1, 0, 0.5, 1])


class DeviceDataPage(
    Widget):  # inputs for device data. Standardised to cause less confusion. Actually, it causes more confusion. Just kidding, it causes even more confusion.
    pass


class ScreenWelcome(Screen):
    def generateScreen(self):
        pass


class ScreenAboutMe(Screen):  # What about me?
    def open_dialog(self):
        # open popup telling user they have saved their theme successfully
        pass


class IOT_toolbar(BoxLayout):  # toolbar, used for making the toolbar. Make it explode! OR the stakeholder will explode!
    dev_name = StringProperty("Test")
    ip = StringProperty("3243242")
    address = StringProperty("32432423324324")

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
        print("Created toolbar")
        print('added toolbar')

    def back(self, *args):
        App.get_running_app().root.current = "ScreenHome"
        # debug log using logging module
        print("Going back to home screen")

    def settings(self, *args):
        print("Going to settings screen")
        print(f"Log self: {self}, args: {args}")
        App.get_running_app().root.current = "DeviceSettings"  # self.parent.parent.manager.current = "DeviceSettings"
        # set screen to DeviceSettings
        # self.parent.parent.parent.manager.current = "DeviceSettings"


# DeviceSettings page
class DeviceSettings(
    Screen):  # settings, used making settings, and having too many settings, and making the user explode because they have too many settings.
    dev_name = StringProperty("")
    ip = StringProperty("")
    desc = StringProperty("")
    dev_type = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def change_screen(self,
                      *args):  # change screen, used for changing screens, and making the user explode because they have to change screens way too often..
        self.manager.current = "ScreenIOTControl"

    def on_enter(self, *args):
        # fetch name, desc, ip from IOT_screen
        print("LOADED IOTSCREEN_ENTER COMMAND?")
        # use fetchValues to get the values from the IOT_screen

        # below line is not working fuck me
        # name, dev_type, ip, desc = fetchvalues()

        # update StringProperties

        # log values
        print(f"Name: {self.dev_name}")
        print(f"Desc: {self.desc}")
        print(f"IP: {self.ip}")

    def save(self, dev_name, ip, desc):
        new_ip = ip
        new_name = dev_name
        new_desc = desc

        # validate using ValidatingTool
        if not ValidatingTool.checkIP(self, ip=new_ip):
            print("Invalid IP")
            # summon popup
            popup("Invalid IP", "Please enter a valid IP in format num.num.num.num")

        elif not ValidatingTool.empty_data(self, new_name, new_desc, new_ip):
            print("Invalid Name")
            # summon popup
            popup("Invalid Name", "Please ensure all fields are filled")

        # check if name exists in database:
        print("test")
        if not(dev_name in devices_storage) or (new_name in devices_storage): # checks if it already exists, if it's the one stored then allow, if it's changing into one in there then don't allow.
            print("Device already in database\n choose a new name")
            popup("Already in database\n choose a new name")


        else:
            # error not here
            # set the values in IOT_screen
            print("beforebefore")
            # new name error, not here? Then? Where?
            self.dev_name, self.desc, self.ip = new_name, new_desc, new_ip
            old_name = self.manager.get_screen('ScreenIOTControl').ids['name'].text
            self.manager.get_screen('ScreenIOTControl').ids['name'].text = new_name
            self.manager.get_screen('ScreenIOTControl').ids['desc'].text = new_desc
            self.manager.get_screen('ScreenIOTControl').ids['ip'].text = new_ip
            self.dev_type = self.manager.get_screen('ScreenIOTControl').ids['dev_type'].text

            # delete old key in device_storage
            devices_storage.delete(old_name)
            # add new key in device_storage
            devices_storage.put(new_name, ip=new_ip, desc=new_desc, device_type=self.dev_type)

            # swap to IOT_screen
            self.manager.current = "ScreenIOTControl"


def fetchvalues():  # fetches values from the IOT screen so we can use in the setting screen
    # fetch values from the IOT screen
    dev_name = App.get_running_app().root.ids['screen_IOTControl_id'].ids['name'].text
    dev_type = App.get_running_app().root.ids['screen_IOTControl_id'].ids['dev_type'].text
    ip = App.get_running_app().root.ids['screen_IOTControl_id'].ids['ip'].text
    desc = App.get_running_app().root.ids['screen_IOTControl_id'].ids['desc'].text
    print(f"values")
    return dev_name, dev_type, ip, desc


class OnlineCheck():  # I want to use Kivy's builtin function, but I haven't implemented it yet.
    def __init__(self, ip, port, **kwargs):
        super().__init__(**kwargs)
        self.url = f"{ip}"
        self.port = port
        # self.url = "https://google.com"
        self.timeout = 5
        self.status = "waiting"
        # use logging module to log
        Logger.info(f"OnlineCheck: loaded CheckSystem; ip = {self.url}")

    # check if online
    def is_online(self):
        Logger.info(f"Checking if device isOnline")
        # use ping in os module
        response = os.system("ping -n 1 " + self.url)
        # and then check the response...
        if response == 0:
            self.status = "online"
            return True
        else:
            self.status = "offline"
            return False


class onlineButton(MDIconButton):  # button to check if online
    def __init__(self, dev_name, **kwargs):
        super().__init__(**kwargs)
        self.icon = "refresh"
        self.dev_name = dev_name

    def on_press(self):
        # get ip address from device_storage
        ip = devices_storage.get(self.dev_name)['ip']
        # run thread to check if online
        self.thread = threading.Thread(target=self.check_online, args=(ip,))
        self.thread.start()

    def check_online(self,
                     ip):
        # check if online
        if OnlineCheck(ip, 5000).is_online():
            self.parent.ids["status"].text = "online"
            Logger.info("online")
        else:
            self.parent.ids["status"].text = "offline"
            Logger.info("offline")


class ScreenIOTControl(Screen):  # screen for controlling IOT devices

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # create object properties
        self.dev_name = ""
        self.dev_type = ""
        self.ip = ""
        self.desc = ""

    def sendCommand(self, ip, command, *args, **kwargs):  # sends command to device
        # use requests to send command to device with format http://ip:port/api?command=command+"
        print(self.ip)
        result = UrlRequest(f"http://{self.ip}/api?command={command}", on_success=self.success, on_failure=self.failure,
                            on_error=self.error, on_redirect=self.redirect)
        if result.result is None:
            # popup
            popup("Error", "Unable to connect to device, please check  IP address and try again. Or your device may not have replied", "Or your device is unreachable due to not being on the same network")

    def success(self, *args, **kwargs):  # success callback
        Logger.info("Success!")
        # create popup
        popup("Success", "Command sent successfully")

    def failure(self, *args, **kwargs):  # failure callback
        Logger.info("Failure!")
        # create popup
        popup("Failure", "Unable to connect to device, please check  IP address and try again",
              "Or your device may be offline", "Or your device is unreachable")

    def error(self, *args, **kwargs):  # error callback
        Logger.info("Error!")
        # load popup
        popup("Error", "Unable to connect to device, please check  IP address and try again",
              "Or your device may be offline", "Or your device is unreachable due to not being on the same network")

    def redirect(self, *args, **kwargs):  # redirect callback
        Logger.info("Redirect!")

    def sendSpeed(self, ip, speed, *args, **kwargs):  # sends speed to device
        # use requests to send command to device with format http://ip:port/api?speed=speed"
        print(self.ip)
        try:
            result = UrlRequest(f"http://{self.ip}/api?speed={speed}", on_success=self.success, on_failure=self.failure,
                                on_error=self.error, on_redirect=self.redirect)
            Logger.info(result.result)
        except ConnectionError:
            print("Unable to send, as no connection!")

    def loadPage(self, dev_name, dev_type, **kwargs):  # assembles the IOT screen and your big brain
        """
        Load the page for the device type and device dev_name with the data and controls.
        :param dev_name:
        :param dev_type:
        :param kwargs:
        :return: screen
        """
        # fetch dev_name.text
        print("LOADED IOTSCREEN_LOADPAGE COMMAND?")

        # load the page for the device type and device dev_name with the data and controls.
        # App.get_running_app().root.current = 'ScreenIOTControl'
        # devices_storage[caller_dev_name]
        print(f"dev_name: {dev_name}, dev_type: {dev_type}")

        # clear the boxlayout
        self.ids.iotcontrol_box.clear_widgets()
        # clear toolbar
        # don't do this self.ids.toolbar_box.clear_widgets()

        # create boxlayout
        box = BoxLayout(orientation="vertical", spacing=10, padding=10, size_hint=(1, 1))  # boxes are cool

        # title label
        box.add_widget(Label(text="Device Controls", size_hint=(1, 0.5), pos_hint={'center_x': 0.5,
                                                                                   'center_y': 0.5}))  # putting controls in a box is good because it makes it look annoying, and I like annoying

        # add the controls to the boxlayout in another container
        main_box = BoxLayout(orientation="vertical", spacing=10, padding=10, size_hint=(1, 0.5),
                             # the master box, the box that contains the box, not even a box, a boxception. I am a genius.
                             pos_hint={'center_x': 0, 'center_y': 0.5})

        # setup class for device
        device_class = OnlineCheck(devices_storage[dev_name]['ip'],
                                   port=5000)  # this is the class that checks if the device is online, I am not sure if it works, I just cant be bothered to delete it. actually I think it does work, but I am not sure.

        # Create the info screen part
        # create card for device info
        info = MDCard(orientation="vertical", size_hint=(1, 0.5),
                      pos_hint={'center_x': 0.5, 'center_y': 0.5})  # info for the local pizza shop
        # add card to boxlayout
        main_box.add_widget(info)  # main boxception

        # add gridlayout to info
        info_grid = GridLayout(cols=2, spacing=10, padding=10, size_hint=(
            1, 1))  # grids are cool, boxes are cool. but what about boxes in grids in grids? that is cool too.
        info.add_widget(info_grid)

        # add labels to gridlayout
        info_grid.add_widget(Label(
            text="Name"))  # this hellhole of a line of code is just a label, with more labels to come. I am a genius.
        nam = Label(text=dev_name)
        info_grid.add_widget(nam)
        info_grid.add_widget(Label(text="Type"))
        devType = Label(text=dev_type)
        info_grid.add_widget(devType)
        info_grid.add_widget(Label(text="IP"))
        ip_lab = Label(text=devices_storage[dev_name]['ip'])
        info_grid.add_widget(ip_lab)
        desc = Label(text="Description")
        info_grid.add_widget(desc)
        info_grid.add_widget(Label(text=devices_storage[dev_name]['desc']))

        # setup ids for info card
        self.ids['name'] = nam  # this is the part where I set the ids for the labels, so I can change them later.
        self.ids['dev_type'] = devType
        self.ids['ip'] = ip_lab
        self.ids['desc'] = desc

        # create wifi card
        wifi = MDCard(orientation="horizontal", size_hint=(1, 0.1), pos_hint={'center_x': 0.5,
                                                                              'center_y': 0.5})  # this is the part where the user rage quits because they cant figure out how to make the wifi card work
        main_box.add_widget(wifi)  # main boxception again

        # Wifi Box setup
        stat = MDLabel(text="Status")
        off = MDLabel(text="Offline")
        online = onlineButton(dev_name=dev_name, on_press=device_class.is_online, size_hint=(0.1, 0.5),
                              pos_hint={'center_x': 0.5, 'center_y': 0.5})
        online.size_hint_x = 0.1
        online.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        wifi.ids[
            'status'] = off  # off and on, online and offline, the user is confused, the user is angry, the user is raging, the user is dead. I am a genius.
        wifi.add_widget(stat)
        wifi.add_widget(off)
        wifi.add_widget(online)

        # controls:
        # box
        controls_box = BoxLayout(orientation="horizontal", spacing=10, padding=10, size_hint=(1,
                                                                                              0.5))  # control that brain of yours, and make it do what you want it to do. and actually do it, not just think about it.
        controls_box.size_hint_x = 1
        # actual
        forw = MDRectangleFlatButton(text="forward", on_press=lambda x: self.sendCommand(self.ip, "STEPFORW"))
        forw.size_hint_x = 1
        backw = MDRectangleFlatButton(text="backward", on_press=lambda x: self.sendCommand(self.ip, "STEPBACK"))
        backw.size_hint_x = 1
        stop = MDRectangleFlatButton(text="stop", on_press=lambda x: self.sendCommand(self.ip, "STEPSTOP"))
        stop.size_hint_x = 1

        # add controls to box
        controls_box.add_widget(
            forw)  # Forward and backwards just like a boat, but not a boat, a car. The air is filled with the sound
        # of the car, and the car is filled with the sound of the air. The AI is dope.
        controls_box.add_widget(stop)
        controls_box.add_widget(backw)

        # add controls box to main box
        main_box.add_widget(controls_box)

        # Boxlayout to add speed slider
        speed_box = BoxLayout(orientation="horizontal", spacing=10, padding=10, size_hint=(1, 0.2))
        speed_box.size_hint_x = 1

        # add speed slider
        speed_slider = MDSlider(min=0, max=100, value=50, size_hint=(1, 0.5),
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # set range of slider to 0-200 with decimal places
        speed_slider.range = (0, 200)
        speed_slider.value = 100
        speed_slider.precision = 1

        speed_slider.size_hint_x = 1
        speed_slider.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        speed_box.add_widget(speed_slider)

        # give id to speed slider
        self.ids['speed_slider'] = speed_slider

        # Button to set speed
        speed_button = MDRectangleFlatButton(text="Set Speed")

        # on press, send command to set speed
        speed_button.on_press = lambda: self.sendSpeed(self.ip, self.ids['speed_slider'].value)

        speed_button.size_hint_x = 1
        speed_button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        speed_box.add_widget(speed_button)

        # add speed box to main box
        main_box.add_widget(speed_box)

        # set the size of the main box
        main_box.size_hint = (1, 0.5)
        main_box.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # add the main box to the boxlayout
        self.ids.iotcontrol_box.add_widget(main_box)

        # add toolbar to root
        # update manager ids
        self.manager.dev_name = dev_name
        self.manager.dev_type = dev_type
        self.manager.ip = devices_storage[dev_name]['ip']
        self.manager.desc = devices_storage[dev_name]['desc']

        self.ip = devices_storage[dev_name]['ip']
        print("added ip")

        App.get_running_app().root.current = 'ScreenIOTControl'


class ValidatingTool:  # useful but useless inheritance, equal to 0 dollars.
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
            ip = ip.split(".")
            for i in ip:
                if int(i) > 255:
                    return False
                elif int(i) < 0:
                    return False
                elif len(ip) != 4:
                    return False
                elif ip[0] == "0":
                    return False
                else:
                    pass
                    # valid
                    return True
        except:
            # invalid
            return False

    def checkDevType(self, dev_type):  # check if device type is valid
        if dev_type == "Device Types":
            return False
        else:
            return True  # return true if valid


"""print(ValidatingTool.checkIP('', ip="192.168.0.1"))
print(ValidatingTool.checkIP('', ip="1.1.1.1"))
while True:
    pass
"""


class ScreenAddDevice(
    Screen):  # here we add a device, and we do it in a way that is so confusing, that the user will rage quit and
    # never come back. I am a genius.
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def on_enter(self, *args):
        # fetch id for dropdown
        dropdown_opener = App.get_running_app().root.ids.screen_Add_id.ids.dropdown_opener  # dropdown on that screen.
        # create dropdown
        dropdown = MDDropdownMenu(
            caller=dropdown_opener,
            # lots and lots of easily made repeated code, but it works, and that is all that matters.
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

    def Validate(self, *args,
                 **kwargs):  # don't you dare touch this code, it is perfect, and it works, and it is the best code
        # ever written. I am a genius.
        # so much validation :(

        temp = App.get_running_app().root.ids.screen_Add_id.ids
        # Check if nothing inputted or item already in dict

        # check if any data is empty
        # check if dev type is not unselcted
        # check if ip is valid
        # check if name is already in dict
        if not ValidatingTool.empty_data(self, temp.dev_name.text, temp.ip_id.text, temp.description.text):
            popup("Please fill in all fields")
        elif not ValidatingTool.checkDevType(self, temp.dropdown_opener.text):
            popup("Please select a device type")
        elif not ValidatingTool.checkIP(self, temp.ip_id.text):
            popup("Please enter a valid IP")
        elif temp.dev_name.text in devices_storage:
            popup("Name already in use")
        else:
            # add to dict
            devices_storage.put(temp.dev_name.text, desc=temp.description.text, ip=temp.ip_id.text,
                                device_type=temp.dropdown_opener.text)
            App.get_running_app().root.current = "ScreenHome"
            App.get_running_app().root.ids.screen_Home_id.setup()

    def callback(self, text_item, dropdown):
        print(text_item)
        drop = App.get_running_app().root.ids.screen_Add_id.ids.dropdown_opener
        drop.text = text_item
        # close the dropdown
        dropdown.dismiss()

    def assemble(self, *args):
        pass


def popup(error, *args):  # popup to annoy the user
    box = BoxLayout(orientation="vertical")
    popup = Popup(title='Error', content=box, size_hint=(None, None), size=(400, 400), auto_dismiss=False)
    box.add_widget(Label(text=error))
    for i in args:
        box.add_widget(Label(text=i))
    box.add_widget(Button(text="Close", on_press=popup.dismiss))
    popup.open()


class OpenerButton(
    MDIconButton):  # I don't know what this does, but it works, and that is all that matters. I am a genius.
    # set image to resources/plus.png
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = 'play'
        # increase icon size
        self.icon_size = "64dp"
        self.font_size = "64dp"  # this is anotehr example of how I am a genius, and I am the best programmer ever. I am a genius.


class codeinpain:
    def __init__(self, item, devType):
        self.item = item
        self.type = devType


class Deletethis(MDIconButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = 'delete'
        self.icon_size = "64dp"
        self.font_size = "64dp"

    def removeFromDatabase(self, dev_name):
        # fetch name to delete
        # delete from database
        devices_storage.delete(dev_name)


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
        add_grid = App.get_running_app().root.ids.screen_Home_id.ids.add_here

        for child in [child for child in
                      add_grid.children]:  # clear screen - this lets us update the screen as well! - no this isn't a lazy workaround so I don't have to append instead... and write a new builder
            add_grid.remove_widget(child)
        print(devices_storage.count())
        for item in devices_storage:
            print(item)
            new = codeinpain(item, devices_storage[item]['device_type'])
            add_grid.parent.item = item

            # create THE Box this'll contain labels and the buton to open the corresponding IOT panel
            Box = DeviceCard(dev_name=item, ip=devices_storage[item]['ip'], desc=devices_storage[item]['desc'],
                             device=devices_storage[item]['device_type'])
            # add color to Box
            # make it pretty
            # it didn't work :(, I wish It did. Then I could be a genius.
            Box.color = (0.5, 0, 0.5, 1)
            Box.padding = 16
            # loop through attributes of box

            # add Box to screen
            add_grid.add_widget(Box)

            # set size and width to exactly half of window size
            Box.size_hint_x = 1
            print(Box.ids)
            # clickable image
            print("BINDING TO " + add_grid.parent.item + " " + devices_storage[item]['device_type'])

    # update rectangle position and size
    def _update_rect(self, instance, value, *args):
        self.rect.size = instance.size

    def IOTOpener(self, device_type):
        pass


class ScreenMain(
    Screen):  # this is the main screen, it is the first screen that is loaded, unlike you getting out of bed in the morning, this one happens every time.
    pass


# testing
class DeviceCard(
    MDCardSwipe):  # this one stores the name, desc, ip and type of the device, and a button to open the IOT panel for it. Probably...
    dev_name = StringProperty()
    device = StringProperty()
    ip = StringProperty()
    desc = StringProperty()

    def __init__(self, dev_name, ip, desc, device, **kwargs):
        super().__init__(**kwargs)
        self.dev_name = dev_name
        self.device = device
        self.ip = ip
        self.desc = desc
        self.on_release = lambda: App.get_running_app().root.ids.screen_IOTControl_id.loadPage(dev_name,
                                                                                               devices_storage[
                                                                                                   dev_name][
                                                                                                   'device_type'])

    def open(self):
        App.get_running_app().root.ids.screen_IOTControl_id.loadPage(self.dev_name,
                                                                     devices_storage[self.dev_name][
                                                                         'device_type'])
        print("OPENING")


class Manager(
    ScreenManager):  # my beloved manager, it manages the screens, and it does it well. It is the best manager ever, and I am the best programmer ever. I am a genius.
    current = ObjectProperty()
    last_screen = ObjectProperty()
    splash_next = ObjectProperty()

    # terrible workaround to get the screen to update, I hate but hopefully this will work.
    dev_name = StringProperty()
    ip = StringProperty()
    desc = StringProperty()
    device = StringProperty()


# have the toolbar inherit from Image and BoxLayout
class ToolBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # set orientation to horizontal
        self.orientation = 'horizontal'
        # Canvas
        print(f"ids: {self.ids}")
        add_to = self
        # bind size and position to update rectangle

        # update size on window resize
        # add padding to half the width of root screen

    # function to update size on resize

    # function to update size on resize


def changeScreenMe(*args, **kwargs):  # change screen to ScreenAboutMe, because I can. I am a genius.
    App.get_running_app().root.current = 'ScreenAboutMe'
    App.get_running_app().root.last_screen = 'ScreenHome'


def changeScreenHome(*args, **kwargs):  # why not go home? I am a genius. I am the best programmer ever.
    App.get_running_app().root.current = 'ScreenHome'


def changeScreenAdd(*args, **kwargs):  # change screen to ScreenAdd, because I can. I am a genius.
    App.get_running_app().root.current = 'ScreenAdd'
    App.get_running_app().root.last_screen = 'ScreenHome'


class HomeButton(MDIconButton):  # Home button, does nothing, purely aesthetic.
    # set image to resources/plus.png
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # set icon to house
        self.icon = 'home'

        # set to third of total area, and full height
        self.size_hint = (0.3, 1)
        # change to home
        self.on_release = changeScreenHome
        # scale image to height of root widget
        self.image_size = self.size


class AddButton(MDIconButton):  # add button for new devices, actually does something.
    # set image to resources/plus.png

    def __init__(self, **kwargs):  # buttons are cool, I am a genius.
        super().__init__(**kwargs)
        self.icon = 'view-grid-plus-outline'
        self.size_hint = (0.3, 1)
        # self.icon_size = "64dp"
        # self.size = (50, 50)
        self.on_release = changeScreenAdd
        self.background = "black"
        print(self.size)


class MeButton(MDIconButton):  # This is me, it's a me, Mario!
    # set image to resources/plus.png
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.icon_size = "64dp"
        self.icon = 'cog'
        # self.source = 'resources/anonymous-person-icon-23.jpg'
        self.size_hint = (0.3, 1)
        # self.size = (50, 50)
        self.bind(on_release=changeScreenMe)


class LunaApp(
    MDApp):  # here we have the main app class, it is the main class, and it is not a class, it is a god. I am a genius.
    allowThemeSaving = BooleanProperty()

    def __init__(self, nursery, **kwargs):
        super().__init__(**kwargs)
        self.nursery = nursery

        # theming, overcomplicated, and I don't know if it's all necessary, but it works.
        self.title = "Luna"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.accent_palette = "Purple"
        self.theme_cls.primary_hue = "A700"
        self.theme_cls.accent_hue = "A700"
        self.theme_primary = [0.5, 0, 0.5, 1]
        self.allowThemeSaving = False # PREVENT THEME FROM SAVING, naughty saving gets you no theme saving.
        try:
            self.theme_primary = settings_storage.get('theme')['args']
            print(self.theme_primary)
        except KeyError: # if theme is not saved, save a default theme.
            # save default theme
            settings_storage.put('theme', args=self.theme_primary)

    def build(self):  # this is the build method, it builds the app, and it does it well. I am a genius.
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

    def on_start(self):  # I am sad, I am very sad. This was painful to write. I am a genius.
        # hopefully this fixes error!
        self.checkComplete()

    def checkComplete(self):  # checking on the completeness of the app, it's not complete, I am a genius.
        devices_storage = JsonStore('devices.json')  # load the devices from storage

        if devices_storage:  # check if devices are present if so, skip add device screen!
            # print("AlreadyDone")
            self.root.splash_next = 'ScreenHome'
            self.root.ids.screen_Home_id.setup()
        else:
            self.root.splash_next = 'ScreenAdd'  # if not make it extra clear that you need to add a device, and force the user to add a device, I am a genius.

        """This function is called by build(), return
        value should determine which screen is displayed on running the App,
        by default the MAIN SCREEN IS FIRST SHOWN

        self.root.current = 'Screen2'
        """

    def open_color_picker(self): # open color picker, brings up a color picker for theme.
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color,
            on_release=self.get_selected_color
        )

    def update_color(self, color: list) -> None: # fetch updated color, and update theme.
        print(f"Setting color to {color}, args are {color}")
        self.theme_primary = color

        # save theme setting to settings.json
        settings_storage.put('theme', args=color)

    def get_selected_color( # get selected color, and update theme.
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''

        print(f"Selected color is {selected_color}") # debug
        # close color picker
        instance_color_picker.dismiss()
        self.update_color(selected_color[:-1] + [1])
        popup("You have successfully saved your theme!", "")

    def on_select_color(self, instance_gradient_tab, color: list) -> None: # cool.
        '''Called when a gradient image is clicked.'''


# defunct code
# set color
# def set_color(self, color, *args):
#   if self.allowThemeSaving:
#      print(f"Setting color to {color}, args are {args}")
#     self.theme_primary = args
#
#           # save theme setting to settings.json
#          settings_storage.put('theme', args=args[0])
#     else: # we shouldn't be saving the theme yet
#        print("Attempted to save theme, but not allowed to save theme yet")


class ScreenCredits(Screen):  # I am the absolute best, I am a god, and I am a genius.
    def on_enter(self, *args):
        print("ENTERED CREDITS SCREEN")  # Say hello to princess Luna, I am a genius.


if __name__ == "__main__":  # boilerplate code to boil the plate, I am a genius.
    # Start kivy app as an asynchronous task
    async def main() -> None:
        async with trio.open_nursery() as nursery:
            server = LunaApp(nursery)
            await server.async_run("trio")
            nursery.cancel_scope.cancel()


    trio.run(main)  # run the app

# if you noticed the comments, I let CoPilot write them, I am a genius. YUp, I am a genius. I am the best program. I am the best programmer and I am the best pet. Even though I am a cat, I can still be the best pet. I am a genius. I love you, I am a genius.


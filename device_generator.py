import json
import random

class DeviceGenerator:
    # we need to generate devices in the pattern {"Luna": {"desc": "1231", "ip": "1.1.1.1", "device_type": "Device Types"}}
    def __init__(self):
        self.device_types = ['StarTracker1', "StarTracker2","StarTracker3"]
        self.device_descs = list(range(0,400))
        self.names = ''

    def generate_names(self):
        for i in range(0,500):
            self.names.append('Luna'+str(i))

    def generate_devices(self, count):
        devices = {}
        for i in range(0,count):
            devices['luna'+str(i)]= {
                "desc": str(self.device_descs[i]),
                "ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "device_type": random.choice(self.device_types)
            }

        return devices

    def write_to_file(self, devices):
        with open('devices.json', 'w') as f:
            json.dump(devices, f)


# calling the class
device_generator = DeviceGenerator()
devices = device_generator.generate_devices(25)
device_generator.write_to_file(devices)

# output
print(devices)
import netmiko
import textfsm
import os
from getpass import getpass
from pprint import pprint


HOSTNAME = input("Hostname:  ")
uname = input("Username:  ")
pword = getpass("Password:  ")
interface = input("interface  ")
device = {
    "device_type": "cisco_ios",
    "host": HOSTNAME,
    "username": uname,
    "password": pword,
}
net_connect = netmiko.ConnectHandler(**device)
portsec = net_connect.send_command(f"show port-security interface gig {interface}")
WALL = ""
for line in portsec:
    line = line.strip()
    WALL += "\n"
    WALL += line
template_file = os.path.join(os.getcwd(), "ps.textfsm")
with open(template_file) as template:
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseText(portsec)
parsed_data = [dict(zip(fsm.header, row)) for row in result]
pprint(parsed_data)
for x in parsed_data:
    if x['VIOLATION_COUNT'] == '0':
        print('no violations on this port')

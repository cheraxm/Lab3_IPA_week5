from netmiko import ConnectHandler
import os

device = {
    'device_type': 'cisco_ios',
    'host': '172.31.115.4', 
    'username': 'admin',
    'password': 'cisco',
}

with open('config/172.31.115.4-exercise-nat.txt') as f:
    config_commands = f.read().splitlines()

with ConnectHandler(**device) as net_connect:
    output = net_connect.send_config_set(config_commands)

print("Configuration applied successfully")

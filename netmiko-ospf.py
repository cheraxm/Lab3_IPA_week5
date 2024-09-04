from netmiko import ConnectHandler
import re

device_ip = ['172.31.115.3', '172.31.115.4']
username = 'admin'
password = 'cisco'

commands = [['router ospf 1 vrf control-data',
                 'network 192.168.1.0 0.0.0.255 area 0',
                 'network 192.168.2.0 0.0.0.255 area 0',
                 'exit'],
                 ['router ospf 1 vrf control-data',
                  'network 192.168.2.0 0.0.0.255 area 0',
                  'network 192.168.3.0 0.0.0.255 area 0',
                  'default-information originate',
                  'exit']]

counter = 0
r1_output = ""
r2_output = ""

for ip in device_ip:
    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': username,
        'password': password
    }
    net_connect = ConnectHandler(**device)
    output = net_connect.send_config_set(commands[counter])
    router_output = net_connect.send_command('sh ip route vrf control-data')
    if counter == 0:
        r1_output = router_output
    else:
        r2_output = router_output

    counter += 1

def check_default_route(output):
    return "0.0.0.0/0" in output or "Gateway of last resort is" in output and "not set" not in output

def check_network(output, network):
    return re.search(rf"{network}", output) is not None

if check_default_route(r1_output):
    print("test routing R1 passes: default route found on R1")

if check_network(r1_output, "192.168.3.0/24"):
    print("test routing R1 passes: 192.168.3.0/24 found on R1")

if check_network(r2_output, "192.168.1.0/24"):
    print("test routing R2 passes: 192.168.1.0/24 found on R2")
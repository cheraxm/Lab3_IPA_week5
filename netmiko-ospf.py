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
    ospf_route_pattern = r'(O|S\*)\s+(\d+\.\d+\.\d+\.\d+/\d+)'

    matches = re.findall(ospf_route_pattern, ospf_route_pattern)

    # Define router identifiers for output
    router_identifiers = {
        '192.168.1.0/24': 'R2',
        '192.168.3.0/24': 'R2'
    }

    # Print results for OSPF routes
    for protocol, network_address in matches:
        if protocol == 'S*':
            router = 'R1'
            print(f"test routing {router} passes: default route found on {router}")
        else:
            router = router_identifiers.get(network_address, 'R1')  # Default to R1 if not found
            print(f"test routing {router} passes: {network_address} found on {router}")

    counter += 1
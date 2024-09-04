import paramiko
import time
import re

device_ip = "172.31.115.4"
USERNAME = 'admin'
KEY_PATH = '/home/chuti/.ssh/id_rsa'

interfaces = [[
    b"int g0/1\n", 
    b"vrf forwarding control-data\n", 
    b"ip address 192.168.2.2 255.255.255.0\n", 
    b"no shut\n", 
    b"exit\n"
], [
    b"int g0/2\n", 
    b"vrf forwarding control-data\n", 
    b"ip address 192.168.3.1 255.255.255.0\n", 
    b"no shut\n", 
    b"exit\n"
], [
    b"int g0/3\n", 
    b"vrf forwarding control-data\n", 
    b"ip address dhcp\n", 
    b"no shut\n", 
    b"exit\n"
]]

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(
    hostname=device_ip,
    username=USERNAME,
    disabled_algorithms={"pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]},
    pkey=paramiko.RSAKey.from_private_key_file("/home/chuti/.ssh/id_rsa"),
)
print("Connection successful")
session = client.invoke_shell()
for interface in interfaces:
    for command in interface:
        session.send(command)

session.send(b"sh ip route vrf control-data\n")
time.sleep(10)
output = session.recv(65535).decode('utf-8')
output = output.split('\n')
for line in output[1:]:
    match = re.search(r'(\S+)\s+(\S+)\s+(\S+)', line)
    if match:
        interface, ip, vrf = match.groups()
        print(f"{ip} of {interface} is assigned to VRF {vrf}")
import paramiko
import logging
import os
import time

# Setup logging
logging.basicConfig(level=logging.DEBUG)
paramiko.util.log_to_file('paramiko.log')

# Define constants
USERNAME = 'admin'
KEY_PATH = '/home/chuti/.ssh/adminR2_id_rsa'
devices_ip = "172.31.115.4"

# Initialize SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"Connecting to {devices_ip} with key {KEY_PATH}")
    client.connect(hostname=devices_ip, username=USERNAME, key_filename=KEY_PATH, allow_agent=False, look_for_keys=False)
    print("Connection successful")

    # Define command sequences
    interfaceg0_1 = [
        "int g0/1", 
        "vrf forwarding control-data", 
        "ip address 192.168.2.2 255.255.255.0", 
        "no shut", 
        "exit"
    ]

    interfaceg0_2 = [
        "int g0/2", 
        "vrf forwarding control-data", 
        "ip address 192.168.3.1 255.255.255.0", 
        "no shut", 
        "exit"
    ]

    interfaceg0_3 = [
        "int g0/3", 
        "vrf forwarding control-data", 
        "ip address dhcp", 
        "no shut", 
        "exit"
    ]

    def execute_commands(commands):
        for command in commands:
            print(f"Executing {command}")
            stdin, stdout, stderr = client.exec_command(command)
            print(stdout.read().decode())
            print("Errors:")
            print(stderr.read().decode())
            time.sleep(1)

    # Execute commands
    execute_commands(interfaceg0_1)
    execute_commands(interfaceg0_2)
    execute_commands(interfaceg0_3)

except paramiko.AuthenticationException:
    print("Authentication failed. Check your username, password, and key.")
except paramiko.SSHException as e:
    print(f"SSH exception: {e}")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    client.close()

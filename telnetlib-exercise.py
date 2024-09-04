import getpass
import telnetlib
import time

host = "172.31.115.3"
user = input("Enter username: ")
password = getpass.getpass()

try:
    tn = telnetlib.Telnet(host, 23, 5)
    
    def send_command(command, delay=2):
        tn.write(command + b"\n")
        time.sleep(delay)


    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    time.sleep(1)

    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    time.sleep(1)

    commands = [
        b"conf t",
        b"int g0/1",
        b"vrf forwarding control-data",
        b"ip address 192.168.1.1 255.255.255.0",
        b"no shut",
        b"exit",
        b"int g0/2",
        b"vrf forwarding control-data",
        b"ip address 192.168.2.1 255.255.255.0",
        b"no shut",
        b"exit",
        b"exit",
        b"sh ip vrf interfaces control-data",
        b"exit"
    ]

    for command in commands:
        if command == b"ip address 192.168.1.1 255.255.255.0":
            print("192.168.1.1 of Gi0/1 is assigned to VRF control-data")
        if command == b"ip address 192.168.2.1 255.255.255.0":
            print("192.168.2.1 of Gi0/2 is assigned to VRF control-data")
        send_command(command, delay=2) 
    send_command(b"")

except BrokenPipeError:
    print("Broken pipe error: The connection was closed unexpectedly.")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    try:
        tn.close()
    except Exception as e:
        print(f"Failed to close Telnet connection: {e}")

import getpass
import telnetlib
import time

host = "172.31.115.3"
user = input("Enter username: ")
password = getpass.getpass()

try:
    tn = telnetlib.Telnet(host, 23, 5)
    
    # Function to send commands and read responses
    def send_command(command, delay=2):
        tn.write(command + b"\n")
        time.sleep(delay)
        response = tn.read_very_eager()  # Read immediately
        print(response.decode('ascii'))
    
    # Read and send username
    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    time.sleep(1)

    # Read and send password
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    time.sleep(1)

    # Send configuration commands
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
        send_command(command, delay=2)  # Adjust delay as needed

    # Ensure there's a newline after the last command
    send_command(b"")  # Ensures we get all the output

except BrokenPipeError:
    print("Broken pipe error: The connection was closed unexpectedly.")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    try:
        tn.close()
    except Exception as e:
        print(f"Failed to close Telnet connection: {e}")

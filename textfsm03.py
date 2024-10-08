import sys
import re
from netmiko import ConnectHandler
from ntc_templates.parse import parse_output

def connect_to_router():
    device = {
        'device_type': 'cisco_ios',
        'host': '172.31.115.4',
        'username': 'admin',
        'password': 'cisco',
    }
    return ConnectHandler(**device)

def normalize_interface_name(name):
    name = name.lower()

    if re.match(r'^(g|gi|gig|giga|gigab|gigabi|gigabit|gigabite|gigabitet|gigabiteth|gigabitether|gigabitethernet|lo|l|loop|loopba|loopback|n|nvi|nv)[0-9/]+$', name):
        interface_type = re.match(r'^[a-z]+', name).group()
        interface_number = name[len(interface_type):]

        if interface_type.startswith('g'):
            return f'GigabitEthernet{interface_number}'
        elif interface_type.startswith('l'):
            return f'Loopback{interface_number}'
        elif interface_type.startswith('n'):
            return f'NVI{interface_number}'

def get_interface_info(conn, interface_name):
    output = conn.send_command("show ip int brief")
    parsed_output = parse_output(platform="cisco_ios", command="show ip interface brief", data=output)
    matching_interface = None
    normalized_input = normalize_interface_name(interface_name)

    for interface in parsed_output:
        if interface['interface'] == normalized_input:
            matching_interface = interface
            break
    return matching_interface

def main():
    if len (sys.argv) < 2:
        print("Usage: python3 textfsm03.py <interface_name>")
        sys.exit(1)
    if len(sys.argv[1]) == 1 or (len(sys.argv[1]) == 1 and sys.argv[1].isdigit()):
        print("Wrong interface name format!")
        sys.exit(1)
    if len(sys.argv) != 2 and sys.argv[1] is not None and sys.argv[2] is not None:
        if "g" in sys.argv[1] or "lo" in sys.argv[1] or "nvi" in sys.argv[1] and "0123456789" in sys.argv[2] and "/" in sys.argv[2]:
            print(f'Do you mean interface "{sys.argv[1]}{sys.argv[2]}"?')
            sys.exit(1)
        else:
            print("Usage: python3 textfsm03.py <interface_name>")
            sys.exit(1)
    interface_name = sys.argv[1]
    interface_name = interface_name.strip('"')
    interface_name = interface_name.replace(" ", "")

    try:
        conn = connect_to_router()
        interface = get_interface_info(conn, interface_name)

        if interface is None:
            print("No interface found")
        else:
            print(f"Interface: {interface['interface']}")
            print(f"IP address = {interface['ip_address']}")
            print(f"Status = {interface['status']}")
            print()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.disconnect()

if __name__ == "__main__":
    main()
                                                                                                                             
import pexpect
import os

PROMPT = '#'
IP = '172.31.115.3'
USERNAME = os.environ.get('TELNET_USER')
PASSWORD = os.environ.get('TELNET_PASSWORD')
# result = b''

child = pexpect.spawn('telnet ' + IP)
child.expect('Username:')
child.sendline(USERNAME)
child.expect('Password:')
child.sendline(PASSWORD)
child.expect(PROMPT)
child.sendline("conf t")
child.expect(PROMPT)
child.sendline("int loopback 0")
child.expect(PROMPT)
child.sendline("ip add 172.16.1.1 255.255.255.255")
child.expect(PROMPT)
child.sendline("do sh ip int br")
child.expect(PROMPT)
# result += child.before
child.sendline("exit")
child.expect(PROMPT)
# print(result)
# print()
# print(result.decode('UTF-8'))
child.sendline('exit')
print("Loopback0 172.16.1.1 is created on 172.31.115.3")


# result2 = b''
child2 = pexpect.spawn('telnet 172.31.115.4')
child2.expect('Username:')
child2.sendline(USERNAME)
child2.expect('Password:')
child2.sendline(PASSWORD)
child2.expect(PROMPT)
child2.sendline("conf t")
child2.expect(PROMPT)
child2.sendline("int loopback 0")
child2.expect(PROMPT)
child2.sendline("ip add 172.16.2.2 255.255.255.255")
child2.expect(PROMPT)
child2.sendline("do sh ip int br")
child2.expect(PROMPT)
# result2 += child2.before
child2.sendline("exit")
child2.expect(PROMPT)
# print(result2)
# print()
# print(result2.decode('UTF-8'))
child2.sendline('exit')
print("Loopback0 172.16.2.2 is created on 172.31.115.4")
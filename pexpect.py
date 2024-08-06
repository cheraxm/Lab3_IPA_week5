import pexpect

PROMPT = '#'
IP = '172.31.115.3'
USERNAME = 'admin'
PASSWORD = 'cisco'

child = pexpect.spawn('telnet ' + IP)
child.expect('Username')
child.sendline(USERNAME)
child.expect('Password')
child.sendline(PASSWORD)
child.expect(PROMPT)
child.sendline("int loopback0")
child.expect(PROMPT)
child.sendline("ip add 172.16.1.1 255.255.255.255")
result = child.before
print(result)
print()
print(result.decode('UTF-8'))
child.sendline('exit')
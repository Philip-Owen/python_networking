import pexpect

devices = {'L3-SW2': {'prompt': 'L3-SW2', 'ip': '10.25.1.11'},
           'L3-SW3': {'prompt': 'L3-SW3', 'ip': '10.25.1.12'}}
username = 'cisco'
password = 'cisco'

for device in devices.keys():
    device_prompt = devices[device]['prompt']
    child = pexpect.spawn('telnet ' + devices[device]['ip'])
    child.expect('Username:')
    child.sendline(username)
    child.expect('Password:')
    child.sendline(password)
    child.expect(device_prompt)
    child.sendline('show version | i V')
    child.expect(device_prompt)
    print(child.before)
    child.sendline('exit')

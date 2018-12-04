import getpass
from pexpect import pxssh

devices = {'R1': {'prompt': 'R1', 'ip': '10.25.1.1'},
           'L3-SW1': {'prompt': 'L3-SW1', 'ip': '10.25.1.10'}}
commands = ['term length 0', 'show version', 'show run']

username = input('Username: ')
password = getpass.getpass('Password: ')

# Loop devices
for device in devices.keys():
    outputFileName = device + '_output_pexpectSSH.txt'
    device_propmt = devices[device]['prompt']
    child = pxssh.pxssh()
    child.login(devices[device]['ip'], username.strip(),
                password.strip(), auto_prompt_reset=False)
    with open('output/' + outputFileName, 'wb') as f:
        # Loop commands
        for command in commands:
            child.sendline(command)
            child.expect(device_propmt)
            f.write(child.before)

    child.logout()

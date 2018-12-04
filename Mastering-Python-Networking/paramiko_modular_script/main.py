import paramiko
import getpass
import time
import json

# load devices from devices.json
with open('devices.json', 'r') as f:
    devices = json.load(f)

# load commands from commands.txt
with open('commands.txt', 'r') as f:
    commands = [line for line in f.readlines()]

username = input('Username: ')
password = getpass.getpass('Password: ')

max_buffer = 65535


def clear_buffer(connection):
    if connection.recv_ready():
        return connection.recv(max_buffer)


# Loop devices.json
for device in devices.keys():
    outputFileName = device + '_output.txt'
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(devices[device]['ip'], username=username,
                       password=password, look_for_keys=False, allow_agent=False)
    new_connection = connection.invoke_shell()
    output = clear_buffer(new_connection)
    time.sleep(2)
    new_connection.send("terminal length 0\n")
    output = clear_buffer(new_connection)
    # write files to output/hostname*_output.txt
    with open('output/' + outputFileName, 'wb') as f:
      # Loop commands.txt
        for command in commands:
            new_connection.send(command)
            time.sleep(2)
            output = new_connection.recv(max_buffer)
            print(output)
            f.write(output)

    new_connection.close()

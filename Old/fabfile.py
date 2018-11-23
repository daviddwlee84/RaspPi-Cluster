from fabric import task
from fabric import Connection

#############################
#       User Setting        #
#############################

hosts = [
    'pi@192.168.1.100',
    'pi@192.168.1.114',
    'pi@192.168.1.115',
    'pi@192.168.1.116',
]

piPassword = 'raspberry'

##############################

@task
def CMD(ctx, command):
    print("Sending commend")
    for host in hosts:
        result = Connection(host, connect_kwargs={'password': piPassword}).run(command, hide=True)
        msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
        print(msg.format(result))

@task
def hello(ctx):
    print("Hello motherfucker")

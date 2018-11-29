# Connection Setting Example

## Four nodes Raspberry Pi cluster

```py
# === Connection Settings === #

NUM_NODES = 4

# Host IP
HOSTS_IP = [
    '192.168.1.109', # Master
    '192.168.1.101', # Slave1
    '192.168.1.102', # Slave2
    '192.168.1.103', # Slave3
]

# Hostname
slavenames = ['slave%i' % (i) for i in range(1, NUM_NODES)]
HOSTNAMES = ['master'] + slavenames

# Default user and password
USER = 'pi'
PASSWORD = 'raspberry'

# Default SSH Private Key path
# if you're using server you've already generate key for it
DEFAULT_SSHKEY = f'{TEMP_FILES}/id_rsa'

# Connection mode
# USE connection_mode.IP MODE BEFORE YOU SETUP HOSTNAME
# OR MODIFY 'master' ABOVE TO 'raspberrypi' (WHICH IS DEFAULT HOSTNAME FOR RASPBERRY PI)
# IF YOU ONLY RUN ON SINGLE NODE
CONN_MODE = connection_mode.HOSTNAME
# =========================== #
```

## One node Raspberry Pi cluster

(assume you want to keep original raspberrypi hostname)

```py
# === Connection Settings === #

NUM_NODES = 1

# Host IP
HOSTS_IP = [
    '192.168.1.109' # Master
]

# Hostname
HOSTNAMES = ['raspberrypi']

# Default user and password
USER = 'pi'
PASSWORD = 'raspberry'

# Default SSH Private Key path
# if you're using server you've already generate key for it
DEFAULT_SSHKEY = f'{TEMP_FILES}/id_rsa'

# Connection mode
# USE connection_mode.IP MODE BEFORE YOU SETUP HOSTNAME
# OR MODIFY 'master' ABOVE TO 'raspberrypi' (WHICH IS DEFAULT HOSTNAME FOR RASPBERRY PI)
# IF YOU ONLY RUN ON SINGLE NODE
CONN_MODE = connection_mode.HOSTNAME
# =========================== #
```

## Local/Remote Debian server

```py
# === Connection Settings === #

NUM_NODES = 1

# Host IP
HOSTS_IP = [
    '140.118.456.789', # Remote Master IP
]

# Hostname
slavenames = ['slave%i' % (i) for i in range(1, NUM_NODES)]
HOSTNAMES = ['master'] + slavenames

# Default user and password
USER = 'remoteuser'
PASSWORD = 'remotepassword'

# Default SSH Private Key path
# if you're using server you've already generate key for it
DEFAULT_SSHKEY = f'{TEMP_FILES}/id_rsa'

# Connection mode
# USE connection_mode.IP MODE BEFORE YOU SETUP HOSTNAME
# OR MODIFY 'master' ABOVE TO 'raspberrypi' (WHICH IS DEFAULT HOSTNAME FOR RASPBERRY PI)
# IF YOU ONLY RUN ON SINGLE NODE
CONN_MODE = connection_mode.IP
# =========================== #
```

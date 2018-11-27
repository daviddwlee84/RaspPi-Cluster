## fabric
from fabric import task
from fabric import Config
# Connection
from fabric import Connection, ThreadingGroup

## Invoke
from invoke import Responder

# util
import os
from os.path import expanduser # home dir
import getpass # password input
from enum import Enum

class connection_mode(Enum):
    IP = True
    HOSTNAME = False

#############################
#       User Setting        #
#############################

# === Connection Settings === #

NUM_NODES = 4

# Host IP
HOSTS_IP = [
    '192.168.1.109', # Master
    '192.168.1.101',
    '192.168.1.102',
    '192.168.1.103',
]

# Hostname
slavenames = ['slave%i' % (i) for i in range(1, NUM_NODES)]
HOSTNAMES = ['master'] + slavenames

# Default user and password
USER = 'pi'
PASSWORD = 'raspberry'

CONN_MODE = connection_mode.HOSTNAME # Connection mode
# =========================== #

REMOTE_UPLOAD = os.path.join('/home', USER, 'Downloads')

# === Hadoop === #
HADOOP_VERSION = '3.1.1'
HADOOP_MIRROR = f'http://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-{HADOOP_VERSION}/hadoop-{HADOOP_VERSION}.tar.gz'

HADOOP_GROUP = 'hadoop' # Hadoop group name
HADOOP_USER = 'hduser' # Hadoop user name
HADOOP_PASSWORD = 'hadoop' # Hadoop user password

######### Some process #######
# generally you don't need to modify things here

# File path
FILE_PATH = './Files' # configure files
TEMP_FILES = './temp_files' # file download, generated ssh key etc.

# Hadoop
HADOOP_FOLDER = 'hadoop-%s' % (HADOOP_VERSION,)
HADOOP_TARFILE = 'hadoop-%s.tar.gz' % (HADOOP_VERSION,)
HADOOP_APACHE_PATH = '/hadoop/common/hadoop-%s/%s' % (HADOOP_VERSION, HADOOP_TARFILE)
HADOOP_INSTALL = os.path.join('/opt', 'hadoop-%s' % (HADOOP_VERSION,))

#############################
#   Global Fabric Object    #
#   and Important Settings  #
#############################

# Hostname
def getHosts(user=USER, mode=connection_mode.IP):
    """
    Return hosts by either IP or Hostname
    """
    if mode == connection_mode.IP:
        # Add user to host
        hosts = list(map(lambda host: user + '@' + host, HOSTS_IP))
    elif mode == connection_mode.HOSTNAME:
        hosts = list(map(lambda hostname: user + '@' + hostname + '.local', HOSTNAMES))
    else:
        print("Unknown mode...")
    return hosts

# for sudo privilege
Configure = Config(overrides={'sudo': {'password': PASSWORD}})

# Parallel Group
Group = ThreadingGroup(*getHosts(mode=CONN_MODE), connect_kwargs={'password': PASSWORD}, config=Configure)

#############################
#       Helper Function     #
#############################

def connect(node_num, user=USER, password=PASSWORD, conn_mode=CONN_MODE, configure=Configure):
    """
    Get Single Conneciton to node
    """
    return Connection(getHosts(user=user, mode=conn_mode)[int(node_num)], connect_kwargs={'password': password}, config=configure)

#############################

### General usage
@task
def node_ls(ctx):
    """
    List nodes IP and Hostname
    """
    print('Node list:')
    print(getHosts(mode=connection_mode.IP))
    print(getHosts(mode=connection_mode.HOSTNAME))

@task(help={'command': "Command you want to sent to host", 'verbose': "Verbose output", 'node-num': "Node number of HOSTS list"})
def CMD(ctx, command, verbose=False, node_num=-1):
    """
    Run command on all nodes in serial order
    """
    if int(node_num) == -1:
        # Run command on all nodes
        if verbose:
            print("Sending commend")
        for connection in Group:
            result = connection.run(command, hide=True)
            msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
            if verbose:
                print(msg.format(result))
    elif NUM_NODES > int(node_num) >= 0:
        # Run command on specific node
        connection = connect(node_num)
        if verbose:
            print("Executing command on", connection)
        connection.run(command, pty=verbose)
    else:
        print('No such node.')    
        node_ls(ctx)

@task(help={'command': "Command you want to sent to host in parallel", 'verbose': "Verbose output"})
def CMD_parallel(ctx, command, verbose=False):
    """
    Execute command on all nodes in parallel
    """
    results = Group.run(command, hide=True)
    if verbose:
        for connection, result in results.items():
            print("{0.host}: {1.stdout}".format(connection, result))

@task(help={'filepath': "Path to file in local", 'destination': "Remote destination (directory)", 'permission': "Use superuser to move file", 'verbose': "Verbose output", 'node-num': "Node number of HOSTS list"})
def uploadfile(ctx, filepath, destination=REMOTE_UPLOAD, permission=False, verbose=False, node_num=-1):
    """
    Copy local file to remote
    """
    # Define helper function
    def simple_upload(dest):
        if int(node_num) == -1:
            # Run command on all nodes
            for connection in Group:
                if connection.run('test -f %s' % os.path.join(dest, os.path.basename(filepath)), warn=True).failed:
                    if verbose:
                        print("Connect to", connection)
                        print("Copying file %s to %s" % (filepath, dest))
                    connection.put(filepath, remote=dest)
                else:
                    if verbose:
                        print("File already exist")
        elif NUM_NODES > int(node_num) >= 0:
            # Run command on specific node
            connection = connect(node_num)
            if connection.run('test -f %s' % os.path.join(dest, os.path.basename(filepath)), warn=True).failed:
                if verbose:
                    print("Connect to", connection)
                    print("Copying file %s to %s" % (filepath, dest))
                connection.put(filepath, remote=dest)
            else:
                if verbose:
                    print("File already exist")
        else:
            print('No such node.')    
            node_ls(ctx)

    # Upload file
    if permission:
        simple_upload(REMOTE_UPLOAD)
        if verbose:
            print("Moving all file from %s to %s" % (os.path.join(REMOTE_UPLOAD, os.path.basename(filepath)), destination))
        CMD_parallel(ctx, 'sudo mv %s %s' % (os.path.join(REMOTE_UPLOAD, os.path.basename(filepath)), destination))
    else:
        try:
            simple_upload(destination)        
        except PermissionError:
            print("Your destination need superuser privilege, try using -p flag!")

@task(help={'node-num': "Node number of HOSTS list", 'private-key': "Path to private key"})
def ssh_connect(ctx, node_num, private_key=f'{TEMP_FILES}/id_rsa'):
    """
    Connect to specific node using ssh private key 
    """    
    private_key = expanduser(private_key) # expand ~ to actual route
    if not os.path.isfile(private_key):
        print("Can't find private key at", private_key)
    else:
        print('ssh -i %s %s' % (private_key, getHosts(mode=CONN_MODE)[int(node_num)]))
        os.system('ssh -i %s %s' % (private_key, getHosts(mode=CONN_MODE)[int(node_num)]))

@task(help={'line-content': 'Contnet to add', 'remote-file-path': 'Path to remote file', 'override': 'Override content instead of append', 'verbose': 'Verbose output'})
def append_line(ctx, line_content, remote_file_path, override=False, verbose=False):
    """
    Append (or Override) content in new line in a remote file.
    (prevent to use ' ' in your string or it may be ignore)
    """
    if override:
        CMD_parallel(ctx, "echo '%s' | sudo tee %s" % (line_content, remote_file_path))
    else:
        CMD_parallel(ctx, "echo '%s' | sudo tee -a %s" % (line_content, remote_file_path))
    if verbose:
        CMD_parallel(ctx, "cat %s" % remote_file_path, verbose=True)

@task(help={'line-content': 'Content match to comment (or uncomment)', 'remote-file-path': 'Path to remote file', 'uncomment': 'Uncomment line instead of comment', 'verbose': 'Verbose output'})
def comment_line(ctx, line_content, remote_file_path, uncomment=False, verbose=False):
    """
    Commment or uncomment a line in a remote file
    """
    if uncomment:
        CMD_parallel(ctx, 'line="%s"; sudo sed -i "s/^#\($line\)\$/$line/" %s' % (line_content, remote_file_path))
    else:
        CMD_parallel(ctx, 'line="%s"; sudo sed -i "s/^$line\$/#&/" %s' % (line_content, remote_file_path))
    if verbose:
        CMD_parallel(ctx, "cat %s" % remote_file_path, verbose=True)

@task(help={'uncommit': 'Uncommit deb-src line in Raspbian (testing phase)'})
def update_and_upgrade(ctx, uncommit=False):
    """
    apt-update and apt-upgrade (this may take a while)
    """
    # Raspbian /etc/apt/sources.list
    UNCOMMENT_URL = r"deb-src http:\/\/raspbian.raspberrypi.org\/raspbian\/ stretch main contrib non-free rpi"
    if uncommit:
        sources_list = '/etc/apt/sources.list'
        print("Uncommit deb-src in", sources_list)
        comment_line(ctx, UNCOMMENT_URL, sources_list, uncomment=True, verbose=True)
    CMD_parallel(ctx, 'sudo apt-get update -y && sudo apt-get upgrade -y')

### Quick Setup

@task
def set_hostname(ctx):
    """
    Set hostname for each node. (it will need to reboot)
    """
    reboot = input('This command will need to reboot all the nodes, are you sure you want to continue? (y/N): ')
    if reboot not in ('y', 'Y'):
        return
    for node_num, hostname in enumerate(HOSTNAMES):
        print('Modifying %s (%d)...' % (hostname, node_num))
        connection = connect(node_num, conn_mode=connection_mode.IP)
        # Modify /etc/hostname
        connection.sudo('echo "%s" | sudo tee /etc/hostname' % hostname)
    # Reboot
    print("Rebooting...")
    try:
        CMD_parallel(ctx, 'sudo reboot')
    except:
        # It will get error when lost connection
        pass

@task
def ssh_config(ctx):
    """
    Set up SSH keys for all pi@ user
    """
    # If ssh key doesn't exist in TEMP_FILES folder then generate one
    os.system(f'mkdir -p {TEMP_FILES}')
    if not os.path.isfile(f'{TEMP_FILES}/id_rsa'):
        try:
            # Remove remote ssh key (make sure it's the same version)
            CMD_parallel(ctx, "rm .ssh/id_rsa*")
        except:
            print('Already clean')
        # Generate ssh key
        os.system(f"ssh-keygen -t rsa -b 4096 -N '' -C 'cluster user key' -f {TEMP_FILES}/id_rsa")
    
    # Upload ssh key
    CMD_parallel(ctx, 'mkdir -p -m 0700 .ssh')
    uploadfile(ctx, f'{TEMP_FILES}/id_rsa', '.ssh', verbose=True)
    uploadfile(ctx, f'{TEMP_FILES}/id_rsa.pub', '.ssh', verbose=True)

    # Append 
    with open(f'{TEMP_FILES}/id_rsa.pub', 'r') as pubkeyfile:
        pubkey = pubkeyfile.read()
        for connection in Group:
            connection.run('touch .ssh/authorized_keys')
            if connection.run('grep -Fxq "%s" %s' % (pubkey, '.ssh/authorized_keys'), warn=True).failed:
                print('No such key, append')
                connection.run('echo "%s" >> .ssh/authorized_keys' % pubkey)
            else:
                print('Already set')

@task(help={'user': 'The user you want to change password for', 'old': 'If enable this flag, it will use your user to login (i.e. ask your current password)'})
def change_passwd(ctx, user, old=False):
    """
    Change a user's password for all nodes
    """
    if old:
        # Method 1. Login with that user and then change the password
        old_password = getpass.getpass("What's your current password?") 
        new_password = getpass.getpass("What password do you want to set?") # If new password is too simple here, it will be reject...
        currResponder = Responder(
            pattern=r'current', # (current) UNIX password:
            response=old_password+'\n',
        )
        newResponder = Responder(
            pattern=r'new', # Enter new UNIX password: and Retype new UNIX password:
            response=new_password+'\n',
        )
        for node_num in range(NUM_NODES):
            connection = connect(node_num, user=user, password=old_password)
            print(connection.run('hostname -I'))
            connection.run('passwd', pty=True, watchers=[currResponder, newResponder])
    else:
        # Method 2. Login with pi and use it as superuser to change other user's password
        new_password = getpass.getpass("What password do you want to set?") # It can accept all kinds of password
        newResponder = Responder(
            pattern=r'new', # Enter new UNIX password: and Retype new UNIX password:
            response=new_password+'\n',
        )
        for connection in Group:
            connection.sudo('sudo passwd %s' % user, pty=True, watchers=[newResponder])

### Hadoop

@task
def download_hadoop(ctx):
    """
    Download specific version of Hadoop to ./temp_files
    """
    print('Downloading to', os.path.join(TEMP_FILES, HADOOP_TARFILE))
    os.system(f'wget {HADOOP_MIRROR} -P {TEMP_FILES}')

@task
def install_hadoop(ctx):
    """
    Auto Setup Hadoop
    1. Add hadoop user and group
    2. Generate ssh key for hadoop user
    3. Upload tar file, extract it and change owner to hadoop group and user
    4. Setup environment variable in /etc/bash.bashrc
    """

    # Hadoop user create password responser
    """
    Enter new UNIX password
    Retype new UNIX password
    """
    hadoopPasswordResponder = Responder(
        pattern=r'new',
        response=HADOOP_PASSWORD+'\n',
    )
    """
    Enter the new value, or press ENTER for the default
        Full Name []:
        Room Number []:
        Work Phone []:
        Home Phone []:
        Other []:
    Is the information correct? [Y/n]
    """
    hduserResponder = Responder(
        pattern=r'(\[\]:|\[Y/n\])',
        response='\n'
    )

    print("\n\n====== Set user and group =======")
    for connection in Group:
        print("Setting user and group on", connection)
        # Add a group, a user and then add the user to the group
        try: # If already exists it will keep going
            connection.sudo(f"sudo addgroup {HADOOP_GROUP}", hide=True)
            print(f"Group {HADOOP_GROUP} added!")
        except:
            print(f"Group {HADOOP_GROUP} already exists")
        try:
            connection.sudo(f"sudo adduser --ingroup {HADOOP_GROUP} {HADOOP_USER}", hide=True, watchers=[hadoopPasswordResponder, hduserResponder])
            print(f"User {HADOOP_USER} has been added in {HADOOP_GROUP}!")
        except:
            print(f"User {HADOOP_USER} already in {HADOOP_GROUP}")
        try:
            connection.sudo(f"sudo adduser {HADOOP_USER} sudo", hide=True)
            print(f"User {HADOOP_USER} is a member of SUPERUSER!!")
        except:
            print(f"User {HADOOP_USER} already in sudo")
        print("\tCurrent hadoop user's groups:", end=" ")
        connection.run(f'groups {HADOOP_USER}')

    print("\n\n====== Generate ssh key =======")
    os.system(f'mkdir -p {TEMP_FILES}/hadoopSSH') # Generate in local
    if not os.path.isfile(f'{TEMP_FILES}/hadoopSSH/id_rsa'):
        print(f"Generating hadoop key in {TEMP_FILES}/hadoopSSH")
        os.system(f'ssh-keygen -t rsa -P "" -f {TEMP_FILES}/hadoopSSH/id_rsa')
        os.system(f'cat {TEMP_FILES}/hadoopSSH/id_rsa.pub > {TEMP_FILES}/hadoopSSH/authorized_keys')

    print("Uploading keys to remote")
    for node_num in range(NUM_NODES):
        connection = connect(node_num, user=HADOOP_USER, password=HADOOP_PASSWORD)
        # Remove remote ssh key (make sure it's the same version)
        try:
            connection.run('rm .ssh/id_rsa* .ssh/authorized_keys', hide=True)
        except:
            pass
        connection.put(f'{TEMP_FILES}/hadoopSSH/id_rsa', remote=f'/home/{HADOOP_USER}/.ssh')
        connection.put(f'{TEMP_FILES}/hadoopSSH/id_rsa.pub', remote=f'/home/{HADOOP_USER}/.ssh')
        connection.put(f'{TEMP_FILES}/hadoopSSH/authorized_keys', remote=f'/home/{HADOOP_USER}/.ssh')

    print("====== Upload", HADOOP_TARFILE, "======")
    for connection in Group:
        print("Connect to", connection)
        if connection.run('test -d %s' % HADOOP_INSTALL, warn=True).failed:
            print("Did not find %s, uploading %s..." % (HADOOP_INSTALL, HADOOP_TARFILE))
            connection.put(os.path.join(TEMP_FILES, HADOOP_TARFILE), remote=REMOTE_UPLOAD)
            print("Extracting tar file...")
            connection.sudo('tar zxf %s -C %s' % (os.path.join(REMOTE_UPLOAD, HADOOP_TARFILE), '/opt'))
            print("Clean up tar file...")
            connection.run('rm %s' % os.path.join(REMOTE_UPLOAD, HADOOP_TARFILE))
            print("Change owner...")
            connection.sudo(f'sudo chown -R {HADOOP_USER}:{HADOOP_GROUP} {HADOOP_INSTALL}')
        else:
            print('Found %s, skip to next node' % HADOOP_INSTALL)

    print("\n\n====== Setup environment variable ======")
    bashrc_location = '/etc/bash.bashrc'
    bashrc_setting = f'''
# Hadoop Settings
export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")
export HADOOP_HOME={HADOOP_INSTALL}
export HADOOP_INSTALL=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export PATH=$PATH:$HADOOP_INSTALL/bin
'''
    for connection in Group:
        if connection.run("grep -Fxq '%s' %s" % ("# Hadoop Settings", bashrc_location), warn=True).failed:
            print('No previous settings, append settings...')
            append_line(ctx, bashrc_setting, bashrc_location)
            #pirnt('Current appending:')
            #connection.run("tail -n 8 %s" % bashrc_location) # check the settings
            print('Applying changes...')
            connection.run('source %s' % bashrc_location) # apply changes
        else:
            print('Setting already exist')
        
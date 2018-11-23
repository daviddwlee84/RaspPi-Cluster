## fabric
from fabric import task
from fabric import Config
# Connection
from fabric import Connection, ThreadingGroup

# util
import os

#############################
#       User Setting        #
#############################

HOSTS = [
    'pi@192.168.1.109', # Master
    'pi@192.168.1.101',
    'pi@192.168.1.102',
    'pi@192.168.1.103',
]

USER = 'pi'
PASSWORD = 'raspberry'

FILE_PATH = './Files' # configure files
TEMP_FILES = './temp_files' # file download, generated ssh key etc.
REMOTE_UPLOAD = os.path.join('/home', USER, 'Downloads')


HADOOP_VERSION = '3.1.1'
HADOOP_FOLDER = 'hadoop-%s' % (HADOOP_VERSION,)
HADOOP_TARFILE = 'hadoop-%s.tar.gz' % (HADOOP_VERSION,)
HADOOP_APACHE_PATH = '/hadoop/common/hadoop-%s/%s' % (HADOOP_VERSION, HADOOP_TARFILE)
HADOOP_INSTALL = os.path.join('/opt', 'hadoop-%s' % (HADOOP_VERSION,))

#NUM_SLAVES = 3
#SLAVES = ['hadoop%i.local' % (i) for i in range(1, NUM_SLAVES+1)]
#HOSTS = ['master.local'] + SLAVE

#############################
#   Global Fabric Object    #
#############################

# for sudo privilege
Configure = Config(overrides={'sudo': {'password': PASSWORD}})

# Parallel Group
Group = ThreadingGroup(*HOSTS, connect_kwargs={'password': PASSWORD}, config=Configure)

#############################
#       Helper Function     #
#############################

# Get Single Conneciton to node
def connect(node_num):
    return Connection(HOSTS[int(node_num)], connect_kwargs={'password': PASSWORD}, config=Configure)

#############################

### General usage

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
    elif len(HOSTS) > int(node_num) >= 0:
        # Run command on specific node
        connection = connect(node_num)
        if verbose:
            print("Executing command on", connection)
        connection.run(command, pty=verbose)
    else:
        print('No such node.')    
        print('Node list:\n', HOSTS)

@task(help={'command': "Command you want to sent to host in parallel", 'verbose': "Verbose output"})
def CMD_parallel(ctx, command, verbose=False):
    """
    Execute command on all nodes in parallel
    """
    results = Group.run(command, hide=True)
    if verbose:
        for connection, result in results.items():
            print("{0.host}: {1.stdout}".format(connection, result))

@task(help={'path-to-file': "Path to file in local", 'dest': "Remote destination (directory)", 'verbose': "Verbose output", 'node-num': "Node number of HOSTS list"})
def uploadfile(ctx, path_to_file, dest=REMOTE_UPLOAD, verbose=False, node_num=-1):
    """
    Copy local file to remote
    """
    if int(node_num) == -1:
        # Run command on all nodes
        for connection in Group:
            if connection.run('test -f %s' % os.path.join(dest, os.path.basename(path_to_file)), warn=True).failed:
                if verbose:
                    print("Connect to", connection)
                    print("Copying file %s to %s" % (path_to_file, dest))
                connection.put(path_to_file, remote=dest)
            else:
                if verbose:
                    print("File already exist")
    elif len(HOSTS) > int(node_num) >= 0:
        # Run command on specific node
        connection = connect(node_num)
        if connection.run('test -f %s' % os.path.join(dest, os.path.basename(path_to_file)), warn=True).failed:
            if verbose:
                print("Connect to", connection)
                print("Copying file %s to %s" % (path_to_file, dest))
            connection.put(path_to_file, remote=dest)
        else:
            if verbose:
                print("File already exist")
    else:
        print('No such node.')    
        print('Node list:\n', HOSTS)
    #TODO: chmod

### Quick Setup

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

### Hadoop

@task
def download_hadoop(ctx):
    """
    Download specific version of Hadoop to ./Files
    """
    print('Downloading to', os.path.join(TEMP_FILES, HADOOP_TARFILE))
    os.system(f'wget http://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-{HADOOP_VERSION}/hadoop-{HADOOP_VERSION}.tar.gz -P {TEMP_FILES}')

@task
def install_hadoop(ctx):
    """
    Auto Setup Hadoop
    """
    # SerialGroupt.put() is still pending
    # https://github.com/fabric/fabric/issues/1800
    # https://github.com/fabric/fabric/issues/1810
    # (but it is in the tutorial... http://docs.fabfile.org/en/2.4/getting-started.html#bringing-it-all-together)

    for connection in Group:
        print("Connect to", connection)
        if connection.run('test -d %s' % HADOOP_INSTALL, warn=True).failed:
            print("Did not find %s, uploading %s..." % (HADOOP_INSTALL, HADOOP_TARFILE))
            connection.put(os.path.join(TEMP_FILES, HADOOP_TARFILE), remote=REMOTE_UPLOAD)
            print("Extracting tar file...")
            connection.sudo('tar zxf %s -C %s' % (os.path.join(REMOTE_UPLOAD, HADOOP_TARFILE), '/opt'))
            print("Clean up tar file...")
            connection.run('rm %s' % os.path.join(REMOTE_UPLOAD, HADOOP_TARFILE))
        else:
            print('Found %s, skip to next node' % HADOOP_INSTALL)

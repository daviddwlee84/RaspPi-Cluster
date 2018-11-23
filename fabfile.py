# fabric
from fabric import task
from fabric import Config
from fabric import Connection
from fabric import SerialGroup
from fabric import ThreadingGroup

# util
import os
from distutils.util import strtobool

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
configure = Config(overrides={'sudo': {'password': PASSWORD}}) # for sudo privilege

INSTALL_FILE_PATH = './Files'
REMOTE_UPLOAD = os.path.join('/home', USER, 'Downloads')


HADOOP_VERSION = '3.1.1'
HADOOP_FOLDER = 'hadoop-%s' % (HADOOP_VERSION,)
HADOOP_TARFILE = 'hadoop-%s.tar.gz' % (HADOOP_VERSION,)
HADOOP_APACHE_PATH = '/hadoop/common/hadoop-%s/%s' % (HADOOP_VERSION, HADOOP_TARFILE)
HADOOP_INSTALL = os.path.join('/opt', 'hadoop-%s' % (HADOOP_VERSION,))

#NUM_SLAVES = 6
#SLAVES = [USER + 'hadoop%i.local' % (i) for i in range(1, NUM_SLAVES+1)]
#HOSTS = ['master.local'] + SLAVE

#############################
#       Helper Function     #
#############################


#############################

### General usage

@task(help={'command': "Command you want to sent to host", 'verbose': "Verbose output"})
def CMD(ctx, command, verbose=False):
    """
    Run command on all nodes in serial order
    """
    if verbose:
        print("Sending commend")
    for host in HOSTS:
        result = Connection(host, connect_kwargs={'password': PASSWORD}, config=configure).run(command, hide=True)
        msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
        if verbose:
            print(msg.format(result))

@task(help={'command': "Command you want to sent to host in parallel", 'verbose': "Verbose output"})
def CMD_parallel(ctx, command, verbose=False):
    """
    Execute command on all nodes in parallel
    """
    results = ThreadingGroup(*HOSTS, connect_kwargs={'password': PASSWORD}, config=configure).run(command, hide=True)
    if verbose:
        for connection, result in results.items():
            print("{0.host}: {1.stdout}".format(connection, result))

@task(help={'command': "Command you want to sent to node", 'node-num': "Node number of HOSTS list"})
def CMD_single(ctx, command, node_num):
    """
    Execute command on single node
    """
    c = Connection(HOSTS[int(node_num)], connect_kwargs={'password': PASSWORD}, config=configure)
    print("Executing command on", c)
    c.run(command, pty=True)

@task(help={'path-to-file': "Path to file in local", 'dest': "Remote destination"})
def copyfile(ctx, path_to_file, dest=REMOTE_UPLOAD):
    for host in HOSTS:
        c = Connection(host, connect_kwargs={'password': PASSWORD}, config=configure)
        print("Connect to", c)
        print("Copying file %s to %s" % (path_to_file, dest))
        c.put(path_to_file, remote=dest)

### Hadoop

@task
def install_hadoop(ctx):
    """
    Auto Setup Hadoop
    """
    # SerialGroupt.put() is still pending
    # https://github.com/fabric/fabric/issues/1800
    # https://github.com/fabric/fabric/issues/1810
    # (but it is in the tutorial... http://docs.fabfile.org/en/2.4/getting-started.html#bringing-it-all-together)
    # Group = SerialGroup(*HOSTS, connect_kwargs={'password': PASSWORD}, config=configure)
    # Group.run('mkdir -p /opt')
    # # Upload and unpack
    # Group.put(os.path.join(INSTALL_FILE_PATH, HADOOP_TARFILE), remote=os.path.join('/opt', HADOOP_TARFILE))
    # Group.run('tar -C %s zxf %s' % (HADOOP_INSTALL, HADOOP_TARFILE))

    for host in HOSTS:
        c = Connection(host, connect_kwargs={'password': PASSWORD}, config=configure)
        print("Connect to", c)
        if c.run('test -d %s' % HADOOP_INSTALL, warn=True).failed:
            print("Did not find %s, uploading %s..." % (HADOOP_INSTALL, HADOOP_TARFILE))
            c.put(os.path.join(INSTALL_FILE_PATH, HADOOP_TARFILE), remote=REMOTE_UPLOAD)
            print("Extracting tar file...")
            c.sudo('tar zxf %s -C %s' % (os.path.join(REMOTE_UPLOAD, HADOOP_TARFILE), '/opt'))
            print("Clean up tar file...")
            c.run('rm %s' % os.path.join(REMOTE_UPLOAD, HADOOP_TARFILE))
            #print("Moving...")
            #c.sudo("mv %s %s" % (HADOOP_FOLDER, HADOOP_INSTALL))
            #c.sudo('tar zxf %s' % os.path.join('/opt', HADOOP_TARFILE))
        else:
            print('Found %s, skip to next node' % HADOOP_INSTALL)

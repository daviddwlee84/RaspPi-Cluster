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

# yaml
import yaml

class connection_mode(Enum):
    IP = True
    HOSTNAME = False

#############################
#   Load From YMAL Config   #
#############################

# It's very convenient to save multiple configuration files and keys and configures
# To switch between different server (if you have multiple server)
# (The value in parenthesis means the default value in my case)

# path to yaml connection configuration file
YAML_CONF = './configure.yaml'

if YAML_CONF:
    with open(YAML_CONF, 'r') as stream:
        yamldict = yaml.load(stream)

# Local file path

FILE_PATH = yamldict['Path']['FILE_PATH'] # configure files ('./Files')
TEMP_FILES = yamldict['Path']['TEMP_FILES'] # file download ('./temp_files')
SSH_KEY_PATH = yamldict['Path']['SSH_KEY_PATH'] # generated ssh key ('./connection')

# Connection Settings

NUM_NODES = yamldict['NUM_NODES'] # (4)

# Host IP
HOSTS_IP = yamldict['Connection']['HOST_IP']

# Default user and password
USER = yamldict['Connection']['Login']['USER'] # (pi)
PASSWORD = yamldict['Connection']['Login']['PASSWORD'] # (password)

# Hadoop
HADOOP_GROUP = yamldict['Hadoop']['Connection']['Login']['HADOOP_GROUP'] # Hadoop group name ('hadoop')
HADOOP_USER = yamldict['Hadoop']['Connection']['Login']['HADOOP_USER'] # Hadoop user name ('hduser')
HADOOP_PASSWORD = yamldict['Hadoop']['Connection']['Login']['HADOOP_PASSWORD'] # Hadoop user password ('hadoop')

#############################
#       User Settings       #
#############################

# === Connection Settings === #

# Hostname
slavenames = ['slave%i' % (i) for i in range(1, NUM_NODES)]
HOSTNAMES = ['master'] + slavenames

# Default SSH Private Key path
# if you're using server you've already generate key for it
# you can change this path manually
DEFAULT_SSHKEY = f'{SSH_KEY_PATH}/id_rsa'

# Connection mode
# USE connection_mode.IP MODE BEFORE YOU SETUP HOSTNAME
# OR MODIFY 'master' ABOVE TO 'raspberrypi' (WHICH IS DEFAULT HOSTNAME FOR RASPBERRY PI)
# IF YOU ONLY RUN ON SINGLE NODE
CONN_MODE = connection_mode.HOSTNAME
# =========================== #

# Default upload remote directory
REMOTE_UPLOAD = f'/home/{USER}/Downloads'

# === Hadoop === #
HADOOP_VERSION = '3.1.1'
#HADOOP_MIRROR = 'http://ftp.mirror.tw/pub/apache/hadoop/common' # Taiwan mirror
HADOOP_MIRROR = 'http://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common' # China Tsinghua mirror

# === Spark === #
SPARK_VERSION = '2.4.0'
# Pre-built for Apache Hadoop 2.7 and later
SPARK_MIRROR = 'http://ftp.mirror.tw/pub/apache/spark' # Taiwan mirror


# Location for hadoop SSH key
HADOOP_SSH_KEY_PATH = f'{SSH_KEY_PATH}/hadoopSSH'

######### Some process #######
# Generally you don't need to modify things here
# unless you clearly understand the dependencies (e.g. hadoop config xml)

# Hadoop
HADOOP_TARFILE = f'hadoop-{HADOOP_VERSION}.tar.gz'
HADOOP_SRC_TARFILE = f'hadoop-{HADOOP_VERSION}-src.tar.gz'
HADOOP_REMOTE_TAR = f'{HADOOP_MIRROR}/hadoop-{HADOOP_VERSION}/{HADOOP_TARFILE}'
HADOOP_REMOTE_SRC_TAR = f'{HADOOP_MIRROR}/hadoop-{HADOOP_VERSION}/{HADOOP_SRC_TARFILE}'
HADOOP_INSTALL = f'/opt/hadoop-{HADOOP_VERSION}' # i.e. $HADOOP_HOME
HADOOP_BUILD = f'/home/{HADOOP_USER}/hadoop-{HADOOP_VERSION}-src' # location to extract and build hadoop
HDFS_DIR = '/hadoop' # namenode, datanodes and tmp

# Spark
SPARK_TARFILE = f'spark-{SPARK_VERSION}-bin-hadoop2.7.tgz'
SPARK_REMOTE_TAR = f'{SPARK_MIRROR}/spark-{SPARK_VERSION}/spark-{SPARK_VERSION}-bin-hadoop2.7.tgz'
SPARK_INSTALL = f'/opt/spark-{SPARK_VERSION}-bin-hadoop2.7'

#############################
#   Global Fabric Object    #
#   and Important Settings  #
#############################

# Get connection information
def getHosts(user=USER, mode=CONN_MODE, onlyAddress=False):
    """
    Return hosts by either IP or Hostname
    """
    if mode == connection_mode.IP:
        if onlyAddress:
            hosts = HOSTS_IP
        else:
            hosts = list(map(lambda host: user + '@' + host, HOSTS_IP))
    elif mode == connection_mode.HOSTNAME:
        if onlyAddress:
            hosts = list(map(lambda hostname: hostname + '.local', HOSTNAMES))
        else:
            hosts = list(map(lambda hostname: user + '@' + hostname + '.local', HOSTNAMES))
    else:
        print("Unknown mode...")
    return hosts

# for sudo privilege
PiConfig = Config(overrides={'sudo': {'password': PASSWORD}})
HadoopConfig = Config(overrides={'sudo': {'password': HADOOP_PASSWORD}})

# Parallel Group
PiGroup = ThreadingGroup(*getHosts(user=USER), connect_kwargs={'password': PASSWORD, 'key_filename': DEFAULT_SSHKEY}, config=PiConfig)
# For hadoop user
HadoopGroup = ThreadingGroup(*getHosts(user=HADOOP_USER), connect_kwargs={'password': HADOOP_PASSWORD, 'key_filename': f'{SSH_KEY_PATH}/hadoopSSH/id_rsa'}, config=HadoopConfig)

#############################
#       Helper Function     #
#############################

def connect(node_num, user=USER, password=PASSWORD, private_key_path=DEFAULT_SSHKEY, conn_mode=CONN_MODE, configure=PiConfig):
    """
    Get Single Conneciton to node
    """
    return Connection(getHosts(user=user, mode=conn_mode)[int(node_num)], connect_kwargs={'password': password, 'key_filename': private_key_path}, config=configure)

def questionAsk(questionDict, question=None):
    """
    dict {'selection description': 'function'}
    """
    if question:
        print(question)

    optionsNum = 1
    questions = ''
    selections = {}
    for question, function in questionDict.items():
        questions += str(optionsNum) + '. ' + question + '\n'
        selections[optionsNum] = function
        optionsNum += 1
    
    def default():
        print('No this option.')

    def select(numSelect):
        return selections.get(numSelect, default)
    
    selection = int(input(questions + '\nSelection: '))
    select(selection)()

#############################

### General usage
@task(help={'actual': "Print actual hostname address from server"})
def node_ls(ctx, actual=False):
    """
    List nodes IP and Hostname either by settings or return message
    """
    print('You, %s, have %d nodes' % (USER, NUM_NODES))
    if actual:
        for num_node, connection in enumerate(PiGroup):
            print("The %d node's hostname and IP" % num_node)
            connection.run('hostname && hostname -I')
    else:
        print('Current connection mode is', CONN_MODE)
        print('Node list:')
        print(getHosts(mode=CONN_MODE))
        print("\n ps. use '-a' flag to show the actual IP return from each nodes")

@task
def show_config(ctx):
    """
    Print all current configurations
    """
    # Use capital letter same as the variable means
    # it's load from yaml configure file or important hard-code in fabfile.py
    # Use lower-case letter means the variable
    # was been calculated by other variable (i.e. has some dependencies)
    current_config = f"""
    \rNodes:
    \r\tNUM_NODES = {NUM_NODES}

    \rPath:
    \r\tFILE_PATH = {FILE_PATH}
    \r\tTEMP_FILES = {TEMP_FILES}
    \r\tSSH_KEY_PATH = {SSH_KEY_PATH}
    
    \rConnection:
    \r\tHOST_IP = {HOSTS_IP}
    \r\tHOSTNAMES = {HOSTNAMES}
    \r\tUSER = {USER}, PASSWORD = {PASSWORD}
    \r\tCONN_MODE = {CONN_MODE}
    \r\tssh key location = {DEFAULT_SSHKEY}
    
    \rHadoop:
    \r\tHADOOP_VERSION = {HADOOP_VERSION}
    \r\tHADOOP_USER = {HADOOP_USER}, HADOOP_PASSWORD = {HADOOP_PASSWORD}, HADOOP_GROUP = {HADOOP_GROUP}
    \r\tHADOOP_SSH_KEY_PATH = {HADOOP_SSH_KEY_PATH}
    \r\tssh key location = {HADOOP_SSH_KEY_PATH}
    """
    print(current_config)

@task(help={'command': "Command you want to sent to host", 'verbose': "Verbose output", 'node-num': "Node number of HOSTS list"})
def CMD(ctx, command, verbose=False, node_num=-1):
    """
    Run command on all nodes in serial order. (with Pi user)
    """
    if int(node_num) == -1:
        # Run command on all nodes
        if verbose:
            print("Sending commend")
        for connection in PiGroup:
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

@task(help={'command': "Command you want to sent to host in parallel", 'hadoop': "Use hadoop user to login or default use pi.", 'verbose': "Verbose output"})
def CMD_parallel(ctx, command, hadoop=False, verbose=False):
    """
    Execute command on all nodes in parallel. (with Pi user or Hadoop user)
    """
    if hadoop:
        results = HadoopGroup.run(command, hide=True)
    else:
        results = PiGroup.run(command, hide=True)
    
    if verbose:
        for connection, result in results.items():
            print("{0.host}:\n{1.stdout}\n".format(connection, result))

@task(help={'filepath': "Path to file in local", 'destination': "Remote destination (directory)", 'permission': "Use superuser to move file", 'verbose': "Verbose output", 'node-num': "Node number of HOSTS list", 'scp': "Use scp instead of fabric"})
def uploadfile(ctx, filepath, destination=REMOTE_UPLOAD, permission=False, verbose=False, node_num=-1, scp=False):
    """
    Copy local file to remote. (If the file exist, it will be overwritten)
    Make sure you are the owner of the remote directory
    Use scp mode to support copy folder
    """
    # Use scp
    def scp_upload(dest):
        if int(node_num) == -1:
            for host in getHosts(user=USER):
                os.system('scp -r -i %s %s %s:%s' % (DEFAULT_SSHKEY, filepath, host, dest))
        elif NUM_NODES > int(node_num) >= 0:
            os.system('scp -r -i %s %s %s:%s' % (DEFAULT_SSHKEY, filepath, getHosts(user=USER)[int(node_num)], dest))
        else:
            print('No such node.')    
            node_ls(ctx)
    
    # Use fabric connection.put
    def simple_upload(dest):
        if int(node_num) == -1:
            # Run command on all nodes
            for connection in PiGroup:
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

    # Make sure default upload folder exist
    # Don't use sudo, or there will cause permission denied problem
    # since the owner of the directory will be sudo:sudo
    CMD_parallel(ctx, f'mkdir -p {REMOTE_UPLOAD}')
    # Upload file
    if permission:
        if scp:
            scp_upload(REMOTE_UPLOAD)
        else:
            simple_upload(REMOTE_UPLOAD)
        if verbose:
            print("Moving all file from %s to %s" % (os.path.join(REMOTE_UPLOAD, os.path.basename(filepath)), destination))
        if int(node_num) == -1:
            CMD_parallel(ctx, 'sudo mv %s %s' % (os.path.join(REMOTE_UPLOAD, os.path.basename(filepath)), destination))
        else:
            CMD(ctx, 'sudo mv %s %s' % (os.path.join(REMOTE_UPLOAD, os.path.basename(filepath)), destination), node_num=node_num)
    else:
        if scp:
            scp_upload(destination)
        else:
            try:
                simple_upload(destination)        
            except PermissionError:
                print("Your destination need superuser privilege, try using -p flag!")

@task(help={'node-num': "Node number of HOSTS list", 'hadoop': 'Use Hadoop user instead of pi user to login', 'private-key': "Path to private key"})
def ssh_connect(ctx, node_num, hadoop=False, private_key=DEFAULT_SSHKEY):
    """
    Connect to specific node using ssh private key (make sure you've generated the key)
    1. Pi: ssh-config
    2. Hadoop: install-hadoop
    """
    if hadoop:
        user = HADOOP_USER
        private_key=f'{HADOOP_SSH_KEY_PATH}/id_rsa'
    else:
        user = USER
        if private_key != DEFAULT_SSHKEY:
            private_key = expanduser(private_key) # expand ~ to actual route
        
    if not os.path.isfile(private_key):
        print("Can't find private key at", private_key)
    else:
        if int(node_num) > NUM_NODES or int(node_num) < 0:
            print('No such node')
            node_ls(ctx)
            return
        print('ssh -i %s %s' % (private_key, getHosts(user=user)[int(node_num)]))
        os.system('ssh -i %s %s' % (private_key, getHosts(user=user)[int(node_num)]))

@task(help={'line-content': 'Contnet to add', 'remote-file-path': 'Path to remote file', 'hadoop': 'Use hadoop user', 'override': 'Override content instead of append', 'verbose': 'Verbose output'})
def append_line(ctx, line_content, remote_file_path, hadoop=False, override=False, verbose=False):
    """
    Append (or Override) content in new line in a remote file.
    (prevent to use ' ' in your string or it may be ignore)
    """
    if override:
        CMD_parallel(ctx, "echo '%s' | sudo tee %s" % (line_content, remote_file_path), hadoop=hadoop)
    else:
        CMD_parallel(ctx, "echo '%s' | sudo tee -a %s" % (line_content, remote_file_path), hadoop=hadoop)
    if verbose:
        CMD_parallel(ctx, "cat %s" % remote_file_path, verbose=True)

@task(help={'line-content': 'Content match to comment (or uncomment)', 'remote-file-path': 'Path to remote file', 'uncomment': 'Uncomment line instead of comment', 'verbose': 'Verbose output'})
def comment_line(ctx, line_content, remote_file_path, uncomment=False, verbose=False):
    """
    Commment or uncomment a line in a remote file
    """
    if uncomment:
        CMD_parallel(ctx, 'line="%s"; sudo sed -i "s/^#.*\($line\)\$/$line/" %s' % (line_content, remote_file_path))
    else:
        CMD_parallel(ctx, 'line="%s"; sudo sed -i "s/^$line\$/# &/" %s' % (line_content, remote_file_path))
    if verbose:
        CMD_parallel(ctx, "cat %s" % remote_file_path, verbose=True)

@task(help={'match': 'Pattern to match', 'replace': 'String to replace', 'remote-file-path': 'Path to remote file', 'verbose': 'Verbose output'})
def find_and_replace(ctx, match, replace, remote_file_path, verbose=False):
    """
    Find pattern matched and replace it
    """
    CMD_parallel(ctx, "sudo sed -i 's/%s/%s/' %s" % (match, replace, remote_file_path), verbose=verbose)
    if verbose:
        print('Replacing %s with %s in %s' % (match, replace, remote_file_path))
        print('Result:')
        CMD_parallel(ctx, "cat %s" % remote_file_path, verbose=True)

@task(help={'uncommit': 'Uncommit deb-src line in Raspbian (testing phase)'})
def update_and_upgrade(ctx, uncommit=False):
    """
    apt-update and apt-upgrade
    """
    print("Updating... (this may take a while)")
    # Raspbian /etc/apt/sources.list
    UNCOMMENT_URL = r"deb-src http:\/\/raspbian.raspberrypi.org\/raspbian\/ stretch main contrib non-free rpi"
    if uncommit:
        sources_list = '/etc/apt/sources.list'
        print("Uncommit deb-src in", sources_list)
        comment_line(ctx, UNCOMMENT_URL, sources_list, uncomment=True, verbose=True)
    CMD_parallel(ctx, 'sudo apt-get update -y && sudo apt-get upgrade -y')

@task(help={'install-package': "Packages you want to install, seperate by ',' in a string"})
def env_setup(ctx, install_package=""):
    """
    Environment setup
    """
    if not install_package: # default install
        to_install = ['git', 'vim', 'tmux', 'zsh']
    else:
        to_install = [x.strip() for x in install_package.split(',')]

    for connection in PiGroup:
        if not install_package and connection.run('which java', warn=True).failed: # Java
            to_install.append('oracle-java8-jdk')

        print("Install %s" % (' '.join(to_install)))
        connection.sudo('sudo apt-get -y install %s' % (' '.join(to_install)))

@task
def favorite_devenv(ctx, masterOnly=False):
    """
    Install oh-my-zsh, vim and tmux powerline theme on Master node
    """
    connection = connect(0) # Master

    print("Installing basic environment")
    env_setup(ctx) # git vim tmux zsh

    zshInstallPassword = Responder(
        pattern=r'password',
        response=PASSWORD+'\n',
    )
    print("Installing oh-my-zsh")
    connection.run('sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"',
                    pty=True, watchers=[zshInstallPassword])
    #TODO
    

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
        connection = connect(node_num, conn_mode=connection_mode.IP) # Force to use IP to connect
        # Modify /etc/hostname
        connection.sudo('echo "%s" | sudo tee /etc/hostname' % hostname)
        # Modify /etc/hosts
        connection.sudo("sudo sed -i 's/%s/%s/' %s" % (r'127.0.1.1\s*\t*.*', '127.0.1.1\t%s' % hostname, '/etc/hosts'))
        print("Results:")
        print("/etc/hostname:")
        connection.run('cat /etc/hostname')
        print("/etc/hosts:")
        connection.run('cat /etc/hosts')
    print("Rebooting...")
    try:
        CMD_parallel(ctx, 'sudo reboot')
    except:
        # It will get error when lost connection
        pass

@task(help={'clean': 'Clean up previous settings'})
def hosts_config(ctx, cleanup=False):
    """
    Bind internal fixed IP address between nodes in /etc/hosts
    """
    for num_node, connection in enumerate(PiGroup):
        if cleanup:
            print('\n'+HOSTNAMES[num_node])
            for i in range(NUM_NODES):
                if i == num_node:
                    comment_line(ctx, '127.0.1.1\t%s' % HOSTNAMES[i], '/etc/hosts', uncomment=True)
                print(HOSTS_IP[i]+'\t'+HOSTNAMES[i])
                connection.sudo("sudo sed -i '/%s/d' %s" % (HOSTS_IP[i]+'\t'+HOSTNAMES[i], '/etc/hosts'), hide=True)
        else:
            print('\n'+HOSTNAMES[num_node])
            for i in range(NUM_NODES):
                if i == num_node:
                    # Disable self-routing
                    comment_line(ctx, '127.0.1.1\t%s' % HOSTNAMES[i], '/etc/hosts')
                print(HOSTS_IP[i]+'\t'+HOSTNAMES[i])
                connection.sudo("echo '%s' | sudo tee -a %s" % (HOSTS_IP[i]+'\t'+HOSTNAMES[i], '/etc/hosts'), hide=True)
    print('\n\nResult:\n')
    CMD(ctx, 'cat /etc/hosts', verbose=True) # Check result

@task(help={'clean': 'Clean up previous settings'})
def interfaces_config(ctx, cleanup=False):
    """
    Setup fixed IP address for each node itself in /etc/network/interfaces
    """
    pass

@task
def ssh_config(ctx):
    """
    Set up SSH keys for all pi@ user
    """
    # If ssh key doesn't exist in TEMP_FILES folder then generate one
    os.system(f'mkdir -p {SSH_KEY_PATH}')
    if not os.path.isfile(f'{SSH_KEY_PATH}/id_rsa'):
        try:
            # Remove remote ssh key (make sure it's the same version)
            CMD_parallel(ctx, "rm .ssh/id_rsa*")
        except:
            print('Already clean')
        # Generate ssh key
        os.system(f"ssh-keygen -t rsa -b 4096 -N '' -C 'cluster user key' -f {SSH_KEY_PATH}/id_rsa")
        newkeygen = True
    else:
        newkeygen = False
    
    # Upload ssh key
    CMD_parallel(ctx, 'mkdir -p -m 0700 .ssh')
    uploadfile(ctx, f'{SSH_KEY_PATH}/id_rsa', '.ssh', verbose=True)
    uploadfile(ctx, f'{SSH_KEY_PATH}/id_rsa.pub', '.ssh', verbose=True)

    # Append 
    with open(f'{SSH_KEY_PATH}/id_rsa.pub', 'r') as pubkeyfile:
        pubkey = pubkeyfile.read()
        for connection in PiGroup:
            connection.run('touch .ssh/authorized_keys')
            # Somehow grep not work quite well
            if newkeygen or connection.run('grep -Fxq "%s" %s' % (pubkey, '.ssh/authorized_keys'), warn=True).failed:
                print('No such key, append')
                connection.run('echo "%s" >> .ssh/authorized_keys' % pubkey)
            else:
                print('Already set')

@task(help={'clean': 'Clean up previous settings'})
def add_source(ctx, cleanup=False):
    """
    Add sources to solve slow download problem because of the fucking GFW
    """
    pipconf = '/etc/pip.conf'
    if cleanup:
        # pip
        # comment_line(ctx, r'extra-index-url=', pipconf, uncomment=True)
        # Not sure why this will delete all the content
        # PiGroup.run("sudo sed -i '/%s/d' %s" % (r'index-url=http:\/\/mirrors.aliyun.com\/pypi\/simple\/', pipconf), hide=True)
        # PiGroup.run("sudo sed -i '/%s/d' %s" % (r'[install]', pipconf), hide=True)
        # PiGroup.run("sudo sed -i '/%s/d' %s" % (r'trusted-host=mirrors.aliyun.com', pipconf), hide=True)
        append_line(ctx, '[global]\nextra-index-url=https://www.piwheels.org/simple', pipconf, override=True) # recover to original status
    else:
        # pip
        comment_line(ctx, r'extra-index-url=https:\/\/www.piwheels.org\/simple', pipconf)
        append_line(ctx, 'index-url=http://mirrors.aliyun.com/pypi/simple/\n[install]\ntrusted-host=mirrors.aliyun.com', pipconf)
    # pip
    CMD(ctx, 'cat %s' % pipconf, verbose=True) # Check result

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
        for connection in PiGroup:
            connection.sudo('sudo passwd %s' % user, pty=True, watchers=[newResponder])

### Hadoop

## Hadoop Setup

@task(help={'src': 'Download source version instead of binary version'})
def download_hadoop(ctx, src=False):
    """
    Download specific version of Hadoop to ./temp_files
    """
    if src:
        print('Downloading source version to', os.path.join(TEMP_FILES, HADOOP_SRC_TARFILE))
        os.system(f'wget {HADOOP_REMOTE_SRC_TAR} -P {TEMP_FILES}')
    else:
        print('Downloading binary version to', os.path.join(TEMP_FILES, HADOOP_TARFILE))
        os.system(f'wget {HADOOP_REMOTE_TAR} -P {TEMP_FILES}')

@task(help={'filefolder': "Folder with all the configuration files", 'verbose': "Verbose output"})
def update_hadoop_conf(ctx, filesfolder=FILE_PATH, verbose=False):
    """
    Upload hadoop configuration files. (if exist then it will update/overwrite them.)
    Must contain files: 'core-site.xml', 'mapred-site.xml', 'hdfs-site.xml', 'yarn-site.xml'
    """
    conffiles = ['core-site.xml', 'mapred-site.xml', 'hdfs-site.xml', 'yarn-site.xml']
    for conffile in conffiles:
        local = os.path.join(filesfolder, conffile)
        destinaiton = os.path.join(HADOOP_INSTALL, 'etc/hadoop', conffile)
        if verbose:
            print("Uploading", local, "to", destinaiton)
        uploadfile(ctx, local, destinaiton, permission=True)
    PiGroup.run(f'sudo chown -R {HADOOP_USER}:{HADOOP_GROUP} {HADOOP_INSTALL}/etc/hadoop')
    print("\nConfiguration updated! (remember to restart Hadoop to load the settings if your Hadoop is still running.)\n")

@task(help={'verbose': "More detail of setup checking"})
def install_hadoop(ctx, verbose=False):
    """
    Auto Setup Hadoop
    0. Download hadoop
    1. Add hadoop user and group
    2. Generate ssh key for hadoop user
    3. Upload tar file, extract it and change owner to hadoop group and user
    4. Setup environment variable in /etc/bash.bashrc and in hadoop-env.sh
    5. Set master and slaves (workers)
    6. Upload configuration file
    7. Formating master HDFS as namenode (will ask you if you have formatted)
    """
    # Check and download hadoop
    os.system(f'mkdir -p {TEMP_FILES}') # Generate in local
    if not os.path.isfile(f'{TEMP_FILES}/{HADOOP_TARFILE}'):
        download_hadoop(ctx, src=False)

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
    for connection in PiGroup:
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
    os.system(f'mkdir -p {HADOOP_SSH_KEY_PATH}') # Generate in local
    if not os.path.isfile(f'{HADOOP_SSH_KEY_PATH}/id_rsa'):
        print(f"Generating hadoop key in {HADOOP_SSH_KEY_PATH}")
        os.system(f'ssh-keygen -t rsa -P "" -f {HADOOP_SSH_KEY_PATH}/id_rsa')
        os.system(f'cat {HADOOP_SSH_KEY_PATH}/id_rsa.pub > {HADOOP_SSH_KEY_PATH}/authorized_keys')
    else:
        print("Hadoop ssh key already generated")

    print("Uploading keys to remote")
    for connection in PiGroup:
        connection.sudo(f'sudo mkdir -p /home/{HADOOP_USER}/.ssh')
        # Remove remote ssh key (make sure it's the same version)
        connection.sudo(f'sudo rm /home/{HADOOP_USER}/.ssh/id_rsa* /home/{HADOOP_USER}/.ssh/authorized_keys', warn=True, hide=True)
    uploadfile(ctx, f'{HADOOP_SSH_KEY_PATH}/id_rsa', destination=f'/home/{HADOOP_USER}/.ssh', permission=True)
    uploadfile(ctx, f'{HADOOP_SSH_KEY_PATH}/id_rsa.pub', destination=f'/home/{HADOOP_USER}/.ssh', permission=True)
    uploadfile(ctx, f'{HADOOP_SSH_KEY_PATH}/authorized_keys', destination=f'/home/{HADOOP_USER}/.ssh', permission=True)
    CMD_parallel(ctx, f'sudo chown {HADOOP_USER}:{HADOOP_GROUP} /home/{HADOOP_USER}/.ssh -R')

    print("\n\n====== Upload", HADOOP_TARFILE, "======")
    for connection in PiGroup:
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
    # use '# Hadoop Settings' as flag
    bashrc_setting = f'''
# Hadoop Settings
export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")
export HADOOP_HOME={HADOOP_INSTALL}
export YARN_HOME=$HADOOP_HOME
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
'''
    for connection in PiGroup:
        print("Setting", connection)
        if connection.run("grep -Fxq '%s' %s" % ("# Hadoop Settings", bashrc_location), warn=True).failed:
            print('No previous settings, append settings...')
            append_line(ctx, bashrc_setting, bashrc_location)
            if verbose:
                print('Tail of %s:' % bashrc_location)
                connection.run("tail -n 8 %s" % bashrc_location) # check the settings
            print('Applying changes...')
            connection.run('source %s' % bashrc_location) # apply changes
        else:
            print('Setting already exist')
        
        if verbose:
            print("Hadoop version:")
            connection.run('hadoop version')

    # Set hadoop-env.sh
    hadoop_env_file = f'{HADOOP_INSTALL}/etc/hadoop/hadoop-env.sh'
    print("Setting", hadoop_env_file)
    # JAVA_HOME
    comment_line(ctx, 'export JAVA_HOME=', hadoop_env_file, uncomment=True)
    find_and_replace(ctx, r'^export JAVA_HOME=.*', r'export JAVA_HOME=\$\(readlink -f \/usr\/bin\/java \| sed "s:bin\/java::"\)', hadoop_env_file)
    # HADOOP_HEAPSIZE_MAX
    comment_line(ctx, 'export HADOOP_HEAPSIZE_MAX=', hadoop_env_file, uncomment=True)
    find_and_replace(ctx, r'^export HADOOP_HEAPSIZE_MAX=.*', 'export HADOOP_HEAPSIZE_MAX=256', hadoop_env_file)

    print("\n\n====== Set master and slaves (workers) ======")
    masterFile = f'{HADOOP_INSTALL}/etc/hadoop/master'
    slavesFile = f'{HADOOP_INSTALL}/etc/hadoop/workers' # Hadoop 3.X
    #slavesFile = f'{HADOOP_INSTALL}/etc/hadoop/slaves' # Hadoop 2.X
    HadoopGroup.run('echo '' | tee %s %s' % (masterFile, slavesFile))
    for num_node, host in enumerate(HOSTNAMES):
        host += '.local'
        if num_node == 0:
            # master
            HadoopGroup.run('echo "%s" | tee -a %s' % (host, masterFile))
        else:
            # slaves
            HadoopGroup.run('echo "%s" | tee -a %s' % (host, slavesFile))

    print("\n\n====== Copy configure files ======")
    update_hadoop_conf(ctx)
    print("All files have updated!")

    print("\n\n====== HDFS ======")

    print("Creating HDFS directories...")
    PiGroup.run(f'sudo mkdir -p -m 0750 {HDFS_DIR}/tmp && sudo chown {HADOOP_USER}:{HADOOP_GROUP} {HDFS_DIR}/tmp')
    if NUM_NODES == 1:
        # If single node
        # master is both datanode and namenode
        PiGroup[0].sudo(f'sudo mkdir -p {HDFS_DIR}/namenode && sudo chown {HADOOP_USER}:{HADOOP_GROUP} {HDFS_DIR}/namenode')
        PiGroup[0].sudo(f'sudo mkdir -p {HDFS_DIR}/datanode && sudo chown {HADOOP_USER}:{HADOOP_GROUP} {HDFS_DIR}/datanode')
    else:
        # If multiple node
        # master => namenode
        # slaves => datanode
        for num_node, connection in enumerate(PiGroup):
            if num_node == 0:
                connection.sudo(f'sudo mkdir -p {HDFS_DIR}/namenode && sudo chown {HADOOP_USER}:{HADOOP_GROUP} {HDFS_DIR}/namenode')
            else:
                connection.sudo(f'sudo mkdir -p {HDFS_DIR}/datanode && sudo chown {HADOOP_USER}:{HADOOP_GROUP} {HDFS_DIR}/datanode')

    print("Formating master HDFS as namenode...")
    """
    ...
    ...
    Re-format filesystem in Storage Directory root= /hadoop/namenode; location= null ? (Y or N)
    """
    #NamenodeResponder = Responder(
    #    pattern=r'\(Y or N\)',
    #    response='Y\n',
    #)
    # I just leave user to select Y or N in case of accidentally reformat it
    HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hdfs namenode -format')

@task(help={'location': "Location of Hadoop source folder", 'build-protobuf': "Build Protocol Buffers from github source code"})
def build_hadoop(ctx, location=HADOOP_BUILD, build_protobuf=False):
    """
    Build Hadoop source
    (Test phase don't use it now)
    Method 1. make install protobuf (current version)
    Method 2. set HADOOP_PROTOC_PATH and JAVA_HOME and build (haven't script yet)
    """
    print("Install build tools...")
    HadoopGroup.run('sudo apt-get install -y maven libssl-dev build-essential pkgconf cmake')

    if build_protobuf:
        print("Install protobuf building tools...")
        HadoopGroup.run('sudo apt-get install -y autoconf automake libtool curl make g++ unzip')
        # 3.6.X... Too new it don't support
        #print("Clone and build protobuf binary...")
        #HadoopGroup.run('git clone https://github.com/protocolbuffers/protobuf.git')
        #HadoopGroup.run('cd protobuf && git submodule update --init --recursive && ./autogen.sh')
        #HadoopGroup.run('cd protobuf && ./configure --prefix=/usr && make && make check && sudo make install && sudo ldconfig')
        print("Download and build protobuf v2.5.0...")
        HadoopGroup.run('wget https://github.com/protocolbuffers/protobuf/releases/download/v2.5.0/protobuf-2.5.0.tar.gz')
        HadoopGroup.run('tar xzf protobuf-2.5.0.tar.gz')
        HadoopGroup.run('cd protobuf-2.5.0 && ./configure && make && sudo make install') # skip make check
    else:
        print("Install protobuf...")
        HadoopGroup.run('sudo apt-get install -y libprotobuf10 protobuf-compiler')

    print("Building Hadoop... (this may take a while)")
    HadoopGroup.run('cd %s && mvn package -Pdist,native -DskipTests -Dtar' % location)

@task(help={'clean': "Clean tar and build folder when it's finished"})
def fix_hadoop_lib(ctx, clean=False):
    """
    Fix the Java HotSpot(TM) Client VM warning of libhadoop.so.1.0.0 by building it from source file
    (Test phase don't use it now)
    """
    print("====== Upload", HADOOP_SRC_TARFILE, "======")
    for connection in PiGroup:
        print("Connect to", connection)
        if connection.run('test -d %s' % HADOOP_INSTALL, warn=True).failed:
            print("Did not find %s, uploading %s..." % (HADOOP_INSTALL, HADOOP_SRC_TARFILE))
            connection.put(os.path.join(TEMP_FILES, HADOOP_SRC_TARFILE), remote=REMOTE_UPLOAD)
            print("Extracting tar file...")
            connection.sudo('tar zxf %s -C %s' % (os.path.join(REMOTE_UPLOAD, HADOOP_SRC_TARFILE), f'/home/{HADOOP_USER}'))

            build_hadoop(ctx, HADOOP_BUILD)

            if clean:
                print("Clean up tar file...")
                connection.run('rm %s' % os.path.join(REMOTE_UPLOAD, HADOOP_SRC_TARFILE))
        else:
            print('Found %s, skip to next node' % HADOOP_INSTALL)

    print("\n\n====== Copy native library ======")
    HadoopGroup.run(f'mkdir -p {HADOOP_INSTALL}/hadoop-{HADOOP_VERSION}/lib/build')
    HadoopGroup.run(f'cp -r {HADOOP_BUILD}/hadoop-{HADOOP_VERSION}-src/lib/* {HADOOP_INSTALL}/hadoop-{HADOOP_VERSION}/lib/build/') ### here here here
    if clean:
        print("Clean up build file...")
        connection.run(f'rm -r {HADOOP_BUILD}')

    print("\n\n====== Configure environment variable ======")
    bashrc_location = '/etc/bash.bashrc' # here here here
    bashrc_setting = f'''
# Hadoop Lib Settings
export HADOOP_COMMON_LIB_NATIVE_DIR="{HADOOP_INSTALL}/lib/build"
export HADOOP_OPTS="$HADOOP_OPTS -Djava.library.path={HADOOP_INSTALL}/lib/build"
'''
    for connection in PiGroup:
        print("Setting", connection)
        if connection.run("grep -Fxq '%s' %s" % ("# Hadoop Lib Settings", bashrc_location), warn=True).failed:
            print('No previous settings, append settings...')
            append_line(ctx, bashrc_setting, bashrc_location)
            print('Tail of %s:' % bashrc_location)
            connection.run("tail -n 8 %s" % bashrc_location) # check the settings
            print('Applying changes...')
            connection.run('source %s' % bashrc_location) # apply changes
        else:
            print('Setting already exist')

@task
def format_hdfs(ctx):
    """
    Remove data in namenode, datanodes and logs. Then format namenode in master.
    """
    stopped = input('Have you stopped hdfs? (y/N) [N will run stop-hadoop]: ')
    if stopped not in ('y', 'Y'):
        stop_hadoop(ctx)
    for connection in HadoopGroup:
        connection.sudo(f'sudo rm -rf {HDFS_DIR}/namenode/* {HDFS_DIR}/datanode/* {HDFS_DIR}/tmp/*', hide=True)
        connection.sudo(f'sudo rm -rf {HADOOP_INSTALL}/logs/*', hide=True)
    HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hdfs namenode -format')

## Hadoop Utility Functions

@task
def start_hadoop(ctx):
    """
    Start Hadoop
    """
    # Just run on master node
    print("Starting dfs...")
    HadoopGroup[0].run(f'{HADOOP_INSTALL}/sbin/start-dfs.sh')
    print("Starting yarn...")
    HadoopGroup[0].run(f'{HADOOP_INSTALL}/sbin/start-yarn.sh')
    print("Starting jobhistory...")
    # $HADOOP_HOME/sbin/mr-jobhistory-daemon.sh has been deprecated
    HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/mapred --daemon start historyserver')
    print("List of JVM")
    CMD_parallel(ctx, 'jps', hadoop=True, verbose=True)

@task
def stop_hadoop(ctx):
    """
    Stop Hadoop
    """
    # Just run on master node
    print("Stopping dfs...")
    HadoopGroup[0].run(f'{HADOOP_INSTALL}/sbin/stop-dfs.sh')
    print("Stopping yarn...")
    HadoopGroup[0].run(f'{HADOOP_INSTALL}/sbin/stop-yarn.sh')
    print("Stopping jobhistory...")
    HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/mapred --daemon stop historyserver')
    print("List of JVM")
    CMD_parallel(ctx, 'jps', hadoop=True, verbose=True)

@task
def restart_hadoop(ctx):
    """
    Restart Hadoop
    """
    stop_hadoop(ctx)
    start_hadoop(ctx)

@task
def status_hadoop(ctx):
    """
    Show Hadoop status
    """
    # Monitor your HDFS Cluster
    def status_hdfs():
        HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hdfs dfsadmin -report')

    # Monitor YARN
    def status_yarn():
        def running_node():
            HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/yarn node -list')
        def running_app():
            HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/yarn application -list')
        questionAsk({'Report of running nodes': running_node,
                     'Report of running applications': running_app})

    print('HDFS Web Monitor: \thttp://%s:50070' % (getHosts(onlyAddress=True)[0]))
    print('YARN Web Monitor: \thttp://%s:8088/cluster' % (getHosts(onlyAddress=True)[0]))
    print('YARN Job History: \thttp://%s:19888/jobhistory' % (getHosts(onlyAddress=True)[0]))
    print('YARN NameNode Manager: \thttp://%s:8042/node' % (getHosts(onlyAddress=True)[0]))

    questionAsk({'Monitor HDFS': status_hdfs,
                 'Monitor YARN': status_yarn},
                 question="What do you want to monitor?")

@task
def example_hadoop(ctx):
    """
    Select a classic hadoop example to run
    """
    # Remote directory
    resultDir = f'/home/{HADOOP_USER}/hadoop_example_result'
    uploadDir = f'/home/{HADOOP_USER}/hadoop_example_upload'

    def PI_example():
        num_maps = input('Number of Maps (default 16): ')
        num_maps = 16 if not num_maps else int(num_maps)
        samples = input('Samples per Map (default 1000): ')
        samples = 1000 if not samples else int(samples)
        HadoopGroup[0].run('%s/bin/hadoop jar %s/share/hadoop/mapreduce/hadoop-mapreduce-examples-%s.jar pi %d %d' % (HADOOP_INSTALL, HADOOP_INSTALL, HADOOP_VERSION, num_maps, samples))

    def Wordcount_example():
        # Use default hadoop licence to test
        def hadoop_license():
            HadoopGroup[0].run('mkdir -p %s' % resultDir)
            try:
                HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hdfs dfs -rm /license.txt /license-out')
                HadoopGroup[0].run('rm -r %s/license-out' % resultDir)
            except:
                pass
            HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hdfs dfs -copyFromLocal {HADOOP_INSTALL}/LICENSE.txt /license.txt')
            HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hdfs dfs -ls /')
            HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hadoop jar {HADOOP_INSTALL}/share/hadoop/mapreduce/hadoop-mapreduce-examples-{HADOOP_VERSION}.jar wordcount /license.txt /license-out')
            HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hdfs dfs -copyToLocal /license-out {resultDir}/license-out')
            print("Result:")
            HadoopGroup[0].run(f'head {resultDir}/license-out/part-r-00000')
            print("\n...\n")
            HadoopGroup[0].run(f'tail {resultDir}/license-out/part-r-00000')
        def local_file():
            location = input('Where is your file? (file location): ')
            filename = os.path.basename(location)
            hdfsDir = '/hadoopExample/wordCount'
            upload_hdfs(ctx, location, filename=filename, uploadDir=uploadDir, hdfsDir=hdfsDir)
            HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hadoop jar {HADOOP_INSTALL}/share/hadoop/mapreduce/hadoop-mapreduce-examples-{HADOOP_VERSION}.jar wordcount {hdfsDir}/{filename} {hdfsDir}/{filename}-out')
            print("Result:")
            HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hdfs dfs -cat {hdfsDir}/{filename}-out/part-r-00000')
            clean = input('Clean up? (Y/n): ')
            if clean not in ('n', 'N'):
                HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hdfs dfs -rm -r {hdfsDir}/{filename} {hdfsDir}/{filename}-out')
        questionAsk({'Hadoop license': hadoop_license, 'Local file': local_file}, question='\nUse default Hadoop license or Local file?')
    questionAsk({'PI': PI_example, 'Wordcount': Wordcount_example}, question="Select an Hadoop example")

@task(help={'path-to-file': 'Local file path', 'uploadDir': 'Remote upload dir/path', 'hdfsDir': 'HDFS directory', 'override': 'Override same name file in HDFS', 'verbose': 'Verbose output'})
def upload_hdfs(ctx, path_to_file, filename='', uploadDir = f'/home/{HADOOP_USER}/HDFSupload', hdfsDir='/HDFSupload', override=False, verbose=False):
    """
    Upload local file to cluster's HDFS
    Default:
        Remote Upload: /home/hduser/HDFSupload/yourFileName
        HDFS Upload: /HDFSupload/yourFileName
    """
    Master = HadoopGroup[0]
    # Upload to remote
    if not filename:
        filename = os.path.basename(path_to_file)
    remotefile = os.path.join(uploadDir, filename)
    Master.run('mkdir -p %s' % uploadDir)
    if verbose:
        print(f'Uploading {path_to_file} to remote {remotefile}')
    uploadfile(ctx, path_to_file, destination=remotefile, permission=True, node_num=0)

    # From remote to HDFS
    hdfsfile = os.path.join(hdfsDir, filename)
    Master.run(f'{HADOOP_INSTALL}/bin/hadoop fs -mkdir -p {hdfsDir}')
    if verbose:
        print(f'Copy from Local {remotefile} to HDFS {hdfsfile}')
    if override:
        Master.run(f'{HADOOP_INSTALL}/bin/hadoop fs -copyFromLocal -f {remotefile} {hdfsfile}', hide=not verbose)
    else:
        Master.run(f'{HADOOP_INSTALL}/bin/hadoop fs -copyFromLocal {remotefile} {hdfsfile}', hide=not verbose)
    if verbose:
        print(f'Content in {hdfsDir}')
        Master.run(f'{HADOOP_INSTALL}/bin/hadoop fs -ls {hdfsDir}')


### Spark

## Spark Setup

@task
def download_spark(ctx):
    """
    Download specific version of Spark to ./temp_files
    """
    print('Downloading binary version to', os.path.join(TEMP_FILES, SPARK_TARFILE))
    os.system(f'wget {SPARK_REMOTE_TAR} -P {TEMP_FILES}')

@task(help={'filefolder': "Folder with all the configuration files", 'verbose': "Verbose output"})
def update_spark_conf(ctx, filesfolder=FILE_PATH, verbose=False):
    """
    Upload spark configuration files. (if exist then it will update/overwrite them.)
    Must contain files: 'spark-env.sh'
    """
    conffiles = ['spark-env.sh']
    for conffile in conffiles:
        local = os.path.join(filesfolder, conffile)
        destinaiton = os.path.join(SPARK_INSTALL, 'conf', conffile)
        if verbose:
            print("Uploading", local, "to", destinaiton)
        uploadfile(ctx, local, destinaiton, permission=True)
    PiGroup.run(f'sudo chown -R {HADOOP_USER}:{HADOOP_GROUP} {SPARK_INSTALL}/conf')
    print("\nConfiguration updated! (remember to restart Spark to load the settings if your Spark is still running.)\n")

@task(help={'verbose': "More detail of setup checking"})
def install_spark(ctx, verbose=False):
    """
    Install Spark (current is Standalone mode)
    0. Download Spark
    1. Upload tar file, extract it and change owner to hadoop group and user
    2. Setup environment variable in /etc/bash.bashrc
    3. Install PySpark by pip
    4. Copy configuration files to SPARK_INSTALL/conf
    """
    # Check and download spark
    os.system(f'mkdir -p {TEMP_FILES}') # Generate in local
    if not os.path.isfile(f'{TEMP_FILES}/{SPARK_TARFILE}'):
        download_spark(ctx)

    print("\n\n====== Upload", SPARK_TARFILE, "======")
    for connection in PiGroup:
        print("Connect to", connection)
        if connection.run('test -d %s' % SPARK_INSTALL, warn=True).failed:
            print("Did not find %s, uploading %s..." % (SPARK_INSTALL, SPARK_TARFILE))
            connection.put(os.path.join(TEMP_FILES, SPARK_TARFILE), remote=REMOTE_UPLOAD)
            print("Extracting tar file...")
            connection.sudo('tar zxf %s -C %s' % (os.path.join(REMOTE_UPLOAD, SPARK_TARFILE), '/opt'))
            print("Clean up tar file...")
            connection.run('rm %s' % os.path.join(REMOTE_UPLOAD, SPARK_TARFILE))
            print("Change owner...")
            connection.sudo(f'sudo chown -R {HADOOP_USER}:{HADOOP_GROUP} {SPARK_INSTALL}')
        else:
            print('Found %s, skip to next node' % SPARK_INSTALL)
    
    print("\n\n====== Setup environment variable ======")
    bashrc_location = '/etc/bash.bashrc'
    # use '# Hadoop Settings' as flag
    bashrc_setting = f'''
# Spark Settings
export SPARK_HOME={SPARK_INSTALL}
export PATH=$PATH:$SPARK_HOME/bin
'''

    for connection in PiGroup:
        if connection.run("grep -Fxq '%s' %s" % ("# Spark Settings", bashrc_location), warn=True).failed:
            print('No previous settings, append settings...')
            append_line(ctx, bashrc_setting, bashrc_location) # This will append line to all the nodes
            if verbose:
                print('Tail of %s:' % bashrc_location)
                connection.run("tail -n 4 %s" % bashrc_location) # check the settings
            print('Applying changes...')
            connection.run('source %s' % bashrc_location) # apply changes
        else:
            print('Setting already exist')

        if verbose:    
            print(" version:")
            connection.run('spark-shell version')
    
    print("\n\n====== Install PySpark ======")

    if PiGroup.run('python3 -c "import pyspark"', warn=True).failed:
        print('Installing.... This may take a while...')
        PiGroup.run("pip3 --no-cache-dir install pyspark")
    else:
        print('Already installed.')

    print("\n\n====== Copy configure files ======")
    update_spark_conf(ctx)
    print("All files have updated!")

    print("\n\n====== Set slaves on master ======")
    slavesFile = f'{SPARK_INSTALL}/conf/slaves'
    HadoopGroup[0].run('echo '' | tee %s' % (slavesFile))
    for host in HOSTNAMES[1:]:
        host += '.local'
        # slaves
        HadoopGroup[0].run('echo "%s" | tee -a %s' % (host, slavesFile))

## Spark Unility Function

@task
def start_spark(ctx):
    """
    Start Spark
    """
    # Just run on master node
    print("Starting spark...")
    HadoopGroup[0].run(f'{SPARK_INSTALL}/sbin/start-all.sh')

@task
def stop_spark(ctx):
    """
    Stop Spark
    """
    # Just run on master node
    print("Stopping spark...")
    HadoopGroup[0].run(f'{SPARK_INSTALL}/sbin/stop-all.sh')

@task
def restart_spark(ctx):
    """
    Restart Spark
    """
    stop_spark(ctx)
    start_spark(ctx)

@task
def status_spark(ctx):
    """
    Show Spark status
    """
    print('Spark Web Monitor: \thttp://%s:8080' % (getHosts(onlyAddress=True)[0]))

@task
def example_spark(ctx):
    """
    Run example on PySpark
    """
    sparkExampleDir = f'{SPARK_INSTALL}/examples/src/main/python'
    uploadDir = f'/home/{HADOOP_USER}/sparkExample/wordCount'

    def PI_example():
        partitions = input('Partitions (default 100): ')
        partitions = 100 if not partitions else int(partitions)
        # found that default deploy mode is client mode
        print(f'{SPARK_INSTALL}/bin/spark-submit --master spark://{HOSTNAMES[0]}.local:7077 --deploy-mode client {sparkExampleDir}/pi.py {partitions}')
        HadoopGroup[0].run(f'{SPARK_INSTALL}/bin/spark-submit --master spark://{HOSTNAMES[0]}.local:7077 --deploy-mode client {sparkExampleDir}/pi.py {partitions}')

    def Wordcount_example():
        def spark_license():
            print(f'{SPARK_INSTALL}/bin/spark-submit --master spark://{HOSTNAMES[0]}.local:7077 {sparkExampleDir}/wordcount.py {SPARK_INSTALL}/LICENSE')
            HadoopGroup[0].run(f'{SPARK_INSTALL}/bin/spark-submit --master spark://{HOSTNAMES[0]}.local:7077 {sparkExampleDir}/wordcount.py {SPARK_INSTALL}/LICENSE')
            
        def local_file(useHDFS=False):
            print('To be done.')
            pass
            # location = input('Where is your file? (file location): ')
            # filename = os.path.basename(location)
            # if useHDFS:
            #     hdfsDir = '/hadoopExample/wordCount'
            #     upload_hdfs(ctx, location, filename=filename, uploadDir=uploadDir, hdfsDir=hdfsDir)
            # else:
            #     HadoopGroup[0].put(location, remote=uploadDir)
            #     HadoopGroup[0].run(f'{SPARK_INSTALL}/bin/spark-submit {sparkExampleDir}/wordcount.py {uploadDir}/{filename}')
            #     clean = input('Clean up? (Y/n): ')
            #     if clean not in ('n', 'N'):
            #         HadoopGroup[0].sudo(f'sudo rm {uploadDir}/{filename}')
        questionAsk({'Spark license': spark_license, 'Local file': local_file}, question='\nUse default Spark license or Local file?')

    questionAsk({'PI': PI_example, 'Wordcount': Wordcount_example}, question="Select an Spark example")

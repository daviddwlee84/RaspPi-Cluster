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

# Local file path
FILE_PATH = './Files' # configure files
TEMP_FILES = './temp_files' # file download, generated ssh key etc.

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

# Default upload remote directory
REMOTE_UPLOAD = f'/home/{USER}/Downloads'

# === Hadoop === #
HADOOP_VERSION = '3.1.1'
#HADOOP_MIRROR = 'http://ftp.mirror.tw/pub/apache/hadoop/common' # Taiwan mirror
HADOOP_MIRROR = 'http://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common' # China Tsinghua mirror

HADOOP_GROUP = 'hadoop' # Hadoop group name
HADOOP_USER = 'hduser' # Hadoop user name
HADOOP_PASSWORD = 'hadoop' # Hadoop user password

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
PiConfig = Config(overrides={'sudo': {'password': PASSWORD}})
HadoopConfig = Config(overrides={'sudo': {'password': HADOOP_PASSWORD}})

# Parallel Group
PiGroup = ThreadingGroup(*getHosts(user=USER, mode=CONN_MODE), connect_kwargs={'password': PASSWORD, 'key_filename': DEFAULT_SSHKEY}, config=PiConfig)
# For hadoop user
HadoopGroup = ThreadingGroup(*getHosts(user=HADOOP_USER, mode=CONN_MODE), connect_kwargs={'password': HADOOP_PASSWORD, 'key_filename': f'{TEMP_FILES}/hadoopSSH/id_rsa'}, config=HadoopConfig)

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
@task
def node_ls(ctx):
    """
    List nodes IP and Hostname
    """
    print('You, %s, have %d nodes' % (USER, NUM_NODES))
    print('Node list:')
    print(getHosts(mode=connection_mode.IP))
    print(getHosts(mode=connection_mode.HOSTNAME))

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

@task(help={'filepath': "Path to file in local", 'destination': "Remote destination (directory)", 'permission': "Use superuser to move file", 'verbose': "Verbose output", 'node-num': "Node number of HOSTS list"})
def uploadfile(ctx, filepath, destination=REMOTE_UPLOAD, permission=False, verbose=False, node_num=-1):
    """
    Copy local file to remote. (If the file exist, it will be overwritten)
    Make sure you are the owner of the remote directory
    """
    # Define helper function
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
        simple_upload(REMOTE_UPLOAD)
        if verbose:
            print("Moving all file from %s to %s" % (os.path.join(REMOTE_UPLOAD, os.path.basename(filepath)), destination))
        CMD_parallel(ctx, 'sudo mv %s %s' % (os.path.join(REMOTE_UPLOAD, os.path.basename(filepath)), destination))
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
        private_key=f'{TEMP_FILES}/hadoopSSH/id_rsa'
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
        print('ssh -i %s %s' % (private_key, getHosts(user=user, mode=CONN_MODE)[int(node_num)]))
        os.system('ssh -i %s %s' % (private_key, getHosts(user=user, mode=CONN_MODE)[int(node_num)]))

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

@task
def env_setup(ctx):
    """
    Environment setup
    """
    to_install = ['git', 'vim', 'tmux']
    for connection in PiGroup:
        if connection.run('which java', warn=True).failed: # Java
            to_install.append('oracle-java8-jdk')

        print("Install %s" %(' '.join(to_install)))
        connection.sudo('sudo apt-get -y install %s' % (' '.join(to_install)))

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
        # Modify /etc/hosts
        connection.sudo("sudo sed -i 's/%s/%s/' %s" % (r'127.0.1.1\s*\t*.*', '127.0.1.1\t%s' % hostname, '/etc/hosts'))
        print("Results:")
        print("/etc/hostname:")
        connection.run('cat /etc/hostname')
        print("/etc/hosts:")
        connection.run('cat /etc/hosts')
        
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
        newkeygen = True
    else:
        newkeygen = False
    
    # Upload ssh key
    CMD_parallel(ctx, 'mkdir -p -m 0700 .ssh')
    uploadfile(ctx, f'{TEMP_FILES}/id_rsa', '.ssh', verbose=True)
    uploadfile(ctx, f'{TEMP_FILES}/id_rsa.pub', '.ssh', verbose=True)

    # Append 
    with open(f'{TEMP_FILES}/id_rsa.pub', 'r') as pubkeyfile:
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
def hosts_config(ctx, cleanup=False):
    """
    Bind internal fixed IP address between nodes in /etc/hosts
    """
    pass

@task(help={'clean': 'Clean up previous settings'})
def interfaces_config(ctx, cleanup=False):
    """
    Setup fixed IP address for each node itself in /etc/network/interfaces
    """
    pass

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

@task
def install_dev_env(ctx):
    """
    Install the best development environment
    (vim, oh-my-zsh, tmux and powerline theme)
    """
    pass

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
    os.system(f'mkdir -p {TEMP_FILES}/hadoopSSH') # Generate in local
    if not os.path.isfile(f'{TEMP_FILES}/hadoopSSH/id_rsa'):
        print(f"Generating hadoop key in {TEMP_FILES}/hadoopSSH")
        os.system(f'ssh-keygen -t rsa -P "" -f {TEMP_FILES}/hadoopSSH/id_rsa')
        os.system(f'cat {TEMP_FILES}/hadoopSSH/id_rsa.pub > {TEMP_FILES}/hadoopSSH/authorized_keys')
    else:
        print("Hadoop ssh key already generated")

    print("Uploading keys to remote")
    for connection in PiGroup:
        connection.sudo(f'sudo mkdir -p /home/{HADOOP_USER}/.ssh')
        # Remove remote ssh key (make sure it's the same version)
        connection.sudo(f'sudo rm /home/{HADOOP_USER}/.ssh/id_rsa* /home/{HADOOP_USER}/.ssh/authorized_keys', warn=True, hide=True)
    uploadfile(ctx, f'{TEMP_FILES}/hadoopSSH/id_rsa', destination=f'/home/{HADOOP_USER}/.ssh', permission=True)
    uploadfile(ctx, f'{TEMP_FILES}/hadoopSSH/id_rsa.pub', destination=f'/home/{HADOOP_USER}/.ssh', permission=True)
    uploadfile(ctx, f'{TEMP_FILES}/hadoopSSH/authorized_keys', destination=f'/home/{HADOOP_USER}/.ssh', permission=True)
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
export HADOOP_INSTALL=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:$HADOOP_INSTALL/bin:$HADOOP_INSTALL/sbin
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
                     'Report of running applications': running_app},
                     question="\n")

    questionAsk({'Monitor HDFS': status_hdfs,
                 'Monitor YARN': status_yarn},
                 question="What do you want to monitor?")

@task
def example_hadoop(ctx):
    """
    Select a classic hadoop example to run
    """

    resultDir = f'/home/{HADOOP_USER}/hadoop_result'
    uploadDir = f'/home/{HADOOP_USER}/to_be_processed'

    def PI_example():
        # Current test
        # 16, 1000 will failed at 100% map 100% reduce.
        # 2, 2 will work.
        # 10, 10 will get the same warning as 16, 1000 but will work.
        # Guessing it's the resource limit problem
        # But I've set up HADOOP_HEAPSIZE_MAX to be 256MB in hadoop-env.sh
        # And other more stuff in mapred-site.xml
        num_maps = input('Number of Maps (default 16): ')
        num_maps = 16 if not num_maps else int(num_maps)
        samples = input('Samples per Map (default 1000): ')
        samples = 1000 if not samples else int(samples)
        HadoopGroup[0].run('%s/bin/hadoop jar %s/share/hadoop/mapreduce/hadoop-mapreduce-examples-%s.jar pi %d %d' % (HADOOP_INSTALL, HADOOP_INSTALL, HADOOP_VERSION, num_maps, samples))

    def Wordcount_example():
        local = input('Use local file or Hadoop license?\n\t1. Local file\n\t2. Hadoop license\n\n1 or 2: ')
        if local == '2':
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
            #HadoopGroup[0].run(f'cat {resultDir}/license-out/part-r-00000') # print entire result may be too long to display
            HadoopGroup[0].run(f'head {resultDir}/license-out/part-r-00000')
            print("\n...\n")
            HadoopGroup[0].run(f'tail {resultDir}/license-out/part-r-00000')
        else:
            location = input('Where is your file? (file location): ')
            filename = os.path.basename(location)
            HadoopGroup[0].run('mkdir -p %s' % uploadDir)
            uploadfile(ctx, location, destination=os.path.join(uploadDir, filename), permission=True, verbose=True)
            HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hdfs dfs -copyFromLocal {uploadDir}/{filename} /{filename}-in')
            HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hdfs dfs -ls /')
            HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hadoop jar {HADOOP_INSTALL}/share/hadoop/mapreduce/hadoop-mapreduce-examples-{HADOOP_VERSION}.jar wordcount /{filename}-in /{filename}-out')
            HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hdfs dfs -copyToLocal /{filename}-out {resultDir}/{filename}-out')
            print("Result:")
            HadoopGroup[0].run(f'head {resultDir}/{filename}-out/part-r-00000')
            print("\n...\n")
            HadoopGroup[0].run(f'tail {resultDir}/{filename}-out/part-r-00000')
            clean = input('Clean up? (Y/n): ')
            if clean not in ('n', 'N'):
                HadoopGroup[0].run(f'{HADOOP_INSTALL}/bin/hdfs dfs -rm /{filename}-in /{filename}-out')
                HadoopGroup[0].run('rm -r %s/%s-out' % (resultDir, filename))

    questionAsk({'PI': PI_example, 'Wordcount': Wordcount_example}, question="Select an Hadoop example")

@task
def hadoop_streaming(ctx, mapper, reducer, **kargs):
    pass

@task
def upload_hdfs(ctx, file, name=None):
    pass
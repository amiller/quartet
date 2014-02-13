from fabric.api import run, cd, sudo, put

def dmidecode():
    sudo('dmidecode -s system-product-name')

def save():
    with cd('quartet_amiller'):
        run('python quartet.py save')

def kill():
    sudo('killall -9 XnSensorServer')
    sudo('killall -9 python')

def update():
    put('quartet_amiller')

def inspect():
    with cd('quartet_amiller'):
        run('python inspect_cams.py')

def setup():
    sudo('apt-get update')
    sudo('apt-get install -y libusb-1.0-0-dev freeglut3-dev doxygen cython ipython python-scipy python-numpy python-opencv python-wxgtk2.8 git default-jdk build-essential g++ cmake emacs23-nox python-wxgtk2.8 python-opengl git python-matplotlib python-snappy')
    put('quartet_amiller')
    #run('git clone git@github.com:amiller/quartet.git')
    with cd('quartet_amiller'):
        run('git submodule init')
        run('git submodule update')
        with cd('OpenNI/Platform/Linux/CreateRedist'):
            run('./RedistMaker')
            with cd('../Redist/OpenNI-Bin-Dev-Linux-x64-v1.5.7.10'):
                sudo('bash install.sh')
        with cd('SensorKinect/Platform/Linux/CreateRedist'):
            run('./RedistMaker')
            with cd('../Redist/Sensor-Bin-Linux-x64-v5.1.2.1/'):
                sudo('bash install.sh')
        with cd('opennpy'):
            sudo('python setup.py install')
        with cd('wxpy3d'):
            sudo('python setup.py install')
        with cd('rtmodel'):
            sudo('python setup.py install')

#sudo pip install pyopengl

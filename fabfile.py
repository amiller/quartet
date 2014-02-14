from fabric.api import run, cd, sudo, put
from fabric.contrib.files import append

def dmidecode():
    sudo('dmidecode -s system-product-name')

def save():
    with cd('quartet_amiller'):
        run('DISPLAY=:0 xhost +x localhost')
        run('DISPLAY=:0 python quartet.py save')

def kill():
    sudo('killall -9 XnSensorServer')
    sudo('killall -9 python')

def reboot():
    sudo('reboot')

def update():
    with cd('quartet_amiller'):
        run('git checkout .')
        run('git pull origin master')
        run('git submodule update')
        with cd('opennpy'):
            sudo('python setup.py install')

def playback():
    with cd('quartet_amiller'):
        run('DISPLAY=:0 xhost +x localhost')
        run('DISPLAY=:0 python quartet.py playback')

def inspect():
    with cd('quartet_amiller'):
        run('python inspect_cams.py')

def preview():
    with cd('quartet_amiller'):
        run('python previewserver.py')

def display():
    with cd('quartet_amiller'):
        run('DISPLAY=:0 xhost +x localhost')
        run('DISPLAY=:0 python quartet.py display')

def niview():
    with cd('quartet_amiller/OpenNI/Platform/Linux/Redist/OpenNI-Bin-Dev-Linux-x64-v1.5.7.10/Samples/Bin/x64-Release'):
        run('DISPLAY=:0 ./NiViewer')

def setup():
    #sudo('apt-get update')
    sudo('apt-get install -y libusb-1.0-0-dev freeglut3-dev libxi-dev libxmu-dev doxygen cython ipython python-scipy python-numpy python-opencv python-wxgtk2.8 git default-jdk build-essential g++ cmake emacs23-nox python-wxgtk2.8 python-opengl git python-matplotlib python-snappy python-zmq')
    append('~/.bashrc', 'DISPLAY=:0 xhost +x localhost')
    append('~/.bashrc', 'export DISPLAY=:0')
    #run('git clone https://github.com/amiller/quartet quartet_amiller')
    with cd('quartet_amiller'):
        run('git submodule init')
        run('git submodule update')
        with cd('libfreenect'):
            run('mkdir -p build')
            with cd('build'):
                run('cmake -DBUILD_PYTHON=on -DLIB_SUFFIX= -DCMAKE_INSTALL_PREFIX=/usr ..')
                run('make')
                sudo('make install')
        # with cd('OpenNI/Platform/Linux/CreateRedist'):
        #     run('./RedistMaker')
        #     with cd('../Redist/OpenNI-Bin-Dev-Linux-x64-v1.5.7.10'):
        #         sudo('bash install.sh')
        # with cd('SensorKinect/Platform/Linux/CreateRedist'):
        #     run('./RedistMaker')
        #     with cd('../Redist/Sensor-Bin-Linux-x64-v5.1.2.1/'):
        #         sudo('bash install.sh')
        with cd('opennpy'):
            sudo('python setup.py install')
        with cd('wxpy3d'):
            sudo('python setup.py install')
        with cd('rtmodel'):
            sudo('python setup.py install')

#sudo pip install pyopengl

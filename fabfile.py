from fabric.api import run, cd, sudo, put, get
from fabric.contrib.files import append

import time
label = time.time()

def dmidecode():
    sudo('dmidecode -s system-product-name')

def save():
    with cd('quartet_amiller'):
        run('DISPLAY=:0 xhost +x localhost')
        run('DISPLAY=:0 python quartet.py save')

def eyesave():
    with cd('quartet_amiller'):
        run('python eye_capture.py save')

def calib():
    with cd('quartet_amiller'):
        run('DISPLAY=:0 python quartet.py save --decimate=10')

def kill():
    sudo('killall -9 XnSensorServer')
    sudo('killall -9 python')

def reboot():
    sudo('reboot')

def trim():
    sudo('fstrim -v /')

def ntp():
    sudo('service ntp stop')
    sudo('ntpdate -s time.nist.gov')
    sudo('service ntp start')
    sudo('ntpq -p')

def mostrecent():
    result = run('ls -1 quartet_amiller/data/kinect_sets | tail -n1')
    get('quartet_amiller/data/kinect_sets/%s' % (result,), 
        'data/quartetdata/%s/host-%%(host)s' % (label))

def update():
    with cd('quartet_amiller'):
        run('git checkout .')
        run('git pull origin master')
        run('git submodule update')
        with cd('libfreenect'):
            run('mkdir -p build')
            with cd('build'):
                run('cmake -DBUILD_PYTHON=on -DLIB_SUFFIX= -DCMAKE_INSTALL_PREFIX=/usr ..')
                run('make')
                sudo('make install')

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

def setup():
    sudo('apt-get update')
    sudo('apt-get install -y ocl-icd-libopencl1 libusb-1.0-0-dev freeglut3-dev libxi-dev libxmu-dev doxygen cython ipython python-scipy python-numpy python-opencv libopencv-dev python-wxgtk2.8 git default-jdk build-essential g++ cmake emacs23-nox python-wxgtk2.8 python-opengl git python-matplotlib python-snappy libsnappy-dev python-zmq indicator-cpufreq ntp')
    #append('~/.bashrc', 'DISPLAY=:0 xhost +x localhost')
    #append('~/.bashrc', 'export DISPLAY=:0')
    run('if ! [ -a quartet_amiller ]; then git clone https://github.com/amiller/quartet quartet_amiller; fi')
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
        # with cd('opennpy'):
        #     sudo('python setup.py install')
        with cd('wxpy3d'):
            sudo('python setup.py install')
        with cd('rtmodel'):
            sudo('python setup.py install')


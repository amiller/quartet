import glob
import subprocess
import os

testdir = "data/quartetdata/quartet/dessner/pm-4sec"
symlinksdir = "data/quartetdata/quartet/dessner/pm-4sec-symlinks"
files = glob.glob("%s/*.prt" % testdir)

def make_symlinks():
    for i in range(5):
        files = sorted(glob.glob("%s/*-%d.*.prt" % (testdir, i)))
        for frame,f in enumerate(files):
            testname = os.path.basename(testdir)
            cmd = "ln -s ../%s/%s %s/%s" % (testname, os.path.basename(f), symlinksdir, "frame-%d.%06d.prt" % (i, frame+1))
            subprocess.call(cmd, shell=True)

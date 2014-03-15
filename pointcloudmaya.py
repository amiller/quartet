from rtmodel import pointmodel
import partio
import subprocess

def pointcloud_to_partio(points, filename):
    p = partio.create()
    P = p.addAttribute("position", partio.VECTOR, 3)
    id = p.addAttribute("id", partio.INT, 1)
    R = p.addAttribute("rgbPP", partio.VECTOR, 3)
    p.addParticles(points.xyz.shape[0])
    for i in xrange(points.xyz.shape[0]):
        p.set(P, i,map(float,points.xyz[i,:]))
        p.set(id,i,(i,))
        p.set(R, i,map(float,points.rgba[i,:3]))
    partio.write(filename,p)
    subprocess.call('~/installing/partio/build/Linux-3.8.0-x86_64-optimize/bin/partconv %s %s.prt' % (filename,filename), shell=True)

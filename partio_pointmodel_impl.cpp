#include <Partio.h>
#include <cstdio>

int write_points_impl(const char *filename, const float *xyz, const float *rgba, int n) {
    Partio::ParticlesDataMutable& foo=*Partio::create();
    Partio::ParticleAttribute idAttr=foo.addAttribute("id",Partio::INT,1);
    Partio::ParticleAttribute positionAttr=foo.addAttribute("position",Partio::VECTOR,3);
    Partio::ParticleAttribute colorAttr=foo.addAttribute("rgbPP",Partio::VECTOR,3);

    foo.addParticles(n);
    for(int i=0;i<n;i++){
        int* id=foo.dataWrite<int>(idAttr,i);
        float* pos=foo.dataWrite<float>(positionAttr,i);
        float* color=foo.dataWrite<float>(colorAttr,i);
        id[0] = i;
        pos[0]=xyz[3*i+0];
        pos[1]=xyz[3*i+1];
        pos[2]=xyz[3*i+2];
        color[0]=rgba[4*i+0];
        color[1]=rgba[4*i+1];
        color[2]=rgba[4*i+2];
    }    
    Partio::write(filename,foo);
    foo.release();
    printf("done [%s]\n", filename);
    return 0;
}

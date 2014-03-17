# distutils: language = c++
# distutils: sources = partio_pointmodel_impl.cpp
# distutils: libraries = partio

cimport numpy as np
import numpy as np

cdef extern from "partio_pointmodel_impl.h":
    int write_points_impl(const char *filename, const float *xyz, const float *rgba, int n)

cdef write_points_(const char *filename,
                   np.ndarray[np.float32_t, ndim=2, mode='c'] xyz,
                   np.ndarray[np.float32_t, ndim=2, mode='c'] rgba,
                   int n):
    write_points_impl(filename,
                      <np.float32_t *> xyz.data,
                      <np.float32_t *> rgba.data,
                      n)

def write_points(filename, pmodel):
    write_points_(filename, 
                  np.ascontiguousarray(pmodel.xyz), 
                  np.ascontiguousarray(pmodel.rgba), 
                  pmodel.xyz.shape[0])

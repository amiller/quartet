from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension("partio_pointmodel", ["partio_pointmodel.pyx", "partio_pointmodel_impl.cpp"],
        libraries = ["partio"],
        library_dirs = ["/home/amiller/lib"])
    ]
ext_modules=cythonize(extensions, language="c++")

setup(name='quartet',
      version='0.1',
      author='Andrew Miller',
      email='amiller@dappervision.com',
      packages=[],
      ext_modules=ext_modules,
      install_requires=['distribute', 'cython', 'pyopencl', 'PyOpenGL', 'numpy', 'scipy'],
      )

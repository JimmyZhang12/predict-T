from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[
    Extension("pdn_sim",        ["sim_pdn.pyx"]),
    Extension("predictor_sim",  ["predictor_sim.pyx"],   language="c++"),
    Extension("ve_dist_sim",    ["ve_dist_sim.pyx"]),
    Extension("long_latency",   ["long_latency.pyx"]),
]

setup(
  name = 'MyProject',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
)

# from distutils.core import setup
# from Cython.Build import cythonize

# setup(
#     ext_modules=cythonize("sim_pdn.pyx")
# )
# # setup(ext_modules = cythonize('ve_dist_sim.pyx'))
# # setup(ext_modules = cythonize('predictor_sim.pyx'))


# # ext_modules = [
# #     Extension("pdn_sim",  ["sim_pdn.pyx"]),
# # ]

# # setup(
# #     name = 'My Program',
# #     cmdclass = {'build_ext': build_ext},
# #     ext_modules = ext_modules
# # )
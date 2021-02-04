from os import path
import glob
dir = '/home/jimmyjz2/passat/gem5/build/X86/python/pybind11/mcpat_src'
 
# temp = path.join(dir ,"../../../../../src")
# temp = path.join(temp ,dir.split('X86/')[-1])
# mcpat_src_path = path.abspath(temp)
# print(mcpat_src_path)

# for name in glob.glob(mcpat_src_path + '/*.cc'):
#     print(name)
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir)

# DIR="$HOME/passat/spec2006/benchspec/CPU2006/401.bzip2/run/run_base_ref_amd64-m64-gcc43-nn.0000"
# name=("bzip") 
# exe=("bzip2_base.amd64-m64-gcc43-nn")
# opt=("$HOME/passat/spec2006/benchspec/CPU2006/401.bzip2/run/run_base_ref_amd64-m64-gcc43-nn.0000/input.program 1")

alpha_suffix = '_base.amd64-m64-gcc43-nn'

#400.perlbench
perlbench = None
perlbench_exe =  'perlbench' + alpha_suffix
# TEST CMDS
#perlbench = [perlbench_exe] + ['-I.', '-I./lib', 'attrs.pl']
# REF CMDS
perlbench = [perlbench_exe] + ['-I./lib', 'checkspam.pl', '2500', '5', '25', '11', '150', '1', '1', '1', '1']
#perlbench = [perlbench_exe] + ['-I./lib', 'diffmail.pl', '4', '800', '10', '17', '19', '300']
#perlbench = [perlbench_exe] + ['-I./lib', 'splitmail.pl', '1600', '12', '26', '16', '4500']
#perlbench.output = out_dir+'perlbench.out'

#401.bzip2
bzip2 = None
bzip2_exe =  'bzip2' + alpha_suffix
# TEST CMDS
#bzip2 = [bzip2_exe] + ['input.program', '5']
# REF CMDS
bzip2 = [bzip2_exe] + ['input.source', '280']
#bzip2 = [bzip2_exe] + ['chicken.jpg', '30']
#bzip2 = [bzip2_exe] + ['liberty.jpg', '30']
#bzip2 = [bzip2_exe] + ['input.program', '280']
#bzip2 = [bzip2_exe] + ['text.html', '280']
#bzip2 = [bzip2_exe] + ['input.combined', '200']
#bzip2.output = out_dir + 'bzip2.out'

#403.gcc
gcc = None
gcc_exe = 'gcc' + alpha_suffix
# TEST CMDS
#gcc = [gcc_exe] + ['cccp.i', '-o', 'cccp.s']
# REF CMDS
gcc = [gcc_exe] + ['166.i', '-o', '166.s']
#gcc = [gcc_exe] + ['200.i', '-o', '200.s']
#gcc = [gcc_exe] + ['c-typeck.i', '-o', 'c-typeck.s']
#gcc = [gcc_exe] + ['cp-decl.i', '-o', 'cp-decl.s']
#gcc = [gcc_exe] + ['expr.i', '-o', 'expr.s']
#gcc = [gcc_exe] + ['expr2.i', '-o', 'expr2.s']
#gcc = [gcc_exe] + ['g23.i', '-o', 'g23.s']
#gcc = [gcc_exe] + ['s04.i', '-o', 's04.s']
#gcc = [gcc_exe] + ['scilab.i', '-o', 'scilab.s']
#gcc.output = out_dir + 'gcc.out'

#410.bwaves
bwaves = None
bwaves_exe = 'bwaves' + alpha_suffix
# TEST CMDS
#bwaves = [bwaves_exe]
# REF CMDS
bwaves = [bwaves_exe]
#bwaves.output = out_dir + 'bwaves.out'

#416.gamess
gamess=None
gamess_exe = 'gamess' + alpha_suffix
# TEST CMDS
#gamess = [gamess_exe]
#gamess_input = 'exam29.config'
# REF CMDS
gamess = [gamess_exe]
gamess_input = 'cytosine.2.config'
#gamess = [gamess_exe]
#gamess_input = 'h2ocu2+.gradient.config'
#gamess = [gamess_exe]
#gamess_input = 'triazolium.config'
#gamess.output = out_dir + 'gamess.out'

#429.mcf
mcf = None
mcf_exe =  'mcf' + alpha_suffix
# TEST CMDS
#mcf = [mcf_exe] + ['inp.in']
# REF CMDS
mcf = [mcf_exe] + ['inp.in']
#mcf.output = out_dir + 'mcf.out'

#433.milc
milc=None
milc_exe = 'milc' + alpha_suffix
# TEST CMDS
#milc = [milc_exe]
#milc_input = 'su3imp.in'
# REF CMDS
milc = [milc_exe]
milc_input = 'su3imp.in'
#milc.output = out_dir + 'milc.out'

#434.zeusmp
zeusmp=None
zeusmp_exe = 'zeusmp' + alpha_suffix
# TEST CMDS
#zeusmp = [zeusmp_exe]
# REF CMDS
zeusmp = [zeusmp_exe]
#zeusmp.output = out_dir + 'zeusmp.out'

#435.gromacs
gromacs = None
gromacs_exe = 'gromacs' + alpha_suffix
# TEST CMDS
#gromacs = [gromacs_exe] + ['-silent','-deffnm', 'gromacs', '-nice','0']
# REF CMDS
gromacs = [gromacs_exe] + ['-silent','-deffnm', 'gromacs', '-nice','0']
#gromacs.output = out_dir + 'gromacs.out'

#436.cactusADM
cactusADM = None
cactusADM_exe = 'cactusADM' + alpha_suffix 
# TEST CMDS
#cactusADM = [cactusADM_exe] + ['benchADM.par']
# REF CMDS
cactusADM = [cactusADM_exe] + ['benchADM.par']
#cactusADM.output = out_dir + 'cactusADM.out'

#437.leslie3d
leslie3d=None
leslie3d_exe = 'leslie3d' + alpha_suffix
# TEST CMDS
#leslie3d = [leslie3d_exe]
#leslie3d_input = 'leslie3d.in'
# REF CMDS
leslie3d = [leslie3d_exe]
leslie3d_input = 'leslie3d.in'
#leslie3d.output = out_dir + 'leslie3d.out'

#444.namd
namd = None
namd_exe = 'namd' + alpha_suffix
# TEST CMDS
#namd = [namd_exe] + ['--input', 'namd_input', '--output', 'namd.out', '--iterations', '1']
# REF CMDS
namd = [namd_exe] + ['--input', 'namd.input', '--output', 'namd.out', '--iterations', '38']
#namd.output = out_dir + 'namd.out'

#445.gobmk
gobmk=None
gobmk_exe = 'gobmk' + alpha_suffix
# TEST CMDS
#gobmk = [gobmk_exe] + ['--quiet','--mode', 'gtp']
#gobmk_input = 'dniwog.tst'
# REF CMDS
gobmk = [gobmk_exe] + ['--quiet','--mode', 'gtp']
gobmk_input = '13x13.tst'
#gobmk = [gobmk_exe] + ['--quiet','--mode', 'gtp']
#gobmk_input = 'nngs.tst'
#gobmk = [gobmk_exe] + ['--quiet','--mode', 'gtp']
#gobmk_input = 'score2.tst'
#gobmk = [gobmk_exe] + ['--quiet','--mode', 'gtp']
#gobmk_input = 'trevorc.tst'
#gobmk = [gobmk_exe] + ['--quiet','--mode', 'gtp']
#gobmk_input = 'trevord.tst'
#gobmk.output = out_dir + 'gobmk.out'

#447.dealII
####### NOT WORKING #########
dealII=None
dealII_exe = 'dealII' + alpha_suffix
# TEST CMDS
####### NOT WORKING #########
dealII = [gobmk_exe]+['8']
# REF CMDS
####### NOT WORKING #########
#dealII.output = out_dir + 'dealII.out'

#450.soplex
soplex=None
soplex_exe = 'soplex' + alpha_suffix
# TEST CMDS
#soplex = [soplex_exe] + ['-m10000', 'test.mps']
# REF CMDS
soplex = [soplex_exe] + ['-m45000', 'pds-50.mps']
#soplex = [soplex_exe] + ['-m3500', 'ref.mps']
#soplex.output = out_dir + 'soplex.out'

#453.povray
povray=None
povray_exe = 'povray' + alpha_suffix
# TEST CMDS
#povray = [povray_exe] + ['SPEC-benchmark-test.ini']
# REF CMDS
povray = [povray_exe] + ['SPEC-benchmark-ref.ini']
#povray.output = out_dir + 'povray.out'

#454.calculix
calculix=None
calculix_exe = 'calculix' + alpha_suffix
# TEST CMDS
#calculix = [calculix_exe] + ['-i', 'beampic']
# REF CMDS
calculix = [calculix_exe] + ['-i', 'hyperviscoplastic']
#calculix.output = out_dir + 'calculix.out' 

#456.hmmer
hmmer=None
hmmer_exe = 'hmmer' + alpha_suffix
# TEST CMDS
#hmmer = [hmmer_exe] + ['--fixed', '0', '--mean', '325', '--num', '45000', '--sd', '200', '--seed', '0', 'bombesin.hmm']
# REF CMDS
hmmer = [hmmer_exe] + ['nph3.hmm', 'swiss41']
#hmmer = [hmmer_exe] + ['--fixed', '0', '--mean', '500', '--num', '500000', '--sd', '350', '--seed', '0', 'retro.hmm']
#hmmer.output = out_dir + 'hmmer.out'

#458.sjeng
sjeng=None
sjeng_exe = 'sjeng' + alpha_suffix 
# TEST CMDS
#sjeng = [sjeng_exe] + ['test.txt']
# REF CMDS
sjeng = [sjeng_exe] + ['ref.txt']
#sjeng.output = out_dir + 'sjeng.out'

#459.GemsFDTD
GemsFDTD=None
GemsFDTD_exe = 'GemsFDTD' + alpha_suffix 
# TEST CMDS
#GemsFDTD = [GemsFDTD_exe]
# REF CMDS
GemsFDTD = [GemsFDTD_exe]
#GemsFDTD.output = out_dir + 'GemsFDTD.out'

#462.libquantum
libquantum=None
libquantum_exe = 'libquantum' + alpha_suffix
# TEST CMDS
#libquantum = [libquantum_exe] + ['33','5']
# REF CMDS
libquantum = [libquantum_exe] + ['1297','8']
#libquantum.output = out_dir + 'libquantum.out' 

#464.h264ref
h264ref=None
h264ref_exe = 'h264ref' + alpha_suffix
# TEST CMDS
#h264ref = [h264ref_exe] + ['-d', 'foreman_test_encoder_baseline.cfg']
# REF CMDS
h264ref = [h264ref_exe] + ['-d', 'foreman_ref_encoder_baseline.cfg']
#h264ref = [h264ref_exe] + ['-d', 'foreman_ref_encoder_main.cfg']
#h264ref = [h264ref_exe] + ['-d', 'sss_encoder_main.cfg']
#h264ref.output = out_dir + 'h264ref.out'

#465.tonto
tonto=None
tonto_exe = 'tonto' + alpha_suffix
# TEST CMDS
#tonto = [tonto_exe]
# REF CMDS
tonto = [tonto_exe]
#tonto.output = out_dir + 'tonto.out'

#470.lbm
lbm=None
lbm_exe = 'lbm' + alpha_suffix
# TEST CMDS
#lbm = [lbm_exe] + ['20', 'reference.dat', '0', '1', '100_100_130_cf_a.of']
# REF CMDS
lbm = [lbm_exe] + ['300', 'reference.dat', '0', '0', '100_100_130_ldc.of']
#lbm.output = out_dir + 'lbm.out'

#471.omnetpp
omnetpp=None
omnetpp_exe = 'omnetpp' + alpha_suffix 
# TEST CMDS
#omnetpp = [omnetpp_exe] + ['omnetpp.ini']
# REF CMDS
omnetpp = [omnetpp_exe] + ['omnetpp.ini']
#omnetpp.output = out_dir + 'omnetpp.out'

#473.astar
astar=None
astar_exe = 'astar' + alpha_suffix
# TEST CMDS
#astar = [astar_exe] + ['lake.cfg']
# REF CMDS
astar = [astar_exe] + ['rivers.cfg']
#astar.output = out_dir + 'astar.out'

#481.wrf
wrf=None
wrf_exe = 'wrf' + alpha_suffix
# TEST CMDS
#wrf = [wrf_exe]
# REF CMDS
wrf = [wrf_exe]
#wrf.output = out_dir + 'wrf.out'

#482.sphinx3
sphinx3=None
sphinx3_exe = 'sphinx_livepretend' + alpha_suffix 
# TEST CMDS
#sphinx3 = [sphinx3_exe] + ['ctlfile', '.', 'args.an4']
# REF CMDS
sphinx3 = [sphinx3_exe] + ['ctlfile', '.', 'args.an4']
#sphinx3.output = out_dir + 'sphinx3.out'

#483.xalancbmk
xalancbmk=None
xalancbmk_exe = 'xalancbmk' + alpha_suffix
# TEST CMDS
######## NOT WORKING ###########
xalancbmk= [xalancbmk_exe]+['-v','test.xml','xalanc.xsl']
# REF CMDS
######## NOT WORKING ###########
xalancbmk_output ='xalancbmk.out'

#998.specrand
specrand_i=None
specrand_i_exe = 'specrand' + alpha_suffix
# TEST CMDS
#specrand_i = [specrand_i_exe] + ['324342', '24239']
# REF CMDS
specrand_i = [specrand_i_exe] + ['1255432124', '234923']
#specrand_i.output = out_dir + 'specrand_i.out'

#999.specrand
specrand_f=None
specrand_f_exe = 'specrand' + alpha_suffix
# TEST CMDS
#specrand_f = [specrand_f_exe] + ['324342', '24239']
# REF CMDS
specrand_f = [specrand_f_exe] + ['1255432124', '234923']
#specrand_f.output = out_dir + 'specrand_f.out'

# DIR="$HOME/passat/spec2006/benchspec/CPU2006/401.bzip2/run/run_base_ref_amd64-m64-gcc43-nn.0000"
# name=("bzip") 
# exe=("bzip2_base.amd64-m64-gcc43-nn")
# opt=("$HOME/passat/spec2006/benchspec/CPU2006/401.bzip2/run/run_base_ref_amd64-m64-gcc43-nn.0000/input.program 1")

names=[
    #"400.perlbench", \ NO BINARIES
    # "401.bzip2", \
    # "403.gcc", \
    # "410.bwaves", \
    # #"416.gamess", \ NO BINARIES
    "429.mcf", \
    "433.milc", \
    # "434.zeusmp", \
    "435.gromacs", \
    "436.cactusADM", \
    "437.leslie3d", \
    "444.namd", \
    "445.gobmk", \
    # "447.dealII", \
    # "450.soplex", \
    "453.povray", \
    "454.calculix", \
    "456.hmmer", \
    "458.sjeng", \
    "459.GemsFDTD", \
    "462.libquantum", \
    "464.h264ref", \
    # "470.lbm", \
    "471.omnetpp", \
    "473.astar", \
    "481.wrf", \
    "482.sphinx3", \
    # "983.xalancbmk", \
    # "998.specrand", \
    # "999.specrand" \
]
names = ["459.GemsFDTD"]



only_names = []
only_nums = []
for i in names:
    only_names.append(i.split(".")[1])
    only_nums.append(i.split(".")[0])

import os
HOME = os.environ['HOME']
print()
f = open(os.getcwd() + '/spec_commands.txt', "w")

#NAMES!
f.write("name=(\n")
for i in names:
    f.write("\t\""+i+"\" \\\n")
f.write(")")
for _ in range(2):
    f.write("\n")

#DIR!
dir_prefix = "$HOME/passat/spec2006/benchspec/CPU2006/"
dir_suffix = "/run/run_base_ref_amd64-m64-gcc43-nn.0000"
f.write("dir=(\n")
for i,t in enumerate(names):
    dir = dir_prefix + t + dir_suffix + '/'
    f.write("\t\""+dir+"\" \\\n")

f.write(")")
for _ in range(2):
    f.write("\n")

#CMDS!
dir_prefix = "$HOME/passat/spec2006/benchspec/CPU2006/"
dir_suffix = "/run/run_base_ref_amd64-m64-gcc43-nn.0000"
f.write("cmd=(\n")
for i,t in enumerate(names):
    if t.split(".")[0] == "998":
        exe = globals()["specrand_i_exe"]
    elif t.split(".")[0] == "999":
        exe = globals()["specrand_f_exe"]
    else:
        exe = globals()[only_names[i] + '_exe']

    # dir = dir_prefix + t + dir_suffix + '/' + exe

    f.write("\t\""+exe+"\" \\\n")

f.write(")")
for _ in range(2):
    f.write("\n")

#OPTIONS!   
dir_prefix = "$HOME/passat/spec2006/benchspec/CPU2006/"
dir_suffix = "/run/run_base_ref_amd64-m64-gcc43-nn.0000/"
bzip2 = [bzip2_exe] + ['input.source', '280']

f.write("opt=(\n")
for i,t in enumerate(names):
    if t.split(".")[0] == "998":
        exe = globals()["specrand_i"]
    elif t.split(".")[0] == "999":
        exe = globals()["specrand_f"]
    else:
        opt = globals()[t.split(".")[1]]

    path = dir_prefix + t + dir_suffix
    write = ""
    for o in opt[1:]: #skip the first list entry which is the exe
        # if '.' in o:
        #     write += (path + o + ' ')
        # else:
        write += (o + ' ')
    write.rstrip()
    f.write("\t\""+write+"\" \\\n")
f.write(")")
for _ in range(2):
    f.write("\n")
#INPUTS!
dir_prefix = "$HOME/passat/spec2006/benchspec/CPU2006/"
dir_suffix = "/run/run_base_ref_amd64-m64-gcc43-nn.0000/"
bzip2 = [bzip2_exe] + ['input.source', '280']

f.write("stdin=(\n")
for i,t in enumerate(names):
    if t.split(".")[0] == "998":
        input_var_name = "specrand_i_input"
    elif t.split(".")[0] == "999":
        input_var_name = "specrand_f_input"
    else:
        input_var_name = t.split(".")[1] + "_input"

    path = dir_prefix + t + dir_suffix
    if input_var_name in globals():
        input = globals()[input_var_name]
        write = path + input
    else:
        write = ""
    f.write("\t\""+write+"\" \\\n")
f.write(")")
for _ in range(2):
    f.write("\n")

# #outputs!
# dir_prefix = "$HOME/passat/testbin/output/"
# bzip2 = [bzip2_exe] + ['input.source', '280']

# f.write("stdout=(\n")
# for i,t in enumerate(names):
#     write = dir_prefix + t + ".out"
#     f.write("\t\""+write+"\" \\\n")
# f.write(")")
# for _ in range(2):
#     f.write("\n")

f.close()

# MIT License
#
# Copyright (c) 2020 Andrew Smith
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# tlb.py
#
# Translation Lookaside Buffer class definition

from xml.etree import ElementTree
from xml.dom import minidom

from tlb import TLB
from btb import BTB
from cache import Cache
from branchpred import Predictor

class Core:
  name = "core"
  id = "core"

  parameters = \
  {
    "clock_rate" : ["1000","Clock Rate in MHz"],
    "vdd" : ["0","0 means using ITRS default vdd"],
    "power_gating_vcc" : ["-1","\"-1\" means using default power gating virtual power supply voltage constrained by technology and computed automatically"],
    "opt_local" : ["0","for cores with unknown timing, set to 0 to force off the opt flag"],
    "instruction_length" : ["32",""],
    "opcode_width" : ["16",""],
    "x86" : ["1",""],
    "micro_opcode_width" : ["8",""],
    "machine_type" : ["0","Specifies the machine type inorder/OoO; 1 inorder; 0 OOO"],
    "number_hardware_threads" : ["2","number_instruction_fetch_ports(icache ports) is always 1 in single-thread processor, it only may be more than one in SMT processors. BTB ports always equals to fetch ports since branch information in consecutive branch instructions in the same fetch group can be read out from BTB once. (cpu.numThreads)"],
    "fetch_width" : ["16","(cpu.fetchWidth)"],
    "number_instruction_fetch_ports" : ["1","fetch_width determines the size of cachelines of L1 cache block"],
    "decode_width" : ["16","decode_width determines the number of ports of the renaming table (both RAM and CAM) scheme (cpu.decodeWidth)"],
    "issue_width" : ["16","(cpu.issueWidth)"],
    "peak_issue_width" : ["16","issue_width determines the number of ports of Issue window and other logic as in the complexity effective processors paper; issue_width==dispatch_width (cpu.issueWidth)"],
    "commit_width" : ["16","commit_width determines the number of ports of register files (cpu.commitWidth)"],
    "fp_issue_width" : ["2","Issue width of the Floating Poing Unit"],
    "prediction_width" : ["1","number of branch instructions can be predicted simultaneously"],
    "pipelines_per_core" : ["1,1","Current version of McPAT does not distinguish int and floating point pipelines. Theses parameters are reserved for future use. integer_pipeline and floating_pipelines, if the floating_pipelines is 0, then the pipeline is shared"],
    "pipeline_depth" : ["31,31","pipeline depth of int and fp, if pipeline is shared, the second number is the average cycles of fp ops issue and exe unit"],
    "ALU_per_core" : ["6","contains an adder, a shifter, and a logical unit"],
    "MUL_per_core" : ["1","For MUL and Div"],
    "FPU_per_core" : ["2","buffer between IF and ID stage"],
    "instruction_buffer_size" : ["32","buffer between ID and sche/exe stage"],
    "decoded_stream_buffer_size" : ["16",""],
    "instruction_window_scheme" : ["0","0 PHYREG based, 1 RSBASED. McPAT support 2 types of OoO cores, RS based and physical reg based"],
    "instruction_window_size" : ["32","(cpu.numIQEntries)"],
    "fp_instruction_window_size" : ["32","The instruction issue Q as in Alpha 21264; The RS as in Intel P6 (cpu.numIQEntries)"],
    "ROB_size" : ["32","Each in-flight instruction has an entry in ROB (cpu.numROBEntries)"],
    "archi_Regs_IRF_size" : ["16","Number of Architectural Integer General Purpose Registers specified by the ISA: X86-64 has 16GPR"],
    "archi_Regs_FRF_size" : ["32","Number of Architectural Registers specified by the ISA: MMX + XMM"],
    "phy_Regs_IRF_size" : ["32","Number of Physical Integer Registers (cpu.numPhysIntRegs)"],
    "phy_Regs_FRF_size" : ["32","Number of Physical FP Registers (cpu.numPhysFloatRegs)"],
    "rename_scheme" : ["0","can be RAM based(0) or CAM based(1) rename scheme RAM-based scheme will have free list, status table; CAM-based scheme have the valid bit in the data field of the CAM"],
    "checkpoint_depth" : ["0","RAM and CAM RAT contains checkpoints, checkpoint_depth=# of in_flight speculations; RAM-based RAT should not have more than 4 GCs (e.g., MIPS R10000).  McPAT assumes the exsistance of RRAT when the RAM-RAT having no GCs (e.g., Netburst) CAM-based RAT should have at least 1 GC and can have more than 8 GCs."],
    "register_windows_size" : ["0","How many windows in the windowed register file, sun processors; no register windowing is used when this number is 0. In OoO cores, loads and stores can be issued whether inorder(Pentium Pro) or (OoO)out-of-order(Alpha), They will always try to execute out-of-order though."],
    "LSU_order" : ["inorder","Load/Store Unit (LSU) Ordering"],
    "store_buffer_size" : ["16","Store Queue Entries (cpu.SQEntries)"],
    "load_buffer_size" : ["16","By default, in-order cores do not have load buffers (cpu.LQEntries)"],
    "memory_ports" : ["2","max_allowed_in_flight_memo_instructions determines the # of ports of load and store buffer as well as the ports of Dcache which is connected to LSU. Dual-pumped Dcache can be used to save the extra read/write ports. Number of ports refer to sustain-able concurrent memory accesses"],
    "RAS_size" : ["2","Branch Predictor RAS Size"],
    "number_of_BPT" : ["2","Number of Branch Predictor Tables (BPT)"],
    "number_of_BTB" : ["2","Number of Branch Target Buffers (BTB)"]
  }
  stats = \
  {
    "total_instructions" : ["0","cpu.iq.iqInstsIssued"],
    "int_instructions" : ["0","iq.FU_type_0::No_OpClass + iq.FU_type_0::IntAlu + iq.FU_type_0::IntMult + iq.FU_type_0::IntDiv + iq.FU_type_0::IprAccess"],
    "fp_instructions" : ["0","cpu.iq.FU_type_0::FloatAdd + cpu.iq.FU_type_0::FloatCmp + cpu.iq.FU_type_0::FloatCvt + cpu.iq.FU_type_0::FloatMult + cpu.iq.FU_type_0::FloatDiv + cpu.iq.FU_type_0::FloatSqrt"],
    "branch_instructions" : ["0","cpu.branchPred.condPredicted"],
    "branch_mispredictions" : ["0","cpu.branchPred.condIncorrect"],
    "load_instructions" : ["0","cpu.iq.FU_type_0::MemRead + cpu.iq.FU_type_0::InstPrefetch"],
    "store_instructions" : ["0","cpu.iq.FU_type_0::MemWrite"],
    "committed_instructions" : ["0","cpu.commit.committedOps"],
    "committed_int_instructions" : ["0","cpu.commit.int_insts"],
    "committed_fp_instructions" : ["0","cpu.commit.fp_insts"],
    "pipeline_duty_cycle" : ["1","<=1, runtime_ipc/peak_ipc; averaged for all cores if homogeneous"],
    "total_cycles" : ["1","cpu.numCycles"],
    "idle_cycles" : ["0","cpu.idleCycles"],
    "busy_cycles" : ["1","cpu.numCycles - cpu.idleCycles"],
    "ROB_reads" : ["0","cpu.rob.rob_reads"],
    "ROB_writes" : ["0","cpu.rob.rob_writes"],
    "rename_reads" : ["0","lookup in renaming logic (cpu.rename.int_rename_lookups)"],
    "rename_writes" : ["0","cpu.rename.RenamedOperands * cpu.rename.int_rename_lookups / cpu.rename.RenameLookups"],
    "fp_rename_reads" : ["0","cpu.rename.fp_rename_lookups"],
    "fp_rename_writes" : ["0","cpu.rename.RenamedOperands * cpu.rename.fp_rename_lookups / cpu.rename.RenameLookups"],
    "inst_window_reads" : ["0","cpu.iq.int_inst_queue_reads"],
    "inst_window_writes" : ["0","cpu.iq.int_inst_queue_writes"],
    "inst_window_wakeup_accesses" : ["0","cpu.iq.int_inst_queue_wakeup_accesses"],
    "fp_inst_window_reads" : ["0","cpu.iq.fp_inst_queue_reads"],
    "fp_inst_window_writes" : ["0","cpu.iq.fp_inst_queue_writes"],
    "fp_inst_window_wakeup_accesses" : ["0","cpu.iq.fp_inst_queue_wakeup_accesses"],
    "int_regfile_reads" : ["0","cpu.int_regfile_reads"],
    "float_regfile_reads" : ["0","cpu.fp_regfile_reads"],
    "int_regfile_writes" : ["1","cpu.int_regfile_writes"],
    "float_regfile_writes" : ["1","cpu.fp_regfile_writes"],
    "function_calls" : ["0","cpu.commit.function_calls"],
    "context_switches" : ["0","cpu.workload.num_syscalls"],
    "ialu_accesses" : ["1","cpu.iq.int_alu_accesses"],
    "fpu_accesses" : ["1","cpu.iq.fp_alu_accesses"],
    "mul_accesses" : ["1","cpu.iq.fu_full::FloatMult"],
    "cdb_alu_accesses" : ["1","cpu.iq.int_alu_accesses"],
    "cdb_mul_accesses" : ["1","cpu.iq.fp_alu_accesses"],
    "cdb_fpu_accesses" : ["1","cpu.iq.fp_alu_accesses"],
    "IFU_duty_cycle" : ["0.25",""],
    "LSU_duty_cycle" : ["0.25",""],
    "MemManU_I_duty_cycle" : ["0.25",""],
    "MemManU_D_duty_cycle" : ["0.25",""],
    "ALU_duty_cycle" : ["1",""],
    "MUL_duty_cycle" : ["0.3",""],
    "FPU_duty_cycle" : ["0.3",""],
    "ALU_cdb_duty_cycle" : ["1",""],
    "MUL_cdb_duty_cycle" : ["0.3",""],
    "FPU_cdb_duty_cycle" : ["0.3",""]
  }

  predictor = None
  itlb = None
  icache = None
  dtlb = None
  dcache = None
  btb = None


  def __init__(self, component_id, component_name, stat_dict, config_dict):
    self.name = component_name
    self.id = component_id

    # Init the Directory Parameters and Stats:

    self.predictor = Predictor(self.id+".predictor","PBT",stat_dict,config_dict)
    self.itlb = TLB(self.id+".itlb","itlb",stat_dict,config_dict)
    self.icache = Cache(self.id+".icache","icache",stat_dict,config_dict)
    self.dtlb = TLB(self.id+".dtlb","dtlb",stat_dict,config_dict)
    self.dcache = Cache(self.id+".dcache","dcache",stat_dict,config_dict)
    self.btb = BTB(self.id+".BTB","BTB",stat_dict,config_dict)

  def xml(self):
    """ Build an XML Tree from the parameters, stats, and subcomponents """
    top = ElementTree.Element('component', id=self.id, name=self.name)
    for key in sorted(self.parameters):
      top.append(ElementTree.Comment(", ".join(['param', key, self.parameters[key][1]])))
      top.append(ElementTree.Element('param', name=key, value=self.parameters[key][0]))
    for key in sorted(self.stats):
      top.append(ElementTree.Comment(", ".join(['stat', key, self.stats[key][1]])))
      top.append(ElementTree.Element('stat', name=key, value=self.stats[key][0]))
    top.append(self.predictor.xml())
    top.append(self.itlb.xml())
    top.append(self.icache.xml())
    top.append(self.dtlb.xml())
    top.append(self.dcache.xml())
    top.append(self.btb.xml())
    return top


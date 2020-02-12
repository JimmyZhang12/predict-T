// DESCRIPTION: Verilator: Verilog example module
//
// This file ONLY is placed into the Public Domain, for any use,
// without warranty, 2017 by Wilson Snyder.
//======================================================================

// Include Shared Memory Struct for InterProcess Communication:
#include <signal.h>
#include "interprocess.h"
mapped* shm_p = NULL;

// Include common routines
#include <verilated.h>

// Include model header, generated from Verilating "top.v"
#include "Vtop.h"

// If "verilator --trace" is used, include the tracing class
#if VM_TRACE
# include <verilated_vcd_c.h>
#endif

// Current simulation time (64-bit unsigned)
vluint64_t main_time = 0;
// Called by $time in Verilog
double sc_time_stamp() {
    return main_time;  // Note does conversion to real, to match SystemC
}

int main(int argc, char** argv, char** env) {
    // This is a more complicated example, please also see the simpler examples/make_hello_c.

    // Prevent unused variable warnings
    if (0 && argc && argv && env) {}

    // Init shared mem, note this process must be started after
    // the driver process.
    mapped* shm_p = create_shm(NINIT);  

    // Set debug level, 0 is off, 9 is highest presently used
    // May be overridden by commandArgs
    Verilated::debug(0);

    // Randomization reset policy
    // May be overridden by commandArgs
    Verilated::randReset(2);

    // Pass arguments so Verilated code can see them, e.g. $value$plusargs
    // This needs to be called before you create any model
    Verilated::commandArgs(argc, argv);

    // Construct the Verilated model, from Vtop.h generated from Verilating "top.v"
    Vtop* top = new Vtop;  // Or use a const unique_ptr, or the VL_UNIQUE_PTR wrapper

#if VM_TRACE
    // If verilator was invoked with --trace argument,
    // and if at run time passed the +trace argument, turn on tracing
    VerilatedVcdC* tfp = NULL;
    const char* flag = Verilated::commandArgsPlusMatch("trace");
    if (flag && 0==strcmp(flag, "+trace")) {
        Verilated::traceEverOn(true);  // Verilator must compute traced signals
        VL_PRINTF("Enabling waves into logs/vlt_dump.vcd...\n");
        tfp = new VerilatedVcdC;
        top->trace(tfp, 99);  // Trace 99 levels of hierarchy
        Verilated::mkdir("logs");
        tfp->open("logs/vlt_dump.vcd");  // Open the dump file
    }
#endif

    // Set some inputs
    top->clk = 0;
    top->rst = 0;
    top->a = 0;
    top->b = 0;
    top->start = 0;
    top->cnt = 0;
    top->sim_over = 0;

    v_incoming_signals new_signals;
    new_signals.start = 0;
    new_signals.rst = 0;
    new_signals.a = 0;
    new_signals.b = 0;
    new_signals.next_clk_cnt = 0;
    new_signals.sim_over = 0;

    uint64_t clk_cnt = 0;
    
    bool ready = false;
    uint64_t next_clk_cnt = 0;
    uint64_t new_next_clk_cnt = 0;

    // Simulate until $finish
    while (!Verilated::gotFinish()) {
      if(new_signals.next_clk_cnt == clk_cnt) {
        printf("%d %d\n", next_clk_cnt, clk_cnt);
        // Wait Until New Data:
        ready = false;
        // Set the Top Level signals:
        next_clk_cnt = new_signals.next_clk_cnt;
        top->rst = new_signals.rst;
        top->a = new_signals.a;
        top->b = new_signals.b;
        top->start = new_signals.start;
        top->sim_over = new_signals.sim_over;
        if(top->sim_over != 1) {
          do {
            sem_wait(&shm_p->pv.sem);
            if(shm_p->pv.new_data == NEW_DATA) {
              ready = true;
              new_signals.next_clk_cnt = shm_p->pv.data.next_clk_cnt;
              new_signals.rst = shm_p->pv.data.rst;
              new_signals.a = shm_p->pv.data.a;
              new_signals.b = shm_p->pv.data.b;
              new_signals.start = shm_p->pv.data.start;
              new_signals.sim_over = shm_p->pv.data.sim_over;
              shm_p->pv.new_data = NO_NEW_DATA;
            }
            sem_post(&shm_p->pv.sem);
          } while (!ready);
        }
      }
      main_time++;  // Time passes...
      // Clk Driver:
      if ((main_time % 2)) {
        top->clk = 1;
      }
      else {
        top->clk = 0;
        clk_cnt++;
      }
      top->cnt = clk_cnt;

      // Evaluate model
      top->eval();

#if VM_TRACE
      // Dump trace data for this cycle
      if (tfp) tfp->dump(main_time);
#endif

      // Read outputs
      VL_PRINTF("[%" VL_PRI64 "d] clk=%u, res=%u\n", main_time, top->cnt, top->res);
    }

    // Final model cleanup
    top->final();

    // Close trace if opened
#if VM_TRACE
    if (tfp) { tfp->close(); tfp = NULL; }
#endif

    //  Coverage analysis (since test passed)
#if VM_COVERAGE
    Verilated::mkdir("logs");
    VerilatedCov::write("logs/coverage.dat");
#endif

    // Destroy model
    delete top; top = NULL;

    // destry shared mem:
    destroy_shm(shm_p);   

    // Fin
    exit(0);
}

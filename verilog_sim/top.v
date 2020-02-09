// DESCRIPTION: Verilator: Verilog example module
//
// This file ONLY is placed into the Public Domain, for any use,
// without warranty, 2003 by Wilson Snyder.
// ======================================================================

// This is intended to be a complex example of several features, please also
// see the simpler examples/make_hello_c.

module top (
  // Declare some signals so we can see how I/O works
  input         clk,
  input logic[31:0] mul_a,
  input logic[31:0] mul_b,
  output logic[31:0] mul_res,
  output logic[31:0] add_res
);
  import "DPI-C" context function void hello_world(input int a);
  export "DPI-C" function hello_world_v;

  function void hello_world_v (int a);
    $display("Hello World from Verilog %d", a);
  endfunction

  function void call_hello (int a);
    hello_world(a);
  endfunction

  // Print some stuff as an example
  initial begin
    $display("Running Call Hello\n");
    call_hello(10);
    $write("*-* All Finished *-*\n");
    $finish;
  end

endmodule

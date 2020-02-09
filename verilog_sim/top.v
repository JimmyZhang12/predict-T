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
  input         rst,
  input logic [31:0] a,
  input logic [31:0] b,
  input logic start,
  output logic [31:0] res,
  output logic ready,
  output logic overflow
);
  import "DPI-C" context function void hello_world(input int id);
  export "DPI-C" function hello_world_v;

  function void hello_world_v (int id);
    $display("Hello World from Verilog %d", id);
  endfunction

  function void call_hello (int id);
    hello_world(id);
  endfunction

  sequential_adder sa
  (
    .clk(clk),
    .rst(rst),
    .a(a),
    .b(b),
    .start(start),
    .ready(ready),
    .overflow(overflow),
    .res(res)
  );

  // Print some stuff as an example
  initial begin
    $display("Running Call Hello\n");
    call_hello(10);
    $write("*-* All Finished *-*\n");
    $finish;
  end

endmodule

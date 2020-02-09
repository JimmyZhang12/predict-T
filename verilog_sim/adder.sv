module adder #(parameter width = 8)
(
  input logic [width-1:0] a, b,
  input logic c_in,
  output logic [width-1:0] f,
  output logic c_out
);
  logic [width:0] intermediate;

  always_comb begin 
    intermediate = a + b + {7'b0, c_in};
    f = intermediate[width-1:0];
    c_out = intermediate[width];
  end
endmodule : adder

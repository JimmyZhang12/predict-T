module register #(parameter width = 8)
(
  input logic clk, rst, load,
  input logic [width-1:0] in,
  output logic [width-1:0] out
);
  logic [width-1:0] data;

  initial begin
    data = 0;
  end

/* verilator lint_off BLKSEQ */
  always_ff @ (posedge clk) begin
    if(rst == 1'b1) begin
      data = 0;
    end
    else if (load == 1'b1) begin
      data = in;
    end
    else begin
      data = data;
    end
  end
/* verilator lint_on BLKSEQ */

  assign out = data;
endmodule : register

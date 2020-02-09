module mux2 #(parameter width = 8)
(
  input logic select,
  input logic [width-1:0] a, b,
  output logic [width-1:0] f
);
  always_comb begin
    f = a;
    case(select)
      0'b00: begin
        f = a;
      end
      0'b01: begin
        f = b;
      end
      default: /* do nothing */;
    endcase
  end
endmodule : mux2

module mux3 #(parameter width = 8)
(
  input logic [1:0] select,
  input logic [width-1:0] a, b, c,
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
      0'b10: begin
        f = c;
      end
      default: /* do nothing */;
    endcase
  end
endmodule : mux3

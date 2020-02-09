module demux2 #(parameter width = 8)
(
  input logic select,
  input logic [width-1:0] f,
  output logic [width-1:0] a, b
);
  always_comb begin
    a = f;
    b = 0;
    case(select)
      0'b00: begin
        a = f;
      end
      0'b01: begin
        b = f;
      end
      default: /* do nothing */;
    endcase
  end
endmodule : demux2

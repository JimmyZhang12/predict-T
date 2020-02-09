module demux3 #(parameter width = 8)
(
  input logic [1:0] select,
  input logic [width-1:0] f,
  output logic [width-1:0] a, b, c
);
  always_comb begin
    a = f;
    b = 0;
    c = 0;
    case(select)
      0'b00: begin
        a = f;
      end
      0'b01: begin
        b = f;
      end
      0'b10: begin
        c = f;
      end
      default: /* do nothing */;
    endcase
  end
endmodule : demux3

module sequential_adder(
  input logic [31:0] a, b;
  input logic start, clk;

  output logic [31:0] res;
  output locic overflow, ready;
}

logic carry;

logic [7:0] a_byte, b_byte;

logic [7:0] res_0, res_1, res_2, res_3;

assign overflow = carry;
assign res i_reg;

enum logic[4:0] {
  wait,
  add_b0,
  add_b1,
  add_b2,
  add_b3,
  complete,
  INVALID_STATE
} state, next_state;

initial begin
  i_reg = 0;
  carry = 0;

end

always_comb begin : control_logic

end : control_logic

always_comb begin : next_state_logic
  ready = 1'b0;
  case(state):
    wait : begin

    end
    add_b0 : begin

    end
    add_b1 : begin

    end
    add_b2 : begin

    end
    add_b3 : begin

    end
    complete : begin

    end
    default : /* Do Nothing */;
end : next_state_logic

assign temp_out = {1'b0, a_byte} + {1'b0, b_byte} + {8'b0, carry};

always @ (posedge clk) begin


end

endmodule;


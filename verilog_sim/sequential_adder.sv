module sequential_adder
(
  input logic [31:0] a, b,
  input logic start, clk, rst,

  output logic [31:0] res,
  output logic overflow, ready
);

enum logic[4:0] {
  idle,
  add_b0,
  add_b1,
  add_b2,
  add_b3,
  complete,
  INVALID_STATE
} state, next_state;

// Signals:
logic load_a;
logic load_b;
logic load_c;
logic load_reg_out_0;
logic load_reg_out_1;
logic load_reg_out_2;
logic load_reg_out_3;

logic [1:0] reg_a_mux_sel;
logic [1:0] reg_b_mux_sel;
logic [1:0] add_demux_sel;
logic reg_c_mux_sel;

logic [31:0] reg_a_out;
logic [31:0] reg_b_out;
logic reg_c_out;
logic reg_c_in;
logic [7:0] reg_out_0_in;
logic [7:0] reg_out_1_in;
logic [7:0] reg_out_2_in;
logic [7:0] reg_out_3_in;
logic [7:0] reg_a_mux_out;
logic [7:0] reg_b_mux_out;
logic reg_c_mux_out;
logic [7:0] adder_out;

// Devices:
register #(.width(32)) reg_a
(
  .clk(clk),
  .rst(rst),
  .load(load_a),
  .in(a),
  .out(reg_a_out)
);
register #(.width(32)) reg_b
(
  .clk(clk),
  .rst(rst),
  .load(load_b),
  .in(b),
  .out(reg_b_out)
);
register #(.width(1)) reg_c
(
  .clk(clk),
  .rst(rst),
  .load(load_c),
  .in(reg_c_in),
  .out(reg_c_out)
);
register #(.width(8)) reg_out_0
(
  .clk(clk),
  .rst(rst),
  .load(load_reg_out_0),
  .in(reg_out_0_in),
  .out(res[7:0])
);
register #(.width(8)) reg_out_1
(
  .clk(clk),
  .rst(rst),
  .load(load_reg_out_1),
  .in(reg_out_1_in),
  .out(res[15:8])
);
register #(.width(8)) reg_out_2
(
  .clk(clk),
  .rst(rst),
  .load(load_reg_out_2),
  .in(reg_out_2_in),
  .out(res[23:16])
);
register #(.width(8)) reg_out_3
(
  .clk(clk),
  .rst(rst),
  .load(load_reg_out_3),
  .in(reg_out_3_in),
  .out(res[31:24])
);
mux4 #(.width(8)) reg_a_mux
(
  .select(reg_a_mux_sel),
  .a(reg_a_out[7:0]),
  .b(reg_a_out[15:8]),
  .c(reg_a_out[23:16]),
  .d(reg_a_out[31:24]),
  .f(reg_a_mux_out)
);
mux4 #(.width(8)) reg_b_mux
(
  .select(reg_b_mux_sel),
  .a(reg_b_out[7:0]),
  .b(reg_b_out[15:8]),
  .c(reg_b_out[23:16]),
  .d(reg_b_out[31:24]),
  .f(reg_b_mux_out)
);
mux2 #(.width(1)) reg_c_mux
(
  .select(reg_c_mux_sel),
  .a(reg_c_out),
  .b(0),
  .f(reg_c_mux_out)
);
adder #(.width(8)) add
(
  .a(reg_a_mux_out),
  .b(reg_b_mux_out),
  .c_in(reg_c_mux_out),
  .c_out(reg_c_in),
  .f(adder_out)
);
demux4 #(.width(8)) add_demux
(
  .select(add_demux_sel),
  .f(adder_out),
  .a(reg_out_0_in),
  .b(reg_out_1_in),
  .c(reg_out_2_in),
  .d(reg_out_3_in)
);

always_comb begin : next_state_logic
  next_state = state;
  case(state)
    idle : begin
      if(start == 1'b1) begin
        next_state = add_b0;
      end
    end
    add_b0 : begin
      next_state = add_b1;
    end
    add_b1 : begin
      next_state = add_b2;
    end
    add_b2 : begin
      next_state = add_b3;
    end
    add_b3 : begin
      next_state = complete;
    end
    complete : begin
      next_state = idle;
    end
    default : next_state = idle;
  endcase
end : next_state_logic

always_comb begin : control_logic
  ready = 0;
  load_a = 0;
  load_b = 0;
  load_c = 0;
  load_reg_out_0 = 0;
  load_reg_out_1 = 0;
  load_reg_out_2 = 0;
  load_reg_out_3 = 0;
  reg_a_mux_sel = 0;
  reg_b_mux_sel = 0;
  add_demux_sel = 0;
  reg_c_mux_sel = 0;

  case(state)
    idle : begin
      if(start == 1'b1) begin
        load_a = 1'b1;
        load_b = 1'b1;
        reg_c_mux_sel = 1'b1;
      end
    end
    add_b0 : begin
      load_c = 1'b1;
      reg_c_mux_sel = 1'b1;
      load_reg_out_0 = 1'b1;
    end
    add_b1 : begin
      reg_a_mux_sel = 2'b01;
      reg_b_mux_sel = 2'b01;
      add_demux_sel = 2'b01;
      load_c = 1'b1;
      load_reg_out_1 = 1'b1;
    end
    add_b2 : begin
      reg_a_mux_sel = 2'b10;
      reg_b_mux_sel = 2'b10;
      add_demux_sel = 2'b10;
      load_c = 1'b1;
      load_reg_out_2 = 1'b1;
    end
    add_b3 : begin
      reg_a_mux_sel = 2'b11;
      reg_b_mux_sel = 2'b11;
      add_demux_sel = 2'b11;
      load_c = 1'b1;
      load_reg_out_3 = 1'b1;
    end
    complete : begin
      ready = 1'b1;
    end
    default : /* Do Nothing */;
  endcase
end : control_logic

assign overflow = reg_c_out; 
/* verilator lint_off BLKSEQ */
always @ (posedge clk) begin
  if(rst == 1'b1) begin
    state = idle;
  end
  else begin
    state = next_state;
  end
end
/* verilator lint_on BLKSEQ */

endmodule;


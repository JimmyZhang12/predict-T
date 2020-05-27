# SUPPLY

class Supply:
  vid = 0
  v_bulk = 0
  v_proc = 0
  i_inst = 0

  proc_max_i = 0
  proc_min_i = 0

  proc_max_v = 0
  proc_min_v = 0

  rpdn = 0
  rll = 0

  def __init__(self, rpdn, rll, vcc_max, vcc_min, imax, imin):
    self.rpdn = rpdn
    self.rll = rll
    self.proc_max_i = imax
    self.proc_min_i = imin
    self.proc_max_v = vcc_max
    self.proc_min_v = vcc_min
    self.vid = vcc_min + rll*imax

  def get_i(self):
    return self.i_inst

  def get_v(self):
    return self.v_bulk

  def get_v_proc(self):
    return self.v_proc

  def get_p(self):
    return self.i_inst*self.v_bulk

  def tick(self, i_proc):
    self.i_inst = i_proc
    self.v_proc = self.vid - self.rll*self.i_inst
    self.v_bulk = self.v_proc + self.rpdn*self.i_inst

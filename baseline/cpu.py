# CPU

class CPU:
  period = 0
  duty = 0
  slew_rate = 0
  amplitude = 0
  min_current = 0
  timestep = 1e-9
  time = 0
  t1 = 0
  inc = False

  current = 0

  def __init__(self, period, duty, slew_rate, amplitude, min_current):
    self.period = period
    self.slew_rate = slew_rate
    self.amplitude = amplitude
    self.min_current = min_current
    self.duty = duty

  def get_i(self):
    return self.current

  def increase(self):
    self.current = min(self.min_current+self.amplitude, self.current+self.slew_rate)

  def decrease(self):
    self.current = max(self.min_current, self.current-self.slew_rate)

  def tick(self):
    # Start with off:
    if(not self.inc and (self.time < self.t1 + (1-self.duty)*self.period)):
      self.decrease()
      self.time += self.timestep
      if(self.time >= self.t1 + (1-self.duty)*self.period):
        self.t1 = self.time
        self.inc = True
    if(self.inc and (self.time < self.t1 + (self.duty)*self.period)):
      self.increase()
      self.time += self.timestep
      if(self.time >= self.t1 + (1-self.duty)*self.period):
        self.t1 = self.time
        self.inc = False

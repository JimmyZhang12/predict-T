#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

#include "interprocess.h"

static void int_handler(int signum) {
  destroy_shm();
  exit(-1);
}

int main(int argc, char** argv) {
  create_shm(1,"verilog_inter_python");

  // Install Signal Handler:
  struct sigaction sa;
  sa.sa_handler = int_handler;
  sigaction(SIGINT, &sa, NULL);
  
  wait_driver_data();
  printf("%d, %d\n", get_voltage_setpoint(), get_effective_resistance());
  ack_driver_data();
  wait_driver_data();
  printf("%d, %d\n", get_voltage_setpoint(), get_effective_resistance());
  ack_driver_data();
  wait_driver_data();
  printf("%d, %d\n", get_voltage_setpoint(), get_effective_resistance());
  ack_driver_data();
  wait_driver_data();
  printf("%d, %d\n", get_voltage_setpoint(), get_effective_resistance());
  ack_driver_data();

  destroy_shm();
  return 0;
}

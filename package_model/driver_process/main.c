#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

#include "interprocess.h"

static void int_handler(int signum) {
  destroy_shm();
  exit(-1);
}

int main(int argc, char** argv) {
  create_shm(0, argv[1]);
  FILE* tv = fopen(argv[2], "r");
  float r = 0.0;
  float t, p;

  // Install Signal Handler:
  struct sigaction sa;
  sa.sa_handler = int_handler;
  sigaction(SIGINT, &sa, NULL);
  
  while(!feof(tv)) {
    fscanf(tv, "%f,%f,%f\n",&t,&r,&p);
    set_driver_signals(1.0, r, 0);
    get_voltage();
  }
  set_driver_signals(1.0, r, 1);
  get_voltage();

  destroy_shm();
  return 0;
}

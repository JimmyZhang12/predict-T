#ifndef INTERPROCESS_H
#define INTERPROCESS_H

#include <fcntl.h> 
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/shm.h> 
#include <sys/stat.h>
#include <unistd.h>
#include <semaphore.h>

#define NEW_DATA    1
#define NO_NEW_DATA 0    // Also doubles as the data was already consumed

#define SHM_LENGTH  sizeof(mapped)
#define SHM_NAME    "shm_verilator_frontend_test"

#define INIT        1
#define NINIT       0

typedef struct {
  uint64_t next_clk_cnt; // The clock count when to set the signals
  uint32_t a, b;         // The inputs to the adder
  uint32_t rst;          // Reset the adder
  uint32_t start;        // Start the adder
  uint32_t sim_over;     // Terminate Simulation
} v_incoming_signals;

typedef struct {
  uint64_t clk_cnt;      // Current Clock Count
  uint32_t res;          // Result of A+B
  uint32_t overflow;     // Overflow?
  uint32_t ready;        // Result Ready
} p_incoming_signals;

typedef struct {
  sem_t sem;
  uint8_t new_data;
  v_incoming_signals data;
} p_to_v;

typedef struct {
  sem_t sem;
  uint8_t new_data;
  p_incoming_signals data;
} v_to_p;

typedef struct {
// Process to Verilog Sim
  p_to_v pv;
// Verilog Sim to Process
  v_to_p vp;
} mapped;

// shm_create
//   Creates, mmaps and initializes data/mutexes in shared mem region if INIT.
//   Opens shm and mmaps if !INIT
// Returns:
//   ptr to shared mem struct on success
//   NULL on failure
mapped* create_shm(int process);

// shm_destroy
//   Unmaps and Unlinks shared memory region
// Input:
//   ptr to shared mem region
void destroy_shm(mapped* shm_ptr);

#endif

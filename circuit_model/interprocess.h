/*
 * Copyright (c) 2020 Andrew Smith
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

/*
 * interprocess.h
 *
 * This file contains the prototypes for the shared memory structures and VPI
 * routines
 */

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
//#define SHM_NAME    "shm_cadence"

#define INIT        1
#define NINIT       0

typedef struct {
  double v_set;          // The next voltage setpoint
  double curr_load;      // The current load of the system
  double prediction;     // The value of the predicted load
  uint32_t enable;       // Enable the Aux Circuit
  uint32_t sim_over;     // Terminate Simulation
} v_incoming_signals;

typedef struct {
  double curr_v;         // Current Voltage From the Sim
  double curr_i;         // Current Current From the Sim
  uint32_t sim_done;     // Terminate Simulation
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
int create_shm(int process, char* name);

// shm_destroy
//   Unmaps and Unlinks shared memory region
// Input:
//   ptr to shared mem region
void destroy_shm();

void wait_driver_data();
double get_voltage_setpoint();
double get_load();
uint32_t get_terminate_simulation();
void ack_driver_data();
int send_voltage(double voltage);
int send_current(double current);

void set_driver_signals(double voltage_setpoint, double load, uint32_t terminate_sim);
double get_voltage();
double get_current();
void ack_supply();

#ifdef WITH_VPI
void register_create_shm();
void register_destroy_shm();
void register_wait_driver_data();
void register_get_voltage_setpoint();
void register_get_load();
void register_get_prediction();
void register_get_enable();
void register_get_terminate_simulation();
void register_ack_driver_data();
void register_send_voltage();
void register_send_current();
void register_ack_simulation();
#endif // WITH_VPI

#endif

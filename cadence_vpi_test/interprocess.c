#include <stdio.h>
#include "interprocess.h"
#ifdef WITH_VPI
#include "vpi_ams.h"
#include "vpi_user.h"
#include "vpi_user_cds.h"
#endif

int shm_fd = 0;

mapped* shm_ptr = NULL;

// shm_init
//   helper to initialize data/mutexes in mapped struct
void init_shm(mapped* p) {
	sem_init(&p->pv.sem, 1, 1);
	p->pv.new_data = NO_NEW_DATA;
	p->pv.data.v_set = 0;
	p->pv.data.curr_r_load = 0;
  p->pv.data.sim_over = 0;
  
	sem_init(&p->vp.sem, 1, 1);
	p->vp.new_data = NO_NEW_DATA;
	p->vp.data.curr_v = 0;
	p->vp.data.sim_done = 0;
}

// shm_create
//   Creates, mmaps and initializes data/mutexes in shared mem region if INIT.
//   Opens shm and mmaps if !INIT
// Returns:
//   ptr to shared mem struct on success
//   NULL on failure
void create_shm(int should_init) {
	mapped* shm_ptr = NULL;
  if(should_init == INIT) {
		shm_fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
		if(shm_fd == -1) {
			fprintf(stderr,"Failed to create & open /dev/shm/%s\n", SHM_NAME);
			exit(-1);
		}
		ftruncate(shm_fd, SHM_LENGTH);
		shm_ptr = (mapped*)mmap(NULL, SHM_LENGTH, PROT_WRITE | PROT_READ, MAP_SHARED, shm_fd, 0);
		if(shm_ptr == NULL) {
			fprintf(stderr,"mmap failed\n");
			shm_unlink(SHM_NAME);
			exit(-1);
		}
		// Initialize Data:
		init_shm(shm_ptr);
  }
  else {
		shm_fd = shm_open(SHM_NAME, O_RDWR, 0666);
		if(shm_fd == -1) {
			fprintf(stderr,"Failed to open /dev/shm/%s\n", SHM_NAME);
			exit(-1);
		}
		shm_ptr = (mapped*)mmap(NULL, SHM_LENGTH, PROT_WRITE | PROT_READ, MAP_SHARED, shm_fd, 0);
		if(shm_ptr == NULL) {
			fprintf(stderr,"mmap failed\n");
			shm_unlink(SHM_NAME);
			exit(-1);
		}
  }
}

// shm_destroy
//   Unmaps and Unlinks shared memory region
// Input:
//   ptr to shared mem region
void destroy_shm(mapped* shm_ptr) {
  munmap(shm_ptr, SHM_LENGTH);
  shm_unlink(SHM_NAME);
}

//*******************************************************************
//
// VPI Getters & Setter functions
//
//*******************************************************************
// driver_data_ready:
//   Call to block simulation until data is sent to it:
#ifdef WITH_VPI
void wait_driver_data() {
  while(1) {
    sem_wait(&shm_ptr->pv.sem);
    if(shm_ptr->pv.new_data == NEW_DATA) {
      sem_post(&shm_ptr->pv.sem);
      return;
    }
    sem_post(&shm_ptr->pv.sem);
  }
}

uint32_t get_size() {
  return sizeof(uint32_t);
}

// get_setpoint_voltage
//   get the new voltage setpoint:
static int get_voltage_setpoint() {
  vpiHandle systfref, argsiter, argh;
  struct t_vpi_value value;

  //systfref = vpi_handle(vpiSysTfCall, NULL); /* get system function that invoked C routine */
  //argsiter = vpi_iterate(vpiArgument, systfref);/* get iterator (list) of passed arguments */
  //argh = vpi_scan(argsiter);/* get the one argument - add loop for more args */
	//if(!argh){
  //  vpi_printf("$VPI missing parameter.\n");
  //  return 0;
  //}
    
  //value.format = vpiStringVal;
  //vpi_get_value(argh, &value);
  //char *s = value.value.str;
                
  ////Do shell command on DOS!
  //int result=reinterpret_cast<int>(ShellExecute(NULL, "open", s, NULL, NULL, SW_SHOWNORMAL));
  //value.value.integer = result;//;
  //value.format = vpiIntVal;/* return the result */

  //vpi_put_value(systfref, &value, NULL, vpiNoDelay);
  //vpi_free_object(argsiter);

  sem_wait(&shm_ptr->pv.sem);
  systfref = vpi_handle(vpiSysTfCall, NULL); /* get system function that invoked C routine */
  value.value.integer = (int)shm_ptr->pv.data.v_set;
  value.format = vpiIntVal;/* return the result */
  vpi_put_value(systfref, &value, NULL, vpiNoDelay);
  sem_post(&shm_ptr->pv.sem);
  return 0;
}

// get_setpoint_voltage
//   get the new voltage setpoint:
static int get_effective_resistance() {
  vpiHandle systfref, argsiter, argh;
  struct t_vpi_value value;

  sem_wait(&shm_ptr->pv.sem);
  systfref = vpi_handle(vpiSysTfCall, NULL); /* get system function that invoked C routine */
  value.value.integer = (int)shm_ptr->pv.data.curr_r_load;
  value.format = vpiIntVal;/* return the result */
  vpi_put_value(systfref, &value, NULL, vpiNoDelay);
  sem_post(&shm_ptr->pv.sem);
  return 0;
}

// get_terminate_simulation
//   get the new voltage setpoint:
uint32_t get_terminate_simulation() {
  sem_wait(&shm_ptr->pv.sem);
  uint32_t term = shm_ptr->pv.data.sim_over; 
  sem_post(&shm_ptr->pv.sem);
  return term;
}

// ack_driver_data
void ack_driver_data() {
  sem_wait(&shm_ptr->pv.sem);
  shm_ptr->pv.new_data = NO_NEW_DATA; 
  sem_post(&shm_ptr->pv.sem);
}

void send_powersupply_stats(uint32_t voltage) {
  sem_wait(&shm_ptr->vp.sem);
  shm_ptr->vp.data.curr_v = voltage;
  shm_ptr->vp.new_data = NEW_DATA;
  sem_post(&shm_ptr->vp.sem);

  // Wait for ack:
  while(1) {
    sem_wait(&shm_ptr->vp.sem);
    if(shm_ptr->vp.new_data == NO_NEW_DATA) {
      sem_post(&shm_ptr->vp.sem);
      return;
    }
    sem_post(&shm_ptr->vp.sem);
  }
}

#endif

void set_driver_signals(uint32_t voltage_setpoint, uint32_t resistance) {
  // Wait for the verilog simulation to consume the previous data:
  while(1) {
    sem_wait(&shm_ptr->pv.sem);
    if(shm_ptr->pv.new_data == NO_NEW_DATA) {
      shm_ptr->pv.data.v_set = voltage_setpoint;
      shm_ptr->pv.data.curr_r_load = resistance;
      shm_ptr->pv.new_data = NEW_DATA;
      sem_post(&shm_ptr->pv.sem);
      return;
    }
    sem_post(&shm_ptr->pv.sem);
  }
}

#ifdef WITH_VPI

// register_create_shm
void register_create_shm() {
    s_vpi_systf_data data;
    data.type = vpiSysTask;
    data.tfname ="$create_shm";
    data.calltf=create_shm;
    data.compiletf=0;
    data.sizetf=0;
    data.user_data=0;
    vpi_register_systf(&data);
}

// register_destroy_shm
void register_destroy_shm() {
    s_vpi_systf_data data;
    data.type = vpiSysTask;
    data.tfname ="$destroy_shm";
    data.calltf=destroy_shm;
    data.compiletf=0;
    data.sizetf=0;
    data.user_data=0;
    vpi_register_systf(&data);
}

// register_wait_driver_data
void register_wait_driver_data() {
    s_vpi_systf_data data;
    data.type = vpiSysTask;
    data.tfname ="$wait_driver_data";
    data.calltf=wait_driver_data;
    data.compiletf=0;
    data.sizetf=0;
    data.user_data=0;
    vpi_register_systf(&data);
}

// register_wait_driver_data
void register_get_voltage_setpoint() {
    s_vpi_systf_data data;
    data.type = vpiSysFunc;
    data.sysfunctype = vpiIntFunc;
    data.tfname ="$get_voltage_setpoint";
    data.user_data ="$get_voltage_setpoint";
    data.calltf=get_voltage_setpoint;
    data.compiletf=0;
    data.sizetf=get_size;
    data.user_data=0;
    vpi_register_systf(&data);
}

// register_wait_driver_data
void register_get_effective_resistance() {
    s_vpi_systf_data data;
    data.type = vpiSysFunc;
    data.sysfunctype = vpiIntFunc;
    data.tfname ="$get_effective_resistance";
    data.user_data ="$get_effective_resistance";
    data.calltf=get_effective_resistance;
    data.compiletf=0;
    data.sizetf=get_size;
    data.user_data=0;
    vpi_register_systf(&data);
}

// register_wait_driver_data
void register_get_terminate_simulation() {
    s_vpi_systf_data data;
    data.type = vpiSysFunc;
    data.sysfunctype = vpiIntFunc;
    data.tfname ="$get_terminate_simulation";
    data.calltf=get_terminate_simulation;
    data.compiletf=0;
    data.sizetf=get_size;
    data.user_data=0;
    vpi_register_systf(&data);
}

// register_ack_driver_data
void register_ack_driver_data() {
    s_vpi_systf_data data;
    data.type = vpiSysTask;
    data.tfname ="$ack_driver_data";
    data.calltf=ack_driver_data;
    data.compiletf=0;
    data.sizetf=0;
    data.user_data=0;
    vpi_register_systf(&data);
}

void register_send_powersupply_stats() {
    s_vpi_systf_data data;
    data.type = vpiSysTask;
    data.tfname ="$send_powersupply_stats";
    data.calltf=send_powersupply_stats;
    data.compiletf=0;
    data.sizetf=0;
    data.user_data=0;
    vpi_register_systf(&data);
}

#endif // WITH_VPI

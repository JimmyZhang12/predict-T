#include "interprocess.h"

int shm_fd = 0;

// shm_init
//   helper to initialize data/mutexes in mapped struct
void shm_init(mapped* p) {
	pthread_mutex_init(&p->pv.mutex);
	p->pv.new_data = NO_NEW_DATA;
	p->pv.data.next_clk_cnt = 0;
	p->pv.data.a = 0;
	p->pv.data.b = 0;
	p->pv.data.rst = 0;
	p->pv.data.start = 0;
  p->pv.data.sim_over = 0;
  
	pthread_mutex_init(&p->vp.mutex);
	p->vp.new_data = NO_NEW_DATA;
	p->vp.data.clk_cnt = 0;
	p->vp.data.res = 0;
	p->vp.data.overflow = 0;
	p->vp.data.ready = 0;
}

// shm_create
//   Creates, mmaps and initializes data/mutexes in shared mem region if INIT.
//   Opens shm and mmaps if !INIT
// Returns:
//   ptr to shared mem struct on success
//   NULL on failure
mapped* shm_create(int should_init) {
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
		shm_init(shm_ptr);
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
	return shm_ptr;
}

// shm_destroy
//   Creates, mmaps and initializes data/mutexes in shared mem region if INIT.
//   Opens shm and mmaps if !INIT
// Input:
//   ptr to shared mem region
// Returns:
//   1 on success
//   0 on error
int shm_destroy(int process, mapped* shm_ptr) {
	if(should_init == INIT) {
		
	}
	else {

  }
}

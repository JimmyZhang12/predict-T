#include <iostream>
#include <string>
#include <vector>
#include <list>
#include <math.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <cstdint>

#define LOOP_LEN 100000000000

#ifdef INT_ADD_TEST
void* test(void* arg) {
  int64_t a[16] = {0};
  int64_t b[16] = {0};
  int64_t c[16] = {0};

  // Init:
  for(int64_t i = 0; i < 16; i++) {
    a[i] = rand();
    b[i] = rand();
  }

  for(int64_t i = 0; i < LOOP_LEN; i++) {
    c[0] = a[0] + b[0];
    c[1] = a[1] + b[1];
    c[2] = a[2] + b[2];
    c[3] = a[3] + b[3];
    c[4] = a[4] + b[4];
    c[5] = a[5] + b[5];
    c[6] = a[6] + b[6];
    c[7] = a[7] + b[7];
    c[8] = a[8] + b[8];
    c[9] = a[9] + b[9];
    c[10] = a[10] + b[10];
    c[11] = a[11] + b[11];
    c[12] = a[12] + b[12];
    c[13] = a[13] + b[13];
    c[14] = a[14] + b[14];
    c[15] = a[15] + b[15];
  }
}
#endif

#ifdef INT_MUL_TEST
void* test(void* arg) {
  int64_t a[16] = {0};
  int64_t b[16] = {0};
  int64_t c[16] = {0};

  // Init:
  for(int64_t i = 0; i < 16; i++) {
    a[i] = rand();
    b[i] = rand();
  }

  for(int64_t i = 0; i < LOOP_LEN; i++) {
    c[0] = a[0] * b[0];
    c[1] = a[1] * b[1];
    c[2] = a[2] * b[2];
    c[3] = a[3] * b[3];
    c[4] = a[4] * b[4];
    c[5] = a[5] * b[5];
    c[6] = a[6] * b[6];
    c[7] = a[7] * b[7];
    c[8] = a[8] * b[8];
    c[9] = a[9] * b[9];
    c[10] = a[10] * b[10];
    c[11] = a[11] * b[11];
    c[12] = a[12] * b[12];
    c[13] = a[13] * b[13];
    c[14] = a[14] * b[14];
    c[15] = a[15] * b[15];
  }
}
#endif

#ifdef DOUBLE_ADD_TEST
void* test(void* arg) {
  double a[16] = {0};
  double b[16] = {0};
  double c[16] = {0};

  // Init:
  for(int64_t i = 0; i < 16; i++) {
    a[i] = (double)rand()/(double)rand();
    b[i] = (double)rand()/(double)rand();
  }

  for(int64_t i = 0; i < LOOP_LEN; i++) {
    c[0] = a[0] + b[0];
    c[1] = a[1] + b[1];
    c[2] = a[2] + b[2];
    c[3] = a[3] + b[3];
    c[4] = a[4] + b[4];
    c[5] = a[5] + b[5];
    c[6] = a[6] + b[6];
    c[7] = a[7] + b[7];
    c[8] = a[8] + b[8];
    c[9] = a[9] + b[9];
    c[10] = a[10] + b[10];
    c[11] = a[11] + b[11];
    c[12] = a[12] + b[12];
    c[13] = a[13] + b[13];
    c[14] = a[14] + b[14];
    c[15] = a[15] + b[15];
  }
}
#endif

#ifdef DOUBLE_MUL_TEST
void* test(void* arg) {
  double a[16];
  double b[16];
  double c[16];

  // Init:
  for(int64_t i = 0; i < 16; i++) {
    a[i] = (double)rand()/(double)rand();
    b[i] = (double)rand()/(double)rand();
  }

  for(int64_t i = 0; i < LOOP_LEN; i++) {
    c[0] = a[0] * b[0];
    c[1] = a[1] * b[1];
    c[2] = a[2] * b[2];
    c[3] = a[3] * b[3];
    c[4] = a[4] * b[4];
    c[5] = a[5] * b[5];
    c[6] = a[6] * b[6];
    c[7] = a[7] * b[7];
    c[8] = a[8] * b[8];
    c[9] = a[9] * b[9];
    c[10] = a[10] * b[10];
    c[11] = a[11] * b[11];
    c[12] = a[12] * b[12];
    c[13] = a[13] * b[13];
    c[14] = a[14] * b[14];
    c[15] = a[15] * b[15];
  }
}
#endif

#ifdef MEM
#define MB 1048576
void* test(void* arg) {
  // Perform random operations on a large vector to stress memory subsystem

  std::vector<double> data(1*MB);
  std::vector<int> keysa(MB/2);
  std::vector<int> keysb(MB/2);
  std::vector<int> keysc(MB/2);
  std::cout << "Finished Alloc" << "\n";

  // Init:
  for(int64_t i = 0; i < data.size(); i++) {
    data[i] = (double)rand()/(double)rand();
  }
  for(int64_t i = 0; i < keysa.size(); i++) {
    keysa[i] = rand()%data.size();
    keysb[i] = rand()%data.size();
    keysc[i] = rand()%data.size();
  }
  std::cout << "Finished Init" << "\n";

  for(int j = 0; j < 1000; j++) {
    for(int64_t i = 0; i < keysa.size(); i++) {
      data[keysa[i]] = data[keysb[i]] * data[keysc[i]];
    }
  }
  std::cout << "Finished Test" << "\n";
}
#endif

#ifdef CACHE_COHERENCE
#define MB 1048576
double data[16];
uint64_t m = 0;

volatile uint64_t spinlock(uint64_t * block) {
  uint64_t value;
	do {
    value = 1;
    __asm__ __volatile__( "xchgq %1,%0" : "=r" (value) : "m" (*block), "0" (value) : "memory");
  } while(value != 1);
  return value;
}

volatile void spinunlock(uint64_t * block) {
  uint64_t value = 0;
  __asm__ __volatile__( "movq %1,%0" : "=r" (value) : "m" (*block), "0" (value) : "memory");
}

void* test(void* arg) {
  // Perform random operations on a large vector to stress memory subsystem

  std::vector<int> keysa(MB/2);
  std::vector<int> keysb(MB/2);
  std::vector<int> keysc(MB/2);
  std::cout << "Finished Alloc" << "\n";

  // Init:
  for(int64_t i = 0; i < 16; i++) {
    data[i] = (double)rand()/(double)rand();
  }
  for(int64_t i = 0; i < keysa.size(); i++) {
    keysa[i] = rand()%16;
    keysb[i] = rand()%16;
    keysc[i] = rand()%16;
  }
  std::cout << "Finished Init" << "\n";

  for(int j = 0; j < 1000; j++) {
    for(int64_t i = 0; i < keysa.size(); i++) {
      spinlock(&m);
      data[keysa[i]] = data[keysb[i]] * data[keysc[i]];
      spinunlock(&m);
    }
  }
  std::cout << "Finished Test" << "\n";
}
#endif

#ifdef SLEEP
void* test(void* arg) {
  // Perform random operations on a large vector to stress memory subsystem

  for(int64_t i = 0; i < 10; i++) {
    sleep(2);
  }
}
#endif

#ifdef PHASES
#define MB 1048576
void* test(void* arg) {
  // Perform random operations on a large vector to stress memory subsystem
  int64_t a[16] = {0};
  int64_t b[16] = {0};
  int64_t c[16] = {0};
  double d[16] = {0.0};
  double e[16] = {0.0};
  double f[16] = {0.0};
  std::vector<double> data(16*MB);
  std::vector<int> keysa(2*MB);
  std::vector<int> keysb(2*MB);
  std::vector<int> keysc(2*MB);
  std::cout << "Finished Alloc" << "\n";

  // Init:
  for(int64_t i = 0; i < data.size(); i++) {
    data[i] = (double)rand()/(double)rand();
  }
  for(int64_t i = 0; i < keysa.size(); i++) {
    keysa[i] = rand()%data.size();
    keysb[i] = rand()%data.size();
    keysc[i] = rand()%data.size();
  }

  // Init:
  for(int64_t i = 0; i < 16; i++) {
    a[i] = rand();
    b[i] = rand();
    a[i] = (double)rand()/(double)rand();
    b[i] = (double)rand()/(double)rand();
  }
  std::cout << "Finished Init" << "\n";

  for(int j = 0; j < 10; j++) {
    std::cout << "INT STRESS" << "\n";
    for(int64_t i = 0; i < 100000; i++) {
      c[0] = a[0] * b[0];
      c[1] = a[1] * b[1];
      c[2] = a[2] * b[2];
      c[3] = a[3] * b[3];
      c[4] = a[4] * b[4];
      c[5] = a[5] * b[5];
      c[6] = a[6] * b[6];
      c[7] = a[7] * b[7];
      c[8] = a[8] * b[8];
      c[9] = a[9] * b[9];
      c[10] = a[10] * b[10];
      c[11] = a[11] * b[11];
      c[12] = a[12] * b[12];
      c[13] = a[13] * b[13];
      c[14] = a[14] * b[14];
      c[15] = a[15] * b[15];
    }

    std::cout << "IDLE" << "\n";
    sleep(1);

    std::cout << "FPU STRESS" << "\n";
    for(int64_t i = 0; i < 100000; i++) {
      c[0] = a[0] * b[0];
      c[1] = a[1] * b[1];
      c[2] = a[2] * b[2];
      c[3] = a[3] * b[3];
      c[4] = a[4] * b[4];
      c[5] = a[5] * b[5];
      c[6] = a[6] * b[6];
      c[7] = a[7] * b[7];
      c[8] = a[8] * b[8];
      c[9] = a[9] * b[9];
      c[10] = a[10] * b[10];
      c[11] = a[11] * b[11];
      c[12] = a[12] * b[12];
      c[13] = a[13] * b[13];
      c[14] = a[14] * b[14];
      c[15] = a[15] * b[15];
    }

    std::cout << "IDLE" << "\n";
    sleep(1);

    std::cout << "CACHE" << "\n";
    for(int j = 0; j < 10; j++) {
      for(int64_t i = 0; i < keysa.size(); i++) {
        data[keysa[i]] = data[keysb[i]] * data[keysc[i]];
      }
    }

    std::cout << "IDLE" << "\n";
    sleep(1);
  }
}
#endif

int main() {
#if (NTHREADS>1)
  pthread_t threads[NTHREADS];
  for(int i = 0; i < NTHREADS; i++) {
    pthread_create(&threads[i], NULL, test, NULL);
  }

  // Join Tthreads:
  for(int i = 0; i < NTHREADS; i++) {
    pthread_join(threads[i], NULL);
  }
#else
  test(NULL);
#endif
	return 0;
}

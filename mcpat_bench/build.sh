g++ mb.cc -std=c++11 -DNTHREADS=$1 -DINT_ADD_TEST -lpthread -O0 -o mb_int_add
g++ mb.cc -std=c++11 -DNTHREADS=$1 -DINT_MUL_TEST -lpthread -O0 -o mb_int_mul
g++ mb.cc -std=c++11 -DNTHREADS=$1 -DDOUBLE_ADD_TEST -lpthread -O0 -o mb_double_add
g++ mb.cc -std=c++11 -DNTHREADS=$1 -DDOUBLE_MUL_TEST -lpthread -O0 -o mb_double_mul
g++ mb.cc -std=c++11 -DNTHREADS=$1 -DMEM -lpthread -O0 -o mb_mem
g++ mb.cc -std=c++11 -DNTHREADS=$1 -DSLEEP -lpthread -O0 -o mb_sleep
g++ mb.cc -std=c++11 -DNTHREADS=$1 -DPHASES -lpthread -O0 -o mb_phases
g++ mb.cc -std=c++11 -DNTHREADS=$1 -DCACHE_COHERENCE -lpthread -O0 -o mb_cache_coherence

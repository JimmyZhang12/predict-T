#include "hello.h"
#include <stdio.h>

void hello_world(int a) {
  printf("Hello World from C: %d\n", a);
  hello_world_v(a);
}

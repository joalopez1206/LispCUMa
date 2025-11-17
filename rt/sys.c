#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

typedef uint64_t u64;
typedef u64 VAL;
void print(VAL val);
const u64 BOOL_TAG   = 0x0000000000000001;
const u64 BOOL_TRUE  = 0x8000000000000001;
const u64 BOOL_FALSE = 0x0000000000000001;

void print(VAL val){
  if((val & BOOL_TAG) == 0) {
    u64 result = (u64) val / 2;
    printf("%ld\n", result);
  }
  else if (val==BOOL_TRUE) {
    printf("true\n");
  }
  else if (val==BOOL_FALSE){
    printf("false\n");
  }
  else {
    printf("Unknown Value: %ld\n", val);
  }
}

extern u64 our_code_starts_here() asm("our_code_starts_here");

int main(int argc, char** argv) {
  u64 result = our_code_starts_here();
  print(result);
  return 0;
}
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

int cmp(const void *a, const void *b) {
  int *x = (int *)a;
  int *y = (int *)b;
  return *x - *y;
}

int main(int argc, char *argv[]) {
  if (argc != 2) {
    printf("Usage: executable_name input_file\n");
    return 1;
  }

  FILE *input_file = fopen(argv[1], "r");
  if (input_file == NULL) {
    printf("File %s not found\n", argv[1]);
    return 1;
  }

  int *left_list = malloc(1000 * sizeof(int));
  int *right_list = malloc(1000 * sizeof(int));
  int left, right;
  int len = 0;
  while (fscanf(input_file, "%d %d", &left, &right) != EOF) {
    left_list[len] = left;
    right_list[len] = right;
    ++len;
  }
  fclose(input_file);

  qsort(left_list, len, sizeof(int), cmp);
  qsort(right_list, len, sizeof(int), cmp);

  int p1_total = 0;
  for (size_t i = 0; i < len; ++i) {
    p1_total += abs(left_list[i] - right_list[i]);
  }
  printf("p1: %d\n", p1_total);

  int p2_total = 0;
  size_t li = 0, ri = 0;
  while (li < len && ri < len) {
    int left = left_list[li];
    size_t r_count = 0;
    while (ri < len && right_list[ri] <= left) {
      if (right_list[ri] == left) {
        ++r_count;
      }
      ++ri;
    }

    size_t l_count = 0;
    while (li < len && left_list[li] == left) {
      ++l_count;
      ++li;
    }

    p2_total += l_count * r_count * left;
  }
  printf("p2: %d\n", p2_total);

  return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int parse_int(char *input, unsigned *value) {
  *value = 0;
  int position = 0;
  while (input[position] != '\0') {
    if (input[position] < '0' || input[position] > '9') {
      break;
    }
    *value = *value * 10 + input[position] - '0';
    ++position;
  }
  return position;
}

unsigned parse_mul(char *input, int len) {
  int position = 0;

  if (position + 3 >= len || input[position++] != 'm' ||
      input[position++] != 'u' || input[position++] != 'l' ||
      input[position++] != '(') {
    return 0;
  }

  unsigned first, second;
  int parsed_chars = parse_int(input + position, &first);
  if (parsed_chars == 0) {
    return 0;
  }

  position += parsed_chars;
  if (position >= len || input[position++] != ',') {
    return 0;
  }

  parsed_chars = parse_int(input + position, &second);
  if (parsed_chars == 0) {
    return 0;
  }

  position += parsed_chars;
  if (position >= len || input[position++] != ')') {
    return 0;
  }

  return first * second;
}

int parse_enabled(char *input, int len, int current_value) {
  if (len < 2 || strncmp(input, "do", 2) != 0) {
    return current_value;
  }
  if (len >= 4 && strncmp(input + 2, "()", 2) == 0) {
    return 1;
  }
  if (len >= 7 && strncmp(input + 2, "n't()", 5) == 0) {
    return 0;
  }
  return current_value;
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

  char *input = malloc(20000 * sizeof(char));

  int c, len = 0;
  while ((c = fgetc(input_file)) != EOF) {
    input[len++] = (char)c;
  }
  input[len] = '\0';

  int i = 0;
  unsigned p1_total = 0;
  while (i < len) {
    unsigned total = parse_mul(input + i, len - i);
    if (total > 0) {
      p1_total += total;
    }
    ++i;
  }

  printf("p1: %u\n", p1_total);

  i = 0;
  int enabled = 1;
  unsigned p2_total = 0;
  while (i < len) {
    enabled = parse_enabled(input + i, len - i, enabled);

    if (enabled == 1) {
      unsigned total = parse_mul(input + i, len - i);
      if (total > 0) {
        p2_total += total;
      }
    }

    ++i;
  }

  printf("p2: %u\n", p2_total);

  return 0;
}

import sys
import os

CODEWORDS = [
  "000",
  "001",
  "010",
  "011",
  "101",
  "100",
  "110",
  "111"
]

CODEWORDS1 = [
  0,
  1,
  2,
  3,
  4,
  5,
  6,
  7
]

def paridad_par_str(codewords):
  result = {}
  for i, word in enumerate(codewords):
    ones = paridad_par(word)
    bit = "1" if ones % 2 != 0 else "0"
    result[word] = word + bit
  return result

def paridad_par(word):
  return sum(1 for bit in word if bit == "1")


def paridad_par_int(codewords):
  result = {}
  for i, v in enumerate(codewords):
    ones = paridad_par_1(v)
    bit = "1" if ones % 2 else "0"
    result[i] = f"{v:03b}" + bit
  return result

def paridad_par_1(v):
    count = 0
    n = v
    while n > 0:
      count += n & 1
      n >>= 1
    return count

def hamming(codewords):
  dist_min = 10000000
  for i, word in enumerate(codewords):
    for j, word_par in enumerate(codewords):
      if word != word_par:
        dist_min = min(dist_min, hamming_distance(codewords[word], codewords[word_par]))
  return dist_min

def hamming_distance(word, word_1):
  return sum(1 for a, b in zip(word, word_1) if a != b)

if __name__ == "__main__":
  words_valid = paridad_par_str(CODEWORDS)
  print(CODEWORDS)
  print(words_valid)
  print(hamming(words_valid))
  words_valid = paridad_par_int(CODEWORDS1)
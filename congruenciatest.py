def congruential_mixed(a, c, m, seed):
  """
  Simulates a congruential mixed linear generator.

  Args:
      a: Multiplier constant.
      c: Increment constant.
      m: Modulus.
      seed: Initial seed value.

  Returns:
      The next random number in the sequence.
  """
  while True:
    seed = (a * seed + c) % m
    yield seed / m

# Example usage
generator = congruential_mixed(a=5, c=7, m=8, seed=6)
for _ in range(1):
  print(next(generator))

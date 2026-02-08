from typing import List

Vector = List[float]
def add(v: Vector, w: Vector) -> Vector:
    return [v_i + w_i for v_i, w_i in zip(v, w)]

v = [1, 2, 3]
w = [4, 5, 6]

# Print the result
print(add(v, w))   # Output: [5, 7, 9]


def subtract(v: Vector, w: Vector) -> Vector:
    return [v_i - w_i for v_i, w_i in zip(v, w)]

# Define vectors
v = [5, 7, 9]
w = [9, 5, 6]

# Validate and print result
print(subtract(v, w))   # Output: [1, 2, 3]


def dot(v: Vector, w: Vector) -> float:
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

# Validate and print
print("Dot product is:", dot([1, 2, 3], [4, 5, 6]))


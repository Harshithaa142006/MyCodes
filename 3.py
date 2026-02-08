from typing import List
import math
from collections import Counter

def _median_odd(xs: List[float]) -> float:
    """Internal helper: median for odd-length list."""
    sorted_xs = sorted(xs)
    mid = len(sorted_xs) // 2
    return sorted_xs[mid]

def _median_even(xs: List[float]) -> float:
    """Internal helper: median for even-length list."""
    sorted_xs = sorted(xs)
    hi_mid = len(xs) // 2
    return (sorted_xs[hi_mid - 1] + sorted_xs[hi_mid]) / 2.0

def median(v: List[float]) -> float:
    """Returns the median of list v."""
    if not v:
        raise ValueError("Cannot compute the median of an empty list.")
    return _median_even(v) if len(v) % 2 == 0 else _median_odd(v)

def mode(x: List[float]) -> List[float]:
    """Returns a list, since there might be more than one mode."""
    counts = Counter(x)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.items() if count == max_count]

def mean(xs: List[float]) -> float:
    return sum(xs) / len(xs)

def de_mean(xs: List[float]) -> List[float]:
    x_bar = mean(xs)
    return [x - x_bar for x in xs]

def sum_of_squares(xs: List[float]) -> float:
    return sum(x * x for x in xs)

def standard_deviation(xs: List[float]) -> float:
    """Sample standard deviation."""
    n = len(xs)
    assert n >= 2, "standard_deviation requires at least two elements"
    deviations = de_mean(xs)
    return math.sqrt(sum_of_squares(deviations) / (n - 1))

def dot(xs: List[float], ys: List[float]) -> float:
    return sum(x * y for x, y in zip(xs, ys))

def covariance(xs: List[float], ys: List[float]) -> float:
    """Sample covariance with Bessel's correction."""
    return dot(de_mean(xs), de_mean(ys)) / (len(xs) - 1)

def correlation(xs: List[float], ys: List[float]) -> float:
    """Pearson correlation coefficient. Returns 0 if no variation."""
    stdev_x = standard_deviation(xs)
    stdev_y = standard_deviation(ys)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(xs, ys) / (stdev_x * stdev_y)
    return 0.0

# Example usage:
num_friends = [10, 5, 7, 2, 9]
daily_minutes = [100, 50, 70, 20, 90]

print("Mean:", mean(num_friends))
print("Median:", median(num_friends))
print("Mode:", mode(num_friends))
print("Standard Deviation:", standard_deviation(num_friends))

corr_value = correlation(num_friends, daily_minutes)
print(f"Correlation: {corr_value:.2f}")

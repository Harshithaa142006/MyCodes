import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

a, b = 0, 10
x_cdf_uniform = np.linspace(-1, 12, 400)
uniform_cdf = np.where(x_cdf_uniform < a, 0, np.where(x_cdf_uniform < b, (x_cdf_uniform - a) / (b - a), 1))

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(x_cdf_uniform, uniform_cdf, label='Uniform CDF', color='blue')
plt.axvline(a, color='red', linestyle='--', label='a = 0')
plt.axvline(b, color='green', linestyle='--', label='b = 10')
plt.title('Uniform Cumulative Distribution Function (CDF)')
plt.xlabel('x')
plt.ylabel('F_X(x)')
plt.legend()
plt.grid()
plt.xlim(-1, 12)
plt.ylim(-0.1, 1.1)

mu, sigma = 0, 1
x_cdf_normal = np.linspace(-4, 4, 400)
normal_cdf = norm.cdf(x_cdf_normal, mu, sigma)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(x_cdf_normal, normal_cdf, label='Normal CDF', color='orange')
plt.axvline(mu, color='red', linestyle='--', label='Mean (μ = 0)')
plt.title('Normal Cumulative Distribution Function (CDF)')
plt.xlabel('x')
plt.ylabel('F_X(x)')
plt.legend()
plt.grid()
plt.xlim(-4, 4)
plt.ylim(-0.1, 1.1)

plt.show()

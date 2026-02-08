import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from textblob import TextBlob
import nltk
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('punkt_tab')

X = np.array([[1], [2], [3], [4], [5]])
y = np.array([40, 50, 60, 70, 80])

model = LinearRegression()
model.fit(X, y)

hours = np.array([[6]])
predicted_marks = model.predict(hours)
print(f"Predicted marks for 6 hours of study: {predicted_marks[0]:.2f}")

plt.scatter(X, y, color='blue', label='Actual data')
plt.plot(X, model.predict(X), color='red', label='Regression Line')
plt.xlabel('Hours Studied')
plt.ylabel('Marks Scored')
plt.title('Linear Regression Example')
plt.legend()
plt.grid(True)


text = "I love data science but somtimes it is challanging!"
blob = TextBlob(text)
print("Corrected text:", blob.correct())
print("Words:", blob.words)
plt.show()
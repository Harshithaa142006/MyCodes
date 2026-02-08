import random

def split_data(data, prob):
    results = [[], []]
    for row in data:
        results[0 if random.random() < prob else 1].append(row)
    return results

def train_test_split(x, y, test_pct):
    data = list(zip(x, y))
    train, test = split_data(data, 1 - test_pct)
    x_train, y_train = zip(*train) if train else ([], [])
    x_test, y_test = zip(*test) if test else ([], [])
    return list(x_train), list(x_test), list(y_train), list(y_test)

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_pct=0.2)

print("Training Features:", x_train)
print("Test Features:", x_test)
print("Training Labels:", y_train)
print("Test Labels:", y_test)

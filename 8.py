import math, re
from collections import defaultdict

def tokenize(message):
    message = message.lower()
    return re.findall("[a-z0-9']+", message)

def count_words(training_set):
    counts = defaultdict(lambda: [0, 0])
    for message, is_spam in training_set:
        for word in set(tokenize(message)):
            counts[word][0 if is_spam else 1] += 1
    return counts

def word_probabilities(counts, total_spams, total_hams, k=0.5):
    return [
        (w, (spam + k) / (total_spams + 2 * k), (ham + k) / (total_hams + 2 * k))
        for w, (spam, ham) in counts.items()
    ]

def spam_probability(word_probs, message):
    message_words = set(tokenize(message))
    log_prob_spam = log_prob_ham = 0.0
    for word, prob_spam, prob_ham in word_probs:
        if word in message_words:
            log_prob_spam += math.log(prob_spam)
            log_prob_ham += math.log(prob_ham)
        else:
            log_prob_spam += math.log(1 - prob_spam)
            log_prob_ham += math.log(1 - prob_ham)
    prob_spam = math.exp(log_prob_spam)
    prob_ham = math.exp(log_prob_ham)
    return prob_spam / (prob_spam + prob_ham)

class NaiveBayesClassifier:
    def __init__(self, k=0.5):
        self.k = k
        self.word_probs = []

    def train(self, training_set):
        num_spams = sum(1 for _, is_spam in training_set if is_spam)
        num_hams = len(training_set) - num_spams
        word_counts = count_words(training_set)
        self.word_probs = word_probabilities(word_counts, num_spams, num_hams, self.k)

    def classify(self, message):
        prob = spam_probability(self.word_probs, message)
        return ("SPAM" if prob > 0.5 else "HAM"), prob

if __name__ == "__main__":
    training_data = [
        ("Win money now!!!", True),
        ("Lowest price on car insurance", True),
        ("Call your mom today", False),
        ("Meeting at 10am", False),
        ("Earn dollars easily from home", True),
        ("Let's have lunch tomorrow", False)
    ]

    classifier = NaiveBayesClassifier()
    classifier.train(training_data)

    user_message = input("Enter a message to check: ")
    label, probability = classifier.classify(user_message)
    print(f"\nMessage classified as: {label}")
    print(f"Spam probability: {probability:.4f}")

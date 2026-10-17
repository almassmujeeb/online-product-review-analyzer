from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


def predict_sentiment(review):
    """
    Returns:
        Positive
        Negative
        Neutral
    """

    score = analyzer.polarity_scores(review)

    compound = score["compound"]

    if compound >= 0.05:
        return "Positive"

    elif compound <= -0.05:
        return "Negative"

    else:
        return "Neutral"


# Testing (optional)
if __name__ == "__main__":

    reviews = [
        "Excellent product. Highly recommended.",
        "Battery backup is average.",
        "Waste of money. Very bad quality."
    ]

    for r in reviews:
        print(r)
        print("Sentiment :", predict_sentiment(r))
        print("---------------------------")
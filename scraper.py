import random

def get_reviews(product_name):
    """
    Returns sample reviews from multiple platforms.
    """

    reviews = [

        {
            "platform": "Amazon",
            "rating": 5,
            "review": f"{product_name} is excellent. Battery backup is amazing."
        },

        {
            "platform": "Amazon",
            "rating": 4,
            "review": f"{product_name} has a good camera and display."
        },

        {
            "platform": "Flipkart",
            "rating": 5,
            "review": f"I highly recommend {product_name}. Excellent value for money."
        },

        {
            "platform": "Flipkart",
            "rating": 2,
            "review": f"{product_name} has heating issues after long use."
        },

        {
            "platform": "Myntra",
            "rating": 4,
            "review": f"{product_name} quality is good and delivery was fast."
        },

        {
            "platform": "Myntra",
            "rating": 3,
            "review": f"{product_name} is average. Packaging was okay."
        },

        {
            "platform": "Meesho",
            "rating": 5,
            "review": f"{product_name} is worth buying."
        },

        {
            "platform": "Meesho",
            "rating": 1,
            "review": f"{product_name} is waste of money."
        }

    ]

    random.shuffle(reviews)

    return reviews
from flask import Flask, render_template, request, redirect, session
import sqlite3

from scraper import get_reviews
from sentiment import predict_sentiment

app = Flask(__name__)
app.secret_key = "12345"


# ---------------------------------
# Database Connection
# ---------------------------------
def get_db():
    conn = sqlite3.connect("review.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------
# Login
# ---------------------------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        session["user"] = username
        return redirect("/dashboard")

    return render_template("login.html")


# ---------------------------------
# Dashboard
# ---------------------------------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    conn = get_db()

    reviews = conn.execute(
        """
        SELECT *
        FROM reviews
        WHERE username=?
        ORDER BY id DESC
        """,
        (session["user"],)
    ).fetchall()

    total_reviews = len(reviews)

    positive = sum(1 for r in reviews if r["sentiment"] == "Positive")
    negative = sum(1 for r in reviews if r["sentiment"] == "Negative")
    neutral = sum(1 for r in reviews if r["sentiment"] == "Neutral")

    platform_summary = conn.execute(
        """
        SELECT
            platform,
            ROUND(AVG(rating),1) AS avg_rating,
            COUNT(*) AS total_reviews,
            SUM(CASE WHEN sentiment='Positive' THEN 1 ELSE 0 END) AS positive_reviews,
            SUM(CASE WHEN sentiment='Negative' THEN 1 ELSE 0 END) AS negative_reviews,
            SUM(CASE WHEN sentiment='Neutral' THEN 1 ELSE 0 END) AS neutral_reviews
        FROM reviews
        WHERE username=?
        GROUP BY platform
        """,
        (session["user"],)
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        reviews=reviews,
        total_reviews=total_reviews,
        positive=positive,
        negative=negative,
        neutral=neutral,
        platform_summary=platform_summary
    )


# ---------------------------------
# Search Page
# ---------------------------------
@app.route("/search")
def search():

    if "user" not in session:
        return redirect("/")

    return render_template("search.html")


# ---------------------------------
# Search Review
# ---------------------------------
@app.route("/search_review", methods=["POST"])
def search_review():

    if "user" not in session:
        return redirect("/")

    product = request.form["product"]

    sample_reviews = get_reviews(product)

    conn = get_db()

    for item in sample_reviews:

        sentiment = predict_sentiment(item["review"])

        conn.execute(
            """
            INSERT INTO reviews
            (
                username,
                platform,
                product_name,
                rating,
                review,
                sentiment
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session["user"],
                item["platform"],
                product,
                item["rating"],
                item["review"],
                sentiment
            )
        )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ---------------------------------
# Visitor Page
# ---------------------------------
@app.route("/visitor")
def visitor():

    if "user" not in session:
        return redirect("/")

    conn = get_db()

    visitors = conn.execute("""
        SELECT
            username,
            product_name,
            platform,
            sentiment
        FROM reviews
        ORDER BY id DESC
    """).fetchall()

    total_visitors = len(visitors)

    total_visitors = len(visitors)

    visitors_today = max(1, total_visitors // 3)
    new_users = max(1, total_visitors // 5)
    page_views = total_visitors * 4

    conn.close()

    return render_template(
        "visitor.html",
    visitors=visitors,
    total_visitors=total_visitors,
    visitors_today=visitors_today,
    new_users=new_users,
    page_views=page_views
)


# ---------------------------------
# Logout
# ---------------------------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ---------------------------------
# Run Flask App
# ---------------------------------
if __name__ == "__main__":
    app.run(debug=True)
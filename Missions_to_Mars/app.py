from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mission_to_mars.find_one()

    # Return template and data
    return render_template("index.html", mission_to_mars=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scraper():

    # Run the scrape function
    # mission_to_mars = mongo.db.mission_to_mars
    mars_news=scrape_mars.scrape_news()
    mars_feature=scrape_mars.scrape_jpl_img()
    mars_fact=scrape_mars.scrape_fact()
    mars_hemi=scrape_mars.scrape_hemispheres()

    mars_data = {}
    # mars_data['mars_news'] = mars_news
    # mars_data['mars_feature'] = mars_feature
    # mars_data['mars_fact'] = mars_fact
    # mars_data['mars_hemi'] = mars_hemi
    for key, value in mars_news.items():
        mars_data[key] = value

    for key, value in mars_feature.items():
        mars_data[key] = value

    for key, value in mars_fact.items():
        mars_data[key] = value

    for key, value in mars_hemi.items():
        mars_data[key] = value

    # Update the Mongo database using update and upsert=True
    mongo.db.mission_to_mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

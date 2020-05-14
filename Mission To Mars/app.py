from flask import Flask, render_template, redirect
import scrape_mars

# from flask_pymongo import PyMongo
from flask_pymongo import PyMongo

# Create an instance of Flask
app = Flask(__name__)

# set inline
mongo = PyMongo(app, uri="mongodb://localhost:27017/MARS_app")

@app.route("/")
def index():
    
    # Find one record of data from the mongo database
    MARS_data = mongo.db.collection.find_one()

    return render_template("index.html", MARS_data = MARS_data)


@app.route("/scrape")
def scrape():

    # Run the scrape function
    MARS_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.replace_one({}, MARS_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=80, debug=True)


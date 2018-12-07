from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import pymongo
import scrape_mars

app = Flask(__name__)
# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db
collection = db.mars


@app.route('/')
def index():
    #mars = mongo.db.mars.find_one()
    mars = list(db.mars.find())

    # mars = client.db.mars.find_one()
    print("mars IS DONE")
    return render_template("index.html", mars=mars)

@app.route('/scrape')
def scrape():
    #mars = mongo.db.mars
    #mars = list(db.mars)
    mars_data = scrape_mars.scrape()
    print(mars_data)


    collection.update({}, mars_data, upsert=True)


    

    #mars.update(mars_data)

    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)

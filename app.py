from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import pymongo
import scrape_mars


#set up connection to mongo db
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db
mars_data = db.mars

#set up flask app
app = Flask(__name__)

@app.route('/')
def index():
    mars = list(db.mars.find())
    return render_template("index.html", mars=mars)

@app.route('/scrape')
def scrape():
    mars_data = scrape_mars.scrape()
    print(mars_data)
    mars_data.update({}, mars_data, upsert=True)

    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)

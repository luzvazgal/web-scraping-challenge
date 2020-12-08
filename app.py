from flask import Flask, render_template
import pymongo
import scrape_mars as sm

app = Flask(__name__)

#database connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
#Creating database everytime document is loaded (queried)
db = client.mars_db



@app.route("/")
def main():
    #Getting data from MongoDB
    mars_info = list(db.mars.find())
    print(mars_info)

    #Render data in index.htlm
    return render_template("index.html", teams=teams)
    return render_template("index.html", text=my_Text, 
    hobbies_list=hobbies, dictionary=player_dictionary)

@app.route("/scrape")
def scrape():
    #Dropping database if already exists
    db.mars.drop()

    #inserting dictionary coming from scrape function in scrape_mars.py
    db.mars.insert(sm.scrape())
   
   #Visualizing announcement data has been scrapped and inserted in Mongo
    return render_template("scrape.html")


if __name__ == "__main__":
    app.run(debug=True)
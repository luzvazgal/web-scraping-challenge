from flask import Flask, render_template
import pymongo

app = Flask(__name__)

#database connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
#Creating database everytime document is loaded (queried)
db = client.mars_db



@app.route("/")
def main():
    my_Text = "This data comes from Python!"
    hobbies = ["dancing", "exercise", "eating", "plants"]
    player_dictionary = {
        "player_1": "Jessica",
        "player_2": "Mark"
    }
    return render_template("index.html", text=my_Text, 
    hobbies_list=hobbies, dictionary=player_dictionary)

@app.route("/scrape")
def scrape():
    #Dropping database if already exists
    db.mars.drop()
    
    #inserting dictionary
    db.mars.insert()
   
    return render_template("scrape.html")


if __name__ == "__main__":
    app.run(debug=True)
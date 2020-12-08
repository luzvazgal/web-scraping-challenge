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
    mars_info = db.mars.find()
    print(mars_info)

    title=mars_info['Title']
    description= mars_info['Description']
    featured_url = mars_info['Featured_Image_URL']
    general_data= mars_info['General_Data']
    hemisphere_imgs = mars_info['Hemisphere_Images_URLs']
    
    return render_template("index.html", title=title, description=description, featured_image=featured_url, 
    general_data=general_data, hemisphere_images=hemisphere_imgs)


@app.route("/scrape")
def scrape():
    #Dropping database if already exists
    db.mars.drop()

    dictionary = sm.scrape()
    print(type(dictionary))

    #inserting dictionary coming from scrape function in scrape_mars.py
    db.mars.insert_many(dictionary)
   
   #Visualizing announcement data has been scrapped and inserted in Mongo
    return render_template("scrape.html")


if __name__ == "__main__":
    app.run(debug=True)
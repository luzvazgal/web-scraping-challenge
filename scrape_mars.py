

# Knowing more about Mars
#This function returns a dictionary containing all relevant data from Mars

#Importing required libraries
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
#To use Regular expressions in parsing HTML, the 're' library is required
import re as re
#Importing Pandas as it will be used to scrap tables
import pandas as pd




#Getting robot and load driver into cache
executable_path = {'executable_path': ChromeDriverManager().install()}
#option = webdriver.ChromeOptions()
#option.add_argument('--headless')
#driver = webdriver.Chrome(chrome_options=option)
browser = Browser('chrome', **executable_path, headless=False)

#URLs of sites to scrap
NASA_site = "https://mars.nasa.gov/news/"
JPL_site = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
MarsFacts_site = "https://space-facts.com/mars/"
USGS_site = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

#Defining scrape function to retrieve Mars data as a dicitonary

def scrape():

    #Scrapping NASA site
    browser.visit(NASA_site)
    html = browser.html

    nasa_soup = BeautifulSoup(html, "html.parser")

    ## NASA Mars News
    #NASA Web Scraping 

    #Scrapping NASA's news title and text
    nasa_news_title = nasa_soup.find('title').text
    nasa_news_p = nasa_soup.find('p').text

    ## JPL Mars Space Images - Featured Image
    #JPL Web Scraping

    #Scrapping JPL site
    browser.visit(JPL_site)
    html = browser.html

    jpl_soup = BeautifulSoup(html, "html.parser")


    #1. Getting the html code representing the featured image identified by:
    #<h2 class="brand_title">
    #          FEATURED IMAGE
    #        </h2>
    #Using find() method and regular expression  to find "main_feature" in document
    jpl_feature_section = jpl_soup.find('section', class_=re.compile("main_feature"))

    #Getting the anchor (a) where the id is the 'full_image' which represents the image location
    image_a_tag = jpl_feature_section.contents[1].find('a', id='full_image')

    #Getting the value of 'data-fancybox-href' attriburte in 'a' tag to form Image URL variable
    featured_image_url = "https://www.jpl.nasa.gov"+image_a_tag['data-fancybox-href']
   
    ## Mars Facts 
    #Mars Facts webscraping

    #Getting all tables from HTML and adding them to a set to ensure we don't have duplicates
    marsfacts_tables = pd.read_html(MarsFacts_site)

    #Tables parsed will be stored in an array
    tables_df = []

    #Iterating over table
    for table in marsfacts_tables:     
        if len(tables_df) ==0:
            tables_df.append(table)
        else:
            #Validating whether the current table df exists in array to prevent adding it
            for table_df in tables_df:
            #Checking if compared DataFrames have the same shapes; otherwise, they're not equal (duplicated)
                if table_df.equals(table):
                    break
                else:   
                    #Adding table DF to array
                    tables_df.append(table)
                    break

    #Displaying Pandas content as HTML
    #Writing an HTML file code with table embedded

    html_file = open("templates/table.html", "w") 
    html_file.write(tables_df[0].to_html()) 
    html_file.close()   

    ## Mars Hemispheres
    #Creating a dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"}
        ]


    
    #Variables to return
    #nasa_news_title - NASA News Mars Title
    #nasa_news_p - NAAS News text
    #featured_image_url - URL fo Mars Feature image
    #tables_df - all tables containing general information of Mars. The dictionary will only contain the general info
    #Hemisphere_image_urls - All four Mars hemispheres' images

    mars_data_dictionary = [{
        "Title":nasa_news_title,
        "Description":nasa_news_p,
        "Featured_Image_URL": featured_image_url,
        "General_Data": tables_df[0].to_html(index=False, header=False, justify="center", classes="cell_format"),
        "Hemisphere_Images_URLs": hemisphere_image_urls
    }]


    return mars_data_dictionary





# Import dependencies
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import requests



def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    
######## NASA MARS NEWS ########################################################
################################################################################

    nasa_mars_news_url = 'https://mars.nasa.gov/news/'
    response = requests.get(nasa_mars_news_url)
    soup = BeautifulSoup(response.text, "html5lib")
    results = soup.find_all(class_="slide")

    for result in results:
        try:
            # Identify and return title of listing
            news_title = result.find(class_="content_title").text
            # Identify and return price of listing
            news_descrip = result.find(class_="rollover_description_inner").text
            
        except AttributeError as e:
            print(e)
        
                
######## JPL MARS SPACE IMAGES - FEATURED IMAGE ###############################
################################################################################
    
    jpl_mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_mars_image_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    html = browser.html
    jpl_soup = BeautifulSoup(html, 'html.parser')
    
    #This line works in Jupyter Notebook, not as standalone Python.
    #image = jpl_soup.find_all(class_="fancybox-image")[0]['src']
    
    image_str = str(jpl_soup.find_all(class_="fancybox-image"))
    image_manip = image_str.split("\"")
    img_maybe = [x for x in image_manip if 'jpg' in x]
    img_maybe_str = str(img_maybe)
    #print(img_maybe_str)
    img_replace_leftbracket = img_maybe_str.replace("[","")
    img_replace_rightbracket = img_replace_leftbracket.replace("]","")
    img_replace_apos = img_replace_rightbracket.replace("'","")
    #featured_image_url = "https://www.jpl.nasa.gov" + img_replace_apos
    testing_jpl = 'https://www.jpl.nasa.gov'
    sentence = [testing_jpl, img_replace_apos]
    other = ''.join(map(str, sentence))
    #print(my_lst_str)
    
    
############ MARS WEATHER ######################################################
################################################################################
    
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    html = browser.html
    mars_w_soup = BeautifulSoup(html, 'html.parser')
    mars_weather = mars_w_soup.find_all(class_= "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[0].text


############ MARS FACTS ########################################################
################################################################################
    
    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url)
    marsfacts_df = tables[0]
    marsfacts_df.columns = ['Measurement', 'Fact']
    marsfacts_df.set_index('Measurement', inplace=True)
    marsfacts_html = marsfacts_df.to_html()
    
    # Converting tables to lists for web presentation
    tables = pd.read_html(mars_facts_url)
    marsfacts_df = tables[0]
    marsfacts_df.columns = ['Measurement', 'Fact']
    marsfacts_measurement = marsfacts_df["Measurement"].tolist()
    marsfacts_facts = marsfacts_df["Fact"].tolist()


############ MARS HEMISPHERES ##################################################
################################################################################

    usgs_astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_astrogeology_url)

    html = browser.html
    usgs_soup = BeautifulSoup(html, 'html.parser')

    #results = usgs_soup.findAll(True, {'class':['item', 'itemLink product-item', 'thumb']})
    results = usgs_soup.find_all(class_="item")

    img_url_list = []
    final_title_list = []


    for x in results:
        search_url = x.find_all('a')[0]['href']
        full_url = 'https://astrogeology.usgs.gov/' + search_url
        browser.visit(full_url)
        html = browser.html
        usgs_soup = BeautifulSoup(html, 'html.parser')
        test_results = usgs_soup.find_all(class_= 'downloads')
        planet_img = test_results[0].a['href']
        img_url_list.append(planet_img)
        titles = x.find_all('h3')
        for y in titles:
            final_title = y.text[:-9]
            final_title_list.append(final_title)
            
        final_list = []
        y = 0
        for x in final_title_list:
            final_dict = {"title": x, "img_url": img_url_list[y]}
            final_list.append(final_dict)
            y = y + 1
    
    #FINAL OUTPUT
    mars_data = {
        "news_title": news_title,
        "news_descrip": news_descrip,
        "other": other,
        "mars_weather": mars_weather,
        "marsfacts_html": marsfacts_html,
        "final_list": final_list,
        "marsfacts_measurement": marsfacts_measurement,
        "marsfacts_facts": marsfacts_facts
    }
    
    f = open("dict.txt","w")
    f.write( str(mars_data))
    f.close()
    
    # FINAL RETURN  
    print(mars_data)
     
    return mars_data


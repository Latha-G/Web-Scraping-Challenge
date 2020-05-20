import pandas as pd
import requests

import time
import re

from splinter import Browser
from bs4 import BeautifulSoup

def init_browser():
    
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def mars_weather(browser):
    
    #browser = init_browser()

    # Url of Mars Weather twitter account
    weather_url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(weather_url)
    time.sleep(3)
    
    weather_html = browser.html

    weather_soup = BeautifulSoup(weather_html, 'lxml')

    pattern = re.compile(r'InSight sol')
    
    try:
        
        mars_weather = weather_soup.find('span', text = pattern).text
        
    except:
        
        mars_weather = 'Some error occured while retrieving Mars weather data from Twitter. Please try again after sometime.'
        
    print(mars_weather)
    
    #Close the browser after scraping
    #browser.quit()
    
    return mars_weather
    
    # -------------------------------------------------------------------------------
       

def scrape_info():
    
    browser = init_browser()
    
    # -------------------------------------------------------------------------------

    # URL of NASA MARS news site

    news_url = 'https://mars.nasa.gov/news/'

    browser.visit(news_url)
    
    time.sleep(2)
    
    soup_html = browser.html
    
    # Create BeautifulSoup object; parse with 'lxml'

    news_soup = BeautifulSoup(soup_html, 'lxml')

    # Retrieve the title of first news article

    news_title = news_soup.find_all('div', class_='content_title')[1].text

    # Retrieve the paragraph under recent article
 
    news_paragraph = news_soup.find('div', class_='article_teaser_body').text

    print(news_title)
    print(news_paragraph)
          

    # -------------------------------------------------------------------------------
    

    # URL of JPL Mars Space Images
    
    spaceimage_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(spaceimage_url)
    time.sleep(2)

    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    image_html = browser.html

    image_soup = BeautifulSoup(image_html, 'lxml')

    img_result = image_soup.find('figure', class_ = 'lede')

    image_url = img_result.a['href']

    featured_image_url = 'https://www.jpl.nasa.gov' + image_url
    
    print(featured_image_url)


    # -------------------------------------------------------------------------------

    
    facts_url = 'https://space-facts.com/mars/'

    browser.visit(facts_url)
    time.sleep(2)
    
    facts_html = browser.html
        
    facts_df = pd.read_html(facts_url, index_col = None)[0]

    facts_df.columns = ['Description','Value']

    facts_df.set_index('Description', inplace = True)

    mars_facts_html = facts_df.to_html()
    
    print(mars_facts_html)

    # -------------------------------------------------------------------------------
    
    ''' Alternate Sol:

    facts_url = 'https://space-facts.com/mars/'

    browser.visit(facts_url)
    time.sleep(2)
    
    facts_html = browser.html
    
    facts_soup = BeautifulSoup(facts_html, 'lxml')
    
    mars_facts_table = facts_soup.find('table', id = "tablepress-p-mars")

    mars_facts_html = mars_facts_table.prettify()

    #print(mars_facts_html)
    
    '''

    # -------------------------------------------------------------------------------
    
    
    # List of Mars hemispheres
    hemispheres_list = ['Cerberus Hemisphere',
                        'Schiaparelli Hemisphere',
                        'Syrtis Major Hemisphere',
                        'Valles Marineris Hemisphere'
                       ]
    
    # Create a list to add the dictionaries with the hemisphere title and the image url string.
    hemispheres_info = []

    
    # URL of page to be scraped
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    for item in hemispheres_list:
    
        browser.visit(hemisphere_url)
    
        browser.click_link_by_partial_text(item)
    
        hemisphere_soup = BeautifulSoup(browser.html,'lxml')
    
        title = hemisphere_soup.find('h2', class_ = 'title').text
        img_url = hemisphere_soup.find("div",class_ ="wide-image-wrapper").find('a')['href']
    
        hemispheres_info.append({"Title": title,
                                 "Image_URL": img_url
                                })
        
    print(hemispheres_info)

    # -------------------------------------------------------------------------------
    
    mars_info = {"news_title" : news_title,
                 "news_paragraph": news_paragraph,
                 "featured_image_url" : featured_image_url,
                 "mars_weather" : mars_weather(browser),
                 "mars_facts_html" : mars_facts_html,
                 "hemispheres_info" : hemispheres_info
                }    

    # Close the browser after scraping
    browser.quit()
    
    return mars_info

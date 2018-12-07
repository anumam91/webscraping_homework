from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import os
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
from selenium import webdriver
import time


def scrape():
    executable_path = {'executable_path': './chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find("div",class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    print(f"Title: {news_title}")
    print(f"Para: {news_p}")
    browser.quit()
    time.sleep(3)



    #JPL Mars Space Images - Featured Image
    executable_path = {'executable_path': './chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    main_container = soup.select("#full_image")[0]["data-fancybox-href"]
    main_image_url="https://www.jpl.nasa.gov"+main_container
    time.sleep(3)
    browser.quit()
    print(main_image_url)

    #weather twitter
    weather_twitter_url='https://twitter.com/marswxreport?lang=en'
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(weather_twitter_url)

    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')

    mars_weather = weather_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)
    time.sleep(3)
    browser.quit()

#Mars Facts¶
#Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc. Use Pandas to convert the data to a HTML table string.

    mars_facts_url='https://space-facts.com/mars/'
    facts_table = pd.read_html(mars_facts_url)
    facts_table
    df_facts_table = facts_table[0]
    df_facts_table.columns = ["Parameter", "Values"]
    df_facts_table.set_index(["Parameter"])


    df_facts_html = df_facts_table.to_html()
    print(df_facts_html)
    time.sleep(3)
    browser.quit()
#Mars Hemispheres
    executable_path = {'executable_path': './chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    astrt_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    request = requests.get(astrt_url)

    soup = BeautifulSoup(request.text, "html.parser")
    hemisphere_list = soup.find_all('a', class_="itemLink product-item")
    print(len(hemisphere_list))
    #print(hemisphere_list[1]['href'])

    hemisphere_list_final = []
    for image in hemisphere_list:
        image_title = image.find('h3').text
        #print(img_title)
        link_to_image = "https://astrogeology.usgs.gov/" + image['href']
        #print(link_to_img)
        image_request = requests.get(link_to_image)
        soup = BeautifulSoup(image_request.text, 'lxml')
        image_tag = soup.find('div', class_='downloads')
        image_url = image_tag.find('a')['href']
        hemisphere_list_final.append({"Title": image_title, "Image_Url": image_url})
    time.sleep(3)
    browser.quit()
    mars_data = {
     "news_title": news_title,
     "news_p": news_p,
     "main_image_url": main_image_url,
     "mars_weather": mars_weather,
     "df_facts_html":df_facts_html,
     "hemisphere_list_final": hemisphere_list_final
     }

    return mars_data

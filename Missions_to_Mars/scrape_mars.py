from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 
import time
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    from webdriver_manager.chrome import ChromeDriverManager
    executable_path = {"executable_path": ChromeDriverManager().install()} 
    return Browser("chrome", **executable_path, headless=False)

mission_to_mars={}

def scrape_news():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")   
    first_li = soup.find('li', class_='slide')
    news_title = first_li.find('div',class_='content_title').text
    news_p= first_li.find('div', class_='article_teaser_body').text

    mission_to_mars['news_title']=news_title
    mission_to_mars['news_p']=news_p


    browser.quit()
    return mission_to_mars

def scrape_jpl_img():
    browser = init_browser()
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html#'
    browser.visit(url)
    time.sleep(2)
    # Design an XPATH selector to grab the "JPL Featured Space Image" 
    xpath = '/html/body/div[1]/img'
    results = browser.find_by_xpath(xpath)
    img = results[0]
    image_url = img['src']
    # img.click()
    # Scrape the browser into soup and use soup to find the full resolution image of mars
    # Scrape the browser into soup and use soup to find the full resolution image of mars
    # Save the image url to a variable called `img_url`
    # html = browser.html
    # soup = BeautifulSoup(html, 'html.parser')
    # #img_url = soup.find_all("img")
    # img_url = soup.find("img",{"headerimage fade-in"})["src"]

    
    mission_to_mars['feature_img'] = image_url

    browser.quit()
    return mission_to_mars
 

def scrape_fact():
    browser = init_browser()
    fact_url='https://space-facts.com/mars/'
    tables = pd.read_html(fact_url)
    df = tables[0]
    df.columns = ['Description', 'Value']
    #html_table = df.to_html(table_id="html_tbl_css",justify='left',index=False)
    #data = df.to_dict(orient='records')  
    html_table = df.to_html()
    html_table.replace('\n', '')
    mission_to_mars['tables']=html_table

    browser.quit()
    return mission_to_mars


def scrape_hemispheres():
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="item")     
    img_url_list = []

    img_url_list = []

    for item in items:
        title = item.find('h3').text
        part_img_url = item.find('a', class_='itemLink product-item')['href']
        print(part_img_url)
        browser.visit('https://astrogeology.usgs.gov' + part_img_url)
        part_img_url=browser.html
        soup=BeautifulSoup(part_img_url,'html.parser')
        img_url='https://astrogeology.usgs.gov'+soup.find('img',class_='wide-image')['src']
        img_url_list.append({"title": title, "img_url":img_url})
    
    mission_to_mars['img_url_list']=img_url_list

        
    browser.quit()
    return mission_to_mars





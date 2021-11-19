import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
   
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    url = 'https://redplanetscience.com/'
    browser.visit(url)

    
    html = browser.html
    soup = bs(html, 'html.parser')

  
    news_title = soup.find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()    


 
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    
    html = browser.html
    soup = bs(html, 'html.parser')

  
    btn = soup.find('button', text=' FULL IMAGE')
    if btn.parent.name == 'a':
        a = btn.parent

    if a:
        featured_image_url = a['href']

   
    mars_featured_image_url = url + featured_image_url


    
    url = 'https://galaxyfacts-mars.com/'
    table = pd.read_html(url, match='Equatorial Diameter')

    
    df = table[0]

   
    mars_html_tbl = df.to_html(index=False, classes="table table-striped", header=False)
    mars_html_tbl = mars_html_tbl.replace('\n', '')


  

    mars_hemi_image_urls = []

   
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    
    html = browser.html
    soup = bs(html, 'html.parser')

    
    browser2 = Browser("chrome", **executable_path, headless=False)

   
    container = soup.find('div', class_='results')

   
    items = container.find_all('div', class_='item')

   
    for item in items:
    
        
        title = item.find('h3').get_text() 

       
        page = item.find('a', class_='product-item')['href']
        url2 = url + page   
        browser2.visit(url2)
        html2 = browser2.html
        soup2 = bs(html2, 'html.parser')

     
        img_url = url + soup2.find('a', text='Sample')['href']

       
        hemishpere_dict = {
            "title":title, 
            "img_url":img_url
        }

      
        marsHemispheres_image_urls.append(hemishpere_dict)

     
        mars_data = {
            "marsNews_latest_Title": news_title,
            "marsNews_latest_ArticleBody": news_p,
            "marsImages_featured_image_url": mars_featured_image_url,
            "marsFacts_html_tbl": mars_html_tbl,
            "marsHemispheres_image_urls": mars_hemi_image_urls
        }

  
    browser2.quit()
    browser.quit()

    # Return results
    return mars_data
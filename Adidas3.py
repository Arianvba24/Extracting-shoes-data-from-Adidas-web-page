import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd


url = r"https://www.adidas.es/zapatillas-hombre"
# url = r"https://www.adidas.es/zapatillas-hombre?start=768"

# Defining variables for DataFrame------------------------------

title = []
price = []
category = []
product_id = []





value = 0 
async def open_browser(url):
    async with async_playwright() as p:
        browser =  await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.wait_for_timeout(2000)
        
        await page.goto(url)
        # await page.get_by_text("open new tab").click()
        
        content = await page.content()
        
        # Cambio---------------------------------------
        await page.wait_for_selector('.gl-cta.gl-cta--primary.gl-cta--full-width._text-wrap_1xzpo_29')
        await page.click('.gl-cta.gl-cta--primary.gl-cta--full-width._text-wrap_1xzpo_29')

        # await asyncio.sleep(1)

        while 1:


            task1 = asyncio.create_task(get_data(content))
            task2 = await asyncio.create_task(get_link(content))

            if task2[1] == None:

       
       
                print("Exiting loop....")
                await asyncio.sleep(1)
                break
            else:

                await page.goto(f"https://www.adidas.es/{task2[1]}")
                content = await page.content()

     

 # Cambio---------------------------------------
async def browse_on_browser(page,url):

    await page.goto(url)
    content = await page.content()
    await asyncio.sleep(3)
    return content
 # Cambio---------------------------------------
async def get_data(html_data_source):
    html_value = BeautifulSoup(html_data_source,"lxml")
    soup = html_value.find_all("div",class_="grid-item")
    for i in soup:
        # title = i.text
        # print(title)
        try:

            title_value = i.find("p",class_="glass-product-card__title").text
            category_value = i.find("p",class_="glass-product-card__category").text
            product_id_value = i.attrs["data-grid-id"]
            # price_value = i.find("div",class_="gl-price-item notranslate").text
            title.append(title_value)
            # price.append(price_value)
            category.append(category_value)
            product_id.append(product_id_value)
            print(f"{title_value} | {category_value} | {product_id_value}")

        except:
            pass



     


def create_dataframe(title,price,category,product_id):

    data = {

    "Title" : title,
    # "Price" : price,
    "Category" : category,
    "Product_id" : product_id



    }
    
    df = pd.DataFrame(data)

    return df


    



async def get_link(html_data_source):
    html_value = BeautifulSoup(html_data_source,"lxml")
    soup = html_value.find("div",class_="pagination__control___3C268 pagination__control--next___329Qo pagination_margin--next___3H3Zd")
    try:
        print(soup)

        if soup.a.text == "Siguiente":
            return "next",soup.a["href"]
        else:
            return None,None
    except:

        return None,None
    

async def main(url):

    
    # print(value)
    html_data = await open_browser(url)

    # while 1:

        # choice = int(input("Eliga un numero"))

        # if choice == 1:
        #     break

    # task1 = await asyncio.create_task(get_data(html_data))
    # task2 = await asyncio.create_task(get_link(html_data))

    # # value = await asyncio.gather(get_data(html_data), get_link(html_data))
    # print(task2,"----------------------------------------------------------------------------")
    # if task2[1] == None:

    #     # print(value,"--------------------------------------")
    #     print("Exiting loop....")
    #     await asyncio.sleep(1)
    #     # break
    # else:
        
    #     data = f"https://www.adidas.es/{task2[1]}"
    #     html_data = await open_browser(data)
    #     # html_data = await asyncio.create_task(browse_on_browser(page,data))
    #     # await open_browser(url)
    #     print(html_data)
    #     await open_browser(html_data)
    #         html_data




if __name__=="__main__":
    asyncio.run(main(url))
    df = create_dataframe(title,price,category,product_id)
    df.to_excel(r"C:\Users\Cash\Proyectos\Web Scrapping\Adidas\Adidas3.xlsx",index=False)
    # print(df)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())

    
# Si
#  

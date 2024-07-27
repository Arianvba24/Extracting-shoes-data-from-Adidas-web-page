import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import json


df_1 = pd.read_excel(r"C:\Users\Cash\Proyectos\Web Scrapping\Adidas\Adidas3.xlsx")
api_values = [f"https://www.adidas.es/api/search/product/{x}" for x in list(df_1["Product_id"].values)]

# api_values = api_values1[:200]
urls = api_values

name = []
brand = []
category = []
color = []
modelID = []
saleprice = []
link = []

data_json = {
    
    "Name" : name,
    "Brand" : brand,
    "Category" : category,
    "Color" : color,
    "Model ID" : modelID,
    "Price" : saleprice,
    "Link" : link
     
}


# print(len(api_values))
async def open_and_download_browser(context, url):
    page = await context.new_page()
    await page.goto(url)
    await page.wait_for_timeout(1300)
    content = await page.content()
    await page.close()
    return content

# Función para procesar una lista de URLs
async def loop_browser(urls):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        tasks = [open_and_download_browser(context, url) for url in urls]
        contents = await asyncio.gather(*tasks)
        await browser.close()
        return contents
        # for value,url in title:
        #     print(f"{value}--------------------------------{url}")
        # print(len(title))
            # soup = BeautifulSoup(value,"lxml")
            # titles = soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
            # for i in titles:
            #     print(i.h3.a.text,url)

def from_dataframe_to_data(df,extension,adress):
   
        if extension == "csv":
            return df.to_csv(adress,index = False)
        elif extension == "xlsx":
            return df.to_excel(adress,index = False)
        elif extension == "sql":
            return df.to_sql(adress,index = False)
        elif extension == "json":
            return df.to_json(adress,index = False)
        elif extension == "parquet":
            return df.to_parquet(adress,index = False)



def find_data(data):
    try:

        # print(data)
        data1 = re.findall('{"_links":[\S\s]*</pre></body></html>',data)
        # print(data1)
        data2 = data1[0].replace("</pre></body></html>","")
        values = json.loads(data2)
        return values
    except:
        return {"name" : "Producto quitado","brand" : "Producto quitado","category" : "Producto quitado","color" : "Producto quitado","modelId" : "Producto quitado","salePrice":"Producto quitado","link":"Producto quitado"}                  
      


if __name__=="__main__":
    # asyncio.run(loop_browser(urls))

    # values_data = [find_data(value) for value in asyncio.run(loop_browser(urls))]
    # for i in values_data:
    #     name.append(i["name"])
    #     brand.append(i["brand"])
    #     category.append(i["category"])
    #     color.append(i["color"])
    #     modelID.append(i["modelId"])
    #     saleprice.append(i["salePrice"])
    #     link.append(f'https://www.adidas.es{i["link"]}')
    
    while 1:
        print(f"Remaining products: {len(api_values)}")

        if len(api_values) >= 80:
            urls = [api_values.pop() for i in range(80)]
            values_data = [find_data(value) for value in asyncio.run(loop_browser(urls))]
            for i in values_data:
                name.append(i["name"])
                brand.append(i["brand"])
                category.append(i["category"])
                color.append(i["color"])
                modelID.append(i["modelId"])
                saleprice.append(i["salePrice"])
                link.append(f'https://www.adidas.es{i["link"]}')

            del urls
        elif len(api_values) < 80 and len(api_values) > 0:
            urls = [api_values.pop() for i in range(len(api_values))]
            values_data = [find_data(value) for value in asyncio.run(loop_browser(urls))]
            for i in values_data:
                name.append(i["name"])
                brand.append(i["brand"])
                category.append(i["category"])
                color.append(i["color"])
                modelID.append(i["modelId"])
                saleprice.append(i["salePrice"])
                link.append(f'https://www.adidas.es{i["link"]}')
          
            del urls
        elif len(api_values) == 0:
            print("Acabado")
            break
        else:
            print("Acabado")
            break

    df = pd.DataFrame(data_json)
    rows_remove = df.loc[df["Name"]=="Producto quitado"].index
    df.drop(rows_remove,inplace=True)

    
    print(df)
    from_dataframe_to_data(df=df,extension="xlsx",adress=r"C:\Users\Cash\Proyectos\Web Scrapping\Adidas\outcome.xlsx")
            







# print(api_values)

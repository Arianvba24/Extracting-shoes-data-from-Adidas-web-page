# Extracting-shoes-data-from-Adidas-web-page
Hi mates!

This is one of the most dificult web pages i've ever scrapped: **Adidas** 

It has all kind of security measures(rendered Javascript code to deploy data, robots.txt file to block you, slow data loading).

In this case we are going to go throught two procedures. One makes an infinite loop until we go throught all the pages and get the ID of every product and after getting all the IDs we go throught and second procedure which is doing a http request to Adidas API and get all the data.

First procedure is has to be done only once a weak at most. You probably are asking we not scrapping the data in a first place? Simple. The data loading is **VERY** slow. The only data that is loaded fast are IDs of every product.

Once we get the IDs and do the https requests we find another security barrier in the API
![image](https://github.com/user-attachments/assets/1dc762b0-b34f-494e-a309-4682a318204b)

We can find to kind of security barriers:

- Javascript generated credentials to access the API
- Javascript anti-scrape barrier

First one is literally impossible to trespass because use algorithms to generate credentials in another hidden api and return credentials that go sticked to the http request of the API.

Second one is possible to trespass but we must use Selenium or Playwright and **SUPER IMPORTANT** use **async programming functions**

What are we gonna do? Instead of going page by page scrapping we will scrappe **ALL PAGES** at once 

Let's check this out:

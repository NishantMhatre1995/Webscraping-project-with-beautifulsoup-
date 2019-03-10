from bs4 import BeautifulSoup
import requests

#Url of website to scrap quotes
base_url = "http://quotes.toscrape.com"
url = "/page/1/"
quotes = []

#scrap all quotes from different web pages
while url:
    responce = requests.get(base_url+url)
    soup = BeautifulSoup(responce.text,"html.parser")
    next_button = soup.find(class_="next")
    url = next_button.find("a")["href"] if next_button else ""
    for quote in soup.select(".quote"):
        quotes.append({
            "text":quote.find("span").get_text(),
            "author":quote.find(class_="author").get_text(),
            "link": quote.find("a")["href"]
            })

#randomly select any quotes and give 4 chance to guess author name.
from random import randrange
chance = 4
again = "y"
while again=="y":
    number = randrange(0,len(quotes))
    quote = quotes[number]
    ans = quote["author"].lower()
    print(quote["text"])
    while chance>0:
        if chance ==3:
            responce = requests.get(base_url+quote["link"])
            soup = BeautifulSoup(responce.text,"html.parser")
            hint = soup.find("span").get_text()
            print(f"\nhint: author born in {hint}")
        elif chance==2:
            print(f"\nauthor's first name start with: {ans[0].upper()}")
        elif chance==1 :
            hint = ans.split(" ")[-1][0]
            print(f"\nauthor's last name start with: {hint.upper()}")
        guss = input(f"chance left:{chance} \nGuesses author name:")    
        if guss.lower()==ans:
            print("you win !!") 
            break
        else:
            chance-=1
    print(f"Answer is: {ans.upper()}")
    again = input("Do you want to play again:(y/n)")
    if again=="y": chance=4
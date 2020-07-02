import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import random
import time

#unquote which one you need
#WebhookUrl = 'webhook1'
#WebhookUrl = ['webhook1', 'webhook2']

mainsite = requests.get('https://supremecommunity.com/season/latest/droplists/')
droplist = BeautifulSoup(mainsite.text,"lxml")
link = droplist.find('div',{'id':'box-latest'}).a.get('href')
droplist_link = 'https://supremecommunity.com/' + link

def main():
    r = requests.get(droplist_link)
    soup = BeautifulSoup(r.text,"html.parser")
    cards = soup.find_all('div',{'class':'card card-2'})
    for card in cards:
        item = card.find("div",{"class":"card-details"})["data-itemname"]
        img = card.find("img",{"class":"prefill-img"})["src"]
        try:
            price = card.find("span",{"class":"label-price"}).text
            price = price.replace(" ","")
            price = price.replace("\n","")
        except:
            price = 'Unknown'
        #upvotes = card.find("p",{"class":"upvotes hidden"}).text
        #downvotes = card.find("p",{"class":"downvotes hidden"}).text
        
        webhook = DiscordWebhook(url=WebhookUrl, username='Supreme Droplist')
        embed = DiscordEmbed(title='Supreme Droplist', color=0xC90101, url=droplist_link)
        embed.set_image(url="https://supremecommunity.com"+img)
        embed.add_embed_field(name='Item:', value='**'+item+'**',inline=False)
        embed.add_embed_field(name='Price:', value='**'+price+'**',inline=False)
        embed.set_footer(text='Supreme Droplist | Developed by DRB02#0001')
        webhook.add_embed(embed)
        webhook.execute()
        time.sleep(0.5)
        print("| WEBHOOK SENT |")
    else:
        print("End of list reached")
        
main()

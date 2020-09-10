import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import random
import time

#unquote which one you need
WebhookUrl = 'https://discordapp.com/api/webhooks/636360687668690985/ap5AMc15BLz4M4SM84uiW2Wx93KiUbnx7BkVyRjAfD2fXn7c7qjf0HlWtbZO16i1CkJ-'


mainsite = requests.get('https://supremecommunity.com/season/latest/droplists/')
droplist = BeautifulSoup(mainsite.text,"lxml")
link = droplist.find('div',{'id':'box-latest'}).a.get('href')
droplist_link = 'https://supremecommunity.com/' + link

def main():
    r = requests.get(droplist_link)
    soup = BeautifulSoup(r.text,"html.parser")
    cards = soup.find_all('div',{'class':'card card-2'})
    for card in cards:
        pid = card.find('div', class_='card-details').get('data-itemid')
        info = requests.get('https://supremecommunity.com/season/itemdetails/' + pid)
        infosoup = BeautifulSoup(info.text,"lxml")
        try:
            priceeuro = infosoup.find_all('span', class_='label label--inline price-label')
			
			#insert 0 for dollar
			#insert 1 for pound
			#insert 2 for euro
			#insert 3 for yen
            price = priceeuro[2].text
    
        except:
            price = 'Unknown'
        item = card.find("div",{"class":"card-details"})["data-itemname"]
        img = card.find("img",{"class":"prefill-img"})["src"]
        upvotes = card.find("p",{"class":"upvotes hidden"}).text
        downvotes = card.find("p",{"class":"downvotes hidden"}).text
        
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

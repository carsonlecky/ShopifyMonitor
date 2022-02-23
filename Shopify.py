import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import json

site = "https://deadstock.ca" # insert the site you want to monitor including the https://
delay = 5 # an integer in seconds.
webhookURL = "" # Insert your Webhook URL here 

def sendWebhook(site, variants, titles, image, item_name, handle): 

    webhook = DiscordWebhook(url=webhookURL)

    embed = DiscordEmbed(title=f"{item_name}", url=f"{site}/products/{handle}",  description=f'**Site**: {site}', color=242424)
    embed.set_thumbnail(url=f'{image}')

    for title, variant in zip(titles, variants):
        embed.add_embed_field(name=f'ATC', value=f'[{title}]({site}/cart/{variant}:1)')

    embed.set_timestamp()
    embed.set_footer(text=f'Shopify Monitor by @carsonleckyy')  
    webhook.add_embed(embed)
    response = webhook.execute()

previousItems = []

while True: 
    req = requests.get(f'{site}/products.json?limit=15')
    data = req.json()

    for product in data['products']: 
        item_name = product['title']
        handle = product['handle']

        if handle in previousItems:
            print('already in')
            continue


        for image in product["images"]: 
            image = image["src"]
            break
                
    
        variants = []
        titles = []

        for variant in product["variants"]: 
            var = variant["id"]
            title = variant["title"]

            variants.append(var)
            titles.append(title)

        sendWebhook(site, variants, titles, image, item_name, handle)
        print(f'Sent webhook {item_name}')
        previousItems.append(handle)
        
    time.sleep(delay)


import discord
from discord.ext import commands, tasks
import random 
import json
from unidecode import unidecode
import os
from dotenv import load_dotenv, find_dotenv
import datetime
import time

client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())


with open("Cards_it.json", "r", encoding="utf8") as f:
    data1 = json.load(f)
    CardListIT = []
    CardListNameIT = []
    for n in range(len(data1)):
        CardListNameIT.append(unidecode(data1[n]['name']).upper())
        CardListIT.append(data1[n])

with open("Cards_de.json", "r", encoding="utf8") as f:
    data2 = json.load(f)
    CardListDE = []
    CardListNameDE = []
    for n in range(len(data2)):
        CardListNameDE.append(unidecode(data2[n]['name']).upper())
        CardListDE.append(data2[n])

with open("Cards.json", "r", encoding="utf8") as f:
    data = json.load(f)
    CardList = []
    CardListName = []
    CardListDay = []
    for n in range(len(data)):
        CardListName.append(unidecode(data[n]['name']).upper())
        CardList.append(data[n])
        if data[n]['set'] != 'Reward':
            CardListDay.append(data[n])

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

dict = {"<b>": "**",  # define desired replacements here
    "</b>": "**", 
    "<i>": "_", 
    "</i>": "_", 
    "reason": "<:reason:1081588160779255938>",
    "conflict": "<:conflict:1081588168807153726>",
    "exploration": "<:exploration:1081588142093635644>",
    "connection": "<:connection:1081588137987424286>",
    "awareness": "<:awareness:1081702479290450031>",
    "spirit": "<:spirit:1081702484784992289>",
    "fitness": "<:fitness:1081702482012549170>",
    "focus": "<:focus:1081702483568623696>",
    "white_large_square": "<:white_large_square:1082277091472588950>",
    "white_square_button": "<:white_square_button:1082277094274371594>",
    } 

# GUESS
@client.command()
async def erguess(ctx):
    i = random.randint(1,len(data))
    traits = data[i]['traits'].split("/")
    traits = list(map(lambda x : unidecode(x.strip()), traits))
    name = data[i]['name']
    print(i, name)
    dict_guess = {"<b>": "**",  # define desired replacements here
    "</b>": "**", 
    "<i>": "_", 
    "</i>": "_", 
    data[i]['name']: "This Card", 
    "[": "<:", 
    "harm]": "harm:1081588151530819644>",
    "progress]": "progress:1081588156509462640>",
    "reason]": "reason:1081588160779255938>",
    "exploration]": "exploration:1081588142093635644>",
    "connection]": "connection:1081588137987424286>",
    "conflict]": "conflict:1081588168807153726>"
    } 
    embed = discord.Embed(title = "What's the card?", description = "Guess the card name typing `is <query>`", color= discord.Color.green(), timestamp = ctx.message.created_at)
    
    if any(x == data[i]['type_name'] for x in ['Gear', 'Attachment', 'Attribute']):          # GEAR, ATTACHMENT, ATTRIBUTE
        embed.add_field(name = "Cost", value = data[i]['cost'])
        embed.add_field(name= "Type and traits", value = f"{data[i]['type_name']} / _{data[i]['traits']}_")
        if data[i]['sphere_code'] == 'awareness':
            card_sphere = '<:awareness:1081702479290450031>'
        elif data[i]['sphere_code'] == 'focus':
            card_sphere = '<:focus:1081702483568623696>'
        elif data[i]['sphere_code'] == 'fitness':
            card_sphere = '<:fitness:1081702482012549170>'
        elif data[i]['sphere_code'] == 'spirit':
            card_sphere = '<:spirit:1081702484784992289>'
        embed.add_field(name = "Sphere", value = card_sphere)
        if data[i]['equip_value'] == 3:
            a, b, c = "<:white_large_square:1082277091472588950>", "<:white_large_square:1082277091472588950>", "<:white_large_square:1082277091472588950>"
            d, e = "<:white_square_button:1082277094274371594>", "<:white_square_button:1082277094274371594>"
            embed.add_field(name= "Equip value", value= f"{a} {b} {c} {d} {e}")
        if data[i]['equip_value'] == 2:
            a, b = "<:white_large_square:1082277091472588950>", "<:white_large_square:1082277091472588950>"
            c, d, e = "<:white_square_button:1082277094274371594>", "<:white_square_button:1082277094274371594>", "<:white_square_button:1082277094274371594>"
            embed.add_field(name= "Equip value", value= f"{a} {b} {c} {d} {e}")
        if data[i]['equip_value'] == 1:
            a = "<:white_large_square:1082277091472588950>"
            b, c, d, e = "<:white_square_button:1082277094274371594>", "<:white_square_button:1082277094274371594>", "<:white_square_button:1082277094274371594>", "<:white_square_button:1082277094274371594>"
            embed.add_field(name= "Equip value", value= f"{a} {b} {c} {d} {e}")
        if data[i]['generic_token'] != '':
            embed.add_field(name= "Token", value= data[i]['generic_token'])
        test_icon = []
        for num in range(data[i]['conflict_number']):
            test_icon.append("<:conflict:1081588168807153726>")
        for num in range(data[i]['connection_number']):
            test_icon.append("<:connection:1081588137987424286>")
        for num in range(data[i]['exploration_number']):
            test_icon.append("<:exploration:1081588142093635644>")
        for num in range(data[i]['reason_number']):
            test_icon.append("<:reason:1081588160779255938>")
        test_icon = str(test_icon)
        test_icon = test_icon.replace(',', '')
        test_icon = test_icon.replace('[', '')
        test_icon = test_icon.replace(']', '')
        test_icon = test_icon.replace("'", '')
        embed.add_field(name= "Test icons", value= test_icon)
        embed.add_field(name = "Text", value = replace_all(data[i]['text'], dict_guess))
        embed.add_field(name = "Flavor", value = data[i]['flavor'])
        embed.add_field(name = "Box", value = data[i]['pack_name'])
        embed.add_field(name = "Set", value = f"{data[i]['set']} - {data[i]['position']}")
        embed.add_field(name= "Attribute requirement", value= f"{data[i]['sphere_cost']} **{data[i]['sphere_name']}**")

    elif data[i]['type_name'] == 'Role':                                                     # ROLE
        embed.add_field(name= "Type and traits", value = f"{data[i]['type_name']}")
        embed.add_field(name = "Text", value = replace_all(data[i]['text'], dict_guess))
        embed.add_field(name = "Flavor", value = data[i]['flavor'])
        embed.add_field(name = "Box", value = data[i]['pack_name'])
        embed.add_field(name = "Set", value = f"{data[i]['set']} - {data[i]['position']}")
    
    elif data[i]['type_name'] == 'Moment':                                                   # MOMENT
        embed.add_field(name = "Cost", value = data[i]['cost'])
        embed.add_field(name= "Type and traits", value = f"{data[i]['type_name']} / _{data[i]['traits']}_")
        if data[i]['sphere_code'] == 'awareness':
            card_sphere = '<:awareness:1081702479290450031>'
        elif data[i]['sphere_code'] == 'focus':
            card_sphere = '<:focus:1081702483568623696>'
        elif data[i]['sphere_code'] == 'fitness':
            card_sphere = '<:fitness:1081702482012549170>'
        elif data[i]['sphere_code'] == 'spirit':
            card_sphere = '<:spirit:1081702484784992289>'
        embed.add_field(name = "Sphere", value = card_sphere)
        test_icon = []
        for num in range(data[i]['conflict_number']):
            test_icon.append("<:conflict:1081588168807153726>")
        for num in range(data[i]['connection_number']):
            test_icon.append("<:connection:1081588137987424286>")
        for num in range(data[i]['exploration_number']):
            test_icon.append("<:exploration:1081588142093635644>")
        for num in range(data[i]['reason_number']):
            test_icon.append("<:reason:1081588160779255938>")
        test_icon = str(test_icon)
        test_icon = test_icon.replace(',', '')
        test_icon = test_icon.replace('[', '')
        test_icon = test_icon.replace(']', '')
        test_icon = test_icon.replace("'", '')
        embed.add_field(name= "Test icons", value= test_icon)
        embed.add_field(name = "Text", value = replace_all(data[i]['text'], dict_guess))
        embed.add_field(name = "Flavor", value = data[i]['flavor'])
        embed.add_field(name = "Box", value = data[i]['pack_name'])
        embed.add_field(name = "Set", value = f"{data[i]['set']} - {data[i]['position']}")
        embed.add_field(name= "Attribute requirement", value= f"{data[i]['sphere_cost']} **{data[i]['sphere_name']}**")

    elif data[i]['type_name'] == 'Being':                                                    # BEING  
        embed.add_field(name = "Cost", value = data[i]['cost'])
        embed.add_field(name= "Type and traits", value = f"{data[i]['type_name']} / _{data[i]['traits']}_")
        if data[i]['sphere_code'] == 'awareness':
            card_sphere = '<:awareness:1081702479290450031>'
        elif data[i]['sphere_code'] == 'focus':
            card_sphere = '<:focus:1081702483568623696>'
        elif data[i]['sphere_code'] == 'fitness':
            card_sphere = '<:fitness:1081702482012549170>'
        elif data[i]['sphere_code'] == 'spirit':
            card_sphere = '<:spirit:1081702484784992289>'
        embed.add_field(name = "Sphere", value = card_sphere)
        test_icon = []
        for num in range(data[i]['conflict_number']):
            test_icon.append("<:conflict:1081588168807153726>")
        for num in range(data[i]['connection_number']):
            test_icon.append("<:connection:1081588137987424286>")
        for num in range(data[i]['exploration_number']):
            test_icon.append("<:exploration:1081588142093635644>")
        for num in range(data[i]['reason_number']):
            test_icon.append("<:reason:1081588160779255938>")
        test_icon = str(test_icon)
        test_icon = test_icon.replace(',', '')
        test_icon = test_icon.replace('[', '')
        test_icon = test_icon.replace(']', '')
        test_icon = test_icon.replace("'", '')
        embed.add_field(name= "Test icons", value= test_icon)
        embed.add_field(name= "Presence", value= data[i]['presence'])
        embed.add_field(name= "Harm", value= data[i]['harm_threshold'])
        embed.add_field(name = "Text", value = replace_all(data[i]['text'], dict_guess))
        embed.add_field(name = "Flavor", value = data[i]['flavor'])
        embed.add_field(name = "Box", value = data[i]['pack_name'])
        embed.add_field(name = "Set", value = f"{data[i]['set']} - {data[i]['position']}")
        embed.add_field(name= "Attribute requirement", value= f"{data[i]['sphere_cost']} **{data[i]['sphere_name']}**")
    
    elif data[i]['type_name'] == 'Feature':                                                  # FEATURE  
        embed.add_field(name = "Cost", value = data[i]['cost'])
        embed.add_field(name= "Type and traits", value = f"{data[i]['type_name']} / _{data[i]['traits']}_")
        if data[i]['sphere_code'] == 'awareness':
            card_sphere = '<:awareness:1081702479290450031>'
        elif data[i]['sphere_code'] == 'focus':
            card_sphere = '<:focus:1081702483568623696>'
        elif data[i]['sphere_code'] == 'fitness':
            card_sphere = '<:fitness:1081702482012549170>'
        elif data[i]['sphere_code'] == 'spirit':
            card_sphere = '<:spirit:1081702484784992289>'
        embed.add_field(name = "Sphere", value = card_sphere)
        test_icon = []
        for num in range(data[i]['conflict_number']):
            test_icon.append("<:conflict:1081588168807153726>")
        for num in range(data[i]['connection_number']):
            test_icon.append("<:connection:1081588137987424286>")
        for num in range(data[i]['exploration_number']):
            test_icon.append("<:exploration:1081588142093635644>")
        for num in range(data[i]['reason_number']):
            test_icon.append("<:reason:1081588160779255938>")
        test_icon = str(test_icon)
        test_icon = test_icon.replace(',', '')
        test_icon = test_icon.replace('[', '')
        test_icon = test_icon.replace(']', '')
        test_icon = test_icon.replace("'", '')
        embed.add_field(name= "Test icons", value= test_icon)
        embed.add_field(name= "Presence", value= data[i]['presence'])
        embed.add_field(name= "Progress", value= data[i]['progress_threshold'])
        embed.add_field(name = "Text", value = replace_all(data[i]['text'], dict_guess))
        embed.add_field(name = "Flavor", value = data[i]['flavor'])
        embed.add_field(name = "Box", value = data[i]['pack_name'])
        embed.add_field(name = "Set", value = f"{data[i]['set']} - {data[i]['position']}")
        embed.add_field(name= "Attribute requirement", value= f"{data[i]['sphere_cost']} **{data[i]['sphere_name']}**")

    await ctx.send(embed=embed)
    await ctx.send(f"I'm thinking of a card...\nTry to guess which one!")
    tries = 0
    def check(m: discord.Message):
        return m.channel == ctx.message.channel #m.author == ctx.author and 
    for j in range(10000):
        guess = await client.wait_for('message', check=check)
        if guess.content.startswith('is'):
            message_text = guess.content.split(" ")
            message_text.pop(0)
            card_name = []
            for h in message_text:
                card_name.append(h)
            mySeparator = " "
            card = mySeparator.join(card_name)
            if unidecode(card).upper() == unidecode(name).upper():
                await ctx.send("You guessed correctly!")
                if data[i]['set'] == 'Reward':
                    await ctx.send(f"|| {data[i]['imagesrc']} ||")
                else:
                    await ctx.send(data[i]['imagesrc'])
                break
            else:
                await ctx.send(f"Nope.\n{4-tries} attempts left.")
                if tries == 4:
                    await ctx.send("Game lost, try again!\nThe card was:")
                    if data[i]['set'] == 'Reward':
                        await ctx.send(f"|| {data[i]['imagesrc']} ||")
                    else:
                        await ctx.send(data[i]['imagesrc'])
                    break
                tries += 1
        elif guess.content.startswith('idk'):
            await ctx.send("Game lost, try again!\nThe card was:")
            if data[i]['set'] == 'Reward':
                await ctx.send(f"|| {data[i]['imagesrc']} ||")
            else:
                await ctx.send(data[i]['imagesrc'])
            break
        else:
            await ctx.send("You have to type `is` followed by the name of the card!\nIf you want to end the game type `idk`.")

# SEARCH CARD
@client.command()
async def erimg(ctx, card=None):
    message = ctx.message.content.split(' ')
    message.pop(0)
    cc = message
    message = " ".join(message)
    card = unidecode(message).upper()
    print(f"Looking for: {card}")
    def search(card_list, string):
        index_list = []
        for n in range(len(card_list)):
            if card_list[n].find(string) != -1:
                index_list.append(n)
        return index_list
    CardIndexes = search(CardListName, card)
    if len(CardIndexes) == len(CardList):
        await ctx.send('I am sorry, but I need at least a name to find a card')
    elif len(CardIndexes) == 1:
        if CardList[CardIndexes[0]]['set'] == 'Reward':
            await ctx.send(f"|| {CardList[CardIndexes[0]]['imagesrc']} ||")
        else:
            await ctx.send(CardList[CardIndexes[0]]['imagesrc'])
        try:
            await ctx.send(CardList[CardIndexes[0]]['imagesrc2'])
        except:
            pass
    elif len(CardIndexes) == 0:
        await ctx.send(f"No cards found matching '{cc}'.")
    else:
        cards_found = []
        if len(CardIndexes) > 20:
            max = 20
            await ctx.send(f"I've found {len(CardIndexes)} cards (Sending 20). Reply with the number of the one you want")
        else:
            max = len(CardIndexes)
            await ctx.send(f"I've found {len(CardIndexes)} cards. Reply with the number of the one you want")
        for ids in range(max):
            sphere = replace_all(CardList[CardIndexes[int(ids)]]['sphere_code'], dict)
            cards_found.append((f"{ids+1}. {sphere} **{CardList[CardIndexes[int(ids)]]['name']}**\n_{CardList[CardIndexes[int(ids)]]['type_name']}_ ({CardList[CardIndexes[int(ids)]]['pack_name']})"))
        await ctx.send('\n'.join(cards_found))
        def check(m: discord.Message):
            return m.channel == ctx.message.channel #m.author == ctx.author and 
        for j in range(1):
            id = await client.wait_for('message', check=check)
            id = id.content
            try:
                if CardList[CardIndexes[int(id)-1]]['set'] == 'Reward':
                    await ctx.send(f"|| {CardList[CardIndexes[int(id)-1]]['imagesrc']} ||")
                else:
                    await ctx.send(CardList[CardIndexes[int(id)-1]]['imagesrc'])
            except:
                await ctx.send("You have to type the number of the card you want!")
            try:
                await ctx.send(CardList[CardIndexes[int(id)-1]]['imagesrc2'])
            except:
                pass

# SEARCH CARD (ITALIAN)
@client.command()
async def erit(ctx, card=None):
    message = ctx.message.content.split(' ')
    message.pop(0)
    cc = message
    message = " ".join(message)
    card = unidecode(message).upper()
    print(f"Looking for: {card}")
    def search(card_list, string):
        index_list = []
        for n in range(len(card_list)):
            if card_list[n].find(string) != -1:
                index_list.append(n)
        return index_list
    CardIndexes = search(CardListNameIT, card)
    if len(CardIndexes) == len(CardListIT):
        await ctx.send('I am sorry, but I need at least a name to find a card')
    elif len(CardIndexes) == 1:
        if CardListIT[CardIndexes[0]]['set'] == 'Ricompensa':
            await ctx.send(f"|| {CardListIT[CardIndexes[0]]['imagesrc']} ||")
        else:
            await ctx.send(CardListIT[CardIndexes[0]]['imagesrc'])
        try:
            await ctx.send(CardListIT[CardIndexes[0]]['imagesrc2'])
        except:
            pass
    elif len(CardIndexes) == 0:
        await ctx.send(f"No cards found matching '{cc}'.")
    else:
        cards_found = []
        if len(CardIndexes) > 20:
            max = 20
            await ctx.send(f"I've found {len(CardIndexes)} cards (Sending 20). Reply with the number of the one you want")
        else:
            max = len(CardIndexes)
            await ctx.send(f"I've found {len(CardIndexes)} cards. Reply with the number of the one you want")
        for ids in range(max):
            sphere = replace_all(CardListIT[CardIndexes[int(ids)]]['sphere_code'], dict)
            cards_found.append((f"{ids+1}. {sphere} **{CardListIT[CardIndexes[int(ids)]]['name']}**\n_{CardListIT[CardIndexes[int(ids)]]['type_name']}_ ({CardListIT[CardIndexes[int(ids)]]['pack_name']})"))
        await ctx.send('\n'.join(cards_found))
        def check(m: discord.Message):
            return m.channel == ctx.message.channel #m.author == ctx.author and 
        for j in range(1):
            id = await client.wait_for('message', check=check)
            id = id.content
            try:
                if CardListIT[CardIndexes[int(id)-1]]['set'] == 'Ricompensa':
                    await ctx.send(f"|| {CardListIT[CardIndexes[int(id)-1]]['imagesrc']} ||")
                else:
                    await ctx.send(CardListIT[CardIndexes[int(id)-1]]['imagesrc'])
            except:
                await ctx.send("You have to type the number of the card you want!")
            try:
                await ctx.send(CardListIT[CardIndexes[int(id)-1]]['imagesrc2'])
            except:
                pass              

# SEARCH CARD (DUTCH)
@client.command()
async def erde(ctx, card=None):
    message = ctx.message.content.split(' ')
    message.pop(0)
    cc = message
    message = " ".join(message)
    card = unidecode(message).upper()
    print(f"Looking for: {card}")
    def search(card_list, string):
        index_list = []
        for n in range(len(card_list)):
            if card_list[n].find(string) != -1:
                index_list.append(n)
        return index_list
    CardIndexes = search(CardListNameDE, card)
    if len(CardIndexes) == len(CardListDE):
        await ctx.send('I am sorry, but I need at least a name to find a card')
    elif len(CardIndexes) == 1:
        if CardListDE[CardIndexes[0]]['set'] == 'Reward':
            await ctx.send(f"|| {CardListDE[CardIndexes[0]]['imagesrc']} ||")
        else:
            await ctx.send(CardListDE[CardIndexes[0]]['imagesrc'])
        try:
            await ctx.send(CardListDE[CardIndexes[0]]['imagesrc2'])
        except:
            pass
    elif len(CardIndexes) == 0:
        await ctx.send(f"No cards found matching '{cc}'.")
    else:
        cards_found = []
        if len(CardIndexes) > 20:
            max = 20
            await ctx.send(f"I've found {len(CardIndexes)} cards (Sending 20). Reply with the number of the one you want")
        else:
            max = len(CardIndexes)
            await ctx.send(f"I've found {len(CardIndexes)} cards. Reply with the number of the one you want")
        for ids in range(max):
            sphere = replace_all(CardListDE[CardIndexes[int(ids)]]['sphere_code'], dict)
            cards_found.append((f"{ids+1}. {sphere} **{CardListDE[CardIndexes[int(ids)]]['name']}**\n_{CardListDE[CardIndexes[int(ids)]]['type_name']}_ ({CardListDE[CardIndexes[int(ids)]]['pack_name']})"))
        await ctx.send('\n'.join(cards_found))
        def check(m: discord.Message):
            return m.channel == ctx.message.channel #m.author == ctx.author and 
        for j in range(1):
            id = await client.wait_for('message', check=check)
            id = id.content
            try:
                if CardListDE[CardIndexes[int(id)-1]]['set'] == 'Reward':
                    await ctx.send(f"|| {CardListDE[CardIndexes[int(id)-1]]['imagesrc']} ||")
                else:
                    await ctx.send(CardListDE[CardIndexes[int(id)-1]]['imagesrc'])
            except:
                await ctx.send("You have to type the number of the card you want!")
            try:
                await ctx.send(CardListDE[CardIndexes[int(id)-1]]['imagesrc2'])
            except:
                pass              

# CARD OF THE DAY
WHEN = datetime.time(12, 0, 5)   # set time here in UTC 
CHANNEL_ID = 1161012075460571167 # Put your channel id here

@tasks.loop(time=WHEN) 
async def card_of_the_day():
    channel = client.get_channel(CHANNEL_ID)
    i = random.randint(1,len(CardListDay))
    await channel.send("**Card of the day!**")
    card = await channel.send(CardListDay[i]['imagesrc'])
    emojis = ["\u0031\ufe0f\u20e3", '\u0032\ufe0f\u20e3', '\u0033\ufe0f\u20e3', '\u0034\ufe0f\u20e3', '\u0035\ufe0f\u20e3']
    time.sleep(0.5)
    for emoji in emojis:
        await card.add_reaction(emoji)

@client.event
async def on_ready():
    card_of_the_day.start()

# .day command
@client.command()
@commands.has_role(869589665043349504)  # ONLY USERS WITH THIS ROLE CAN USE THIS COMMAND
async def erday(ctx):
    channel = client.get_channel(CHANNEL_ID)
    i = random.randint(1,len(CardListDay))
    await channel.send("**Card of the day!**")
    card = await channel.send(CardListDay[i]['imagesrc'])
    emojis = ["\u0031\ufe0f\u20e3", '\u0032\ufe0f\u20e3', '\u0033\ufe0f\u20e3', '\u0034\ufe0f\u20e3', '\u0035\ufe0f\u20e3']
    time.sleep(0.5)
    for emoji in emojis:
        await card.add_reaction(emoji)



load_dotenv(find_dotenv())
client.run(os.getenv('TOKEN'))



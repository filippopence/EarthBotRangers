import discord
from discord.ext import commands, tasks
import random 
import json
from unidecode import unidecode
import os
from dotenv import load_dotenv, find_dotenv
import datetime
import time
import asyncio

class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents().all()
        super().__init__(command_prefix = commands.when_mentioned_or('!'), intents = discord.Intents.all())
    async def setup_hook(self) -> None:
        self.add_view(MySelectView())

client = PersistentViewBot()


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





# File path for storing user information
data_file_path = 'users_badges.json'

# Check if the file exists, if not, create an empty file
if not os.path.exists(data_file_path):
    with open(data_file_path, 'w') as f:
        json.dump({}, f)

badge_list0 = ['All Out Of Options',
              'Big Tech',
              'Electric Slide',
              'Enough Already']
badge_list1 = ['Hard Pass',
              "Howd That Get in There",
              'Long Flume',
              'No Stone Unturned']
badge_list2 = ['Noodling',
              'People Person',
              'Pro Gamer',
              'Shes A Natural']
badge_list3 = ['Ship of Theseus',
              'The Pentaverate',
              'Unlimited Power',
              'Unplanned Reunion']

class MySelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.select(
        placeholder="Choose a badge to grab!",
        options=[
        discord.SelectOption(label='All Out Of Options', emoji='<:All_Out_Of_Options:1174349162112888882>', description="Have only four cards remaining in the challenge deck."),
        discord.SelectOption(label='Big Tech', emoji='<:Big_Tech:1174349163627032636>', description="Discard a gear with 10 or more tokens on it using Moment of Desperation."),
        discord.SelectOption(label='Electric Slide', emoji='<:Electric_Slide:1174349165799682048>', description="Discard"),
        discord.SelectOption(label='Enough Already', emoji='<:Enough_Already:1174349167364157532>', description="Discard"),
        discord.SelectOption(label='Hard Pass', emoji='<:Hard_Pass:1174349170971246653>', description="Discard"),
        discord.SelectOption(label="Howd That Get in There", emoji='<:Howd_That_Get_in_There:1174349173764665466>', description="Discard"),
        discord.SelectOption(label='Long Flume', emoji='<:Log_Flume:1174349175169745018>', description="Discard"),
        discord.SelectOption(label='No Stone Unturned', emoji='<:No_Stone_Unturned:1174349176654528603>', description="Discard"),
        discord.SelectOption(label='Noodling', emoji='<:Noodling:1174349183344463952>', description="Discard"),
        discord.SelectOption(label='People Person', emoji='<:People_Person:1174349187014471730>', description="Discard"),
        discord.SelectOption(label='Pro Gamer', emoji='<:Pro_Gamer:1174349188490854500>', description="Discard"),
        discord.SelectOption(label='Shes A Natural', emoji='<:Shes_A_Natural:1174349191435264111>', description="Discard"),
        discord.SelectOption(label='Ship of Theseus', emoji='<:Ship_of_Theseus:1174349534701309982>', description="Discard"),
        discord.SelectOption(label='The Pentaverate', emoji='<:The_Pentaverate:1174349537700220978>', description="Discard"),
        discord.SelectOption(label='Unlimited Power', emoji='<:Unlimited_Power:1174349540267151483>', description="Discard"),
        discord.SelectOption(label='Unplanned Reunion', emoji='<:Unplanned_Reunion:1174349545304494151>', description="Discard")
        ],
        custom_id="1"
        )
    async def select_callback(self, interaction, select):
        select.disabled=True
        await interaction.response.edit_message(view=self)
        
        author = interaction.user.name
        author_id = interaction.user.id

        # Load existing data from the file
        with open(data_file_path, 'r') as f:
            data = json.load(f)

        if str(author_id) in list(data):
            if str(select.values[0]) in list(data[str(author_id)]):
                msg = await interaction.followup.send(f'Hey {interaction.user.mention}, you already have this badge!')
            else:                
                with open(data_file_path, 'w') as f:    
                    # Add the user to the data and save it
                    data[str(author_id)].update({str(select.values[0]): True})
                    json.dump(data, f, indent=4)
                values = ", ".join(select.values)
                msg = await interaction.followup.send(f'{interaction.user.mention} has obtained the **{values}** badges!')
        else:
            with open(data_file_path, 'w') as f:    
                # Add the user to the data and save it
                data[author_id] = { "name": author,
                                    str(select.values[0]): True}
                json.dump(data, f, indent=4)
            msg = await interaction.followup.send(f'{interaction.user.mention} has obtained their first badge: {select.values[0]}!')

class DeleteView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.select(
        placeholder="Choose a badge to drop!",
        options=[
        discord.SelectOption(label='All Out Of Options', emoji='<:All_Out_Of_Options:1174349162112888882>', description="Have only four cards remaining in the challenge deck."),
        discord.SelectOption(label='Big Tech', emoji='<:Big_Tech:1174349163627032636>', description="Discard a gear with 10 or more tokens on it using Moment of Desperation."),
        discord.SelectOption(label='Electric Slide', emoji='<:Electric_Slide:1174349165799682048>', description="Discard"),
        discord.SelectOption(label='Enough Already', emoji='<:Enough_Already:1174349167364157532>', description="Discard"),
        discord.SelectOption(label='Hard Pass', emoji='<:Hard_Pass:1174349170971246653>', description="Discard"),
        discord.SelectOption(label="Howd That Get in There", emoji='<:Howd_That_Get_in_There:1174349173764665466>', description="Discard"),
        discord.SelectOption(label='Long Flume', emoji='<:Log_Flume:1174349175169745018>', description="Discard"),
        discord.SelectOption(label='No Stone Unturned', emoji='<:No_Stone_Unturned:1174349176654528603>', description="Discard"),
        discord.SelectOption(label='Noodling', emoji='<:Noodling:1174349183344463952>', description="Discard"),
        discord.SelectOption(label='People Person', emoji='<:People_Person:1174349187014471730>', description="Discard"),
        discord.SelectOption(label='Pro Gamer', emoji='<:Pro_Gamer:1174349188490854500>', description="Discard"),
        discord.SelectOption(label='Shes A Natural', emoji='<:Shes_A_Natural:1174349191435264111>', description="Discard"),
        discord.SelectOption(label='Ship of Theseus', emoji='<:Ship_of_Theseus:1174349534701309982>', description="Discard"),
        discord.SelectOption(label='The Pentaverate', emoji='<:The_Pentaverate:1174349537700220978>', description="Discard"),
        discord.SelectOption(label='Unlimited Power', emoji='<:Unlimited_Power:1174349540267151483>', description="Discard"),
        discord.SelectOption(label='Unplanned Reunion', emoji='<:Unplanned_Reunion:1174349545304494151>', description="Discard")
        ],
        custom_id="2"
        )
    async def select_callback(self, interaction, select):
        select.disabled=True
        await interaction.response.edit_message(view=self)
        
        author = interaction.user.name
        author_id = interaction.user.id

        # Load existing data from the file
        with open(data_file_path, 'r') as f:
            data = json.load(f)

        if str(author_id) in list(data):
            if str(select.values[0]) in list(data[str(author_id)]):
                with open(data_file_path, 'w') as f: 
                    data[str(author_id)].pop(str(select.values[0]))
                    json.dump(data, f, indent=4)
                msg = await interaction.followup.send(f'{interaction.user.mention} dropped **{select.values[0]}**.')
            else:                
                msg = await interaction.followup.send(f"Hey {interaction.user.mention}, you still don't have this badge!")
        else:
            await interaction.followup.send("You haven't obtained a badge yet!\nGo and explore The Valley to get your first badge or use the `/badges` command to grab one.")   



@client.tree.command(name="grab_badges", description = "Get badges for your achievements!")
async def grab_badges(interaction: discord.Interaction):
    view = MySelectView()
    await interaction.response.send_message(view=view)

@client.tree.command(name="drop_badge", description = "Did you grab the wrong badge? Drop it!")
async def drop_badge(interaction: discord.Interaction):
    view = DeleteView()
    await interaction.response.send_message(view=view)

@client.tree.command(name="my_badges", description = "Flex your badges!")
async def my_badges(interaction: discord.Interaction):
    author_id = interaction.user.id
    # Load existing data from the file
    with open(data_file_path, 'r') as f:
        data = json.load(f)
    if str(author_id) in list(data):        
        embed0 = discord.Embed(title=f"{interaction.user.name} has obtained {len(list(data[str(author_id)])) - 1}/16!", description="Here are all your obtained badges!")
        for i in range(4):
            embeds = []
            for badge in (globals()[f'badge_list{i}']):
                if str(badge) in list(data[str(author_id)]):
                    single_badge_list = badge.split()
                    b_a_d_g_e = "_".join(single_badge_list)
                    embed = discord.Embed(url = 'https://github.com/filippopence/dragncards-ebr-plugin/wiki').set_image(url= f'https://earthborne-rangers.s3.eu-west-3.amazonaws.com/background-and-tokens/badges/{b_a_d_g_e}.png')
                else:
                    single_badge_list = badge.split()
                    b_a_d_g_e = "_".join(single_badge_list)
                    embed = discord.Embed(url = 'https://github.com/filippopence/dragncards-ebr-plugin/wiki').set_image(url= f'https://earthborne-rangers.s3.eu-west-3.amazonaws.com/background-and-tokens/badges/{b_a_d_g_e}_b&w.png')
                embeds.append(embed)
            if i == 0:
                await interaction.response.send_message(embeds=[embed0] + embeds)
            else:
                await interaction.followup.send(embeds=embeds)
    else:
        await interaction.response.send_message("You haven't obtained a badge yet!\nGo and explore The Valley to get your first badge or use the `/badges` command to grab one.")   
       










### COMMANDS


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
    #"[": "<:", 
    "[harm]": "<:harm:1081588151530819644>",
    "[progress]": "<:progress:1081588156509462640>",
    "[reason]": "<:reason:1081588160779255938>",
    "[exploration]": "<:exploration:1081588142093635644>",
    "[connection]": "<:connection:1081588137987424286>",
    "[conflict]": "<:conflict:1081588168807153726>",
    "[ranger]": "<:ranger:1081588158849880169>"
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
    message = " ".join(message)
    cc = message
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
    message = " ".join(message)
    cc = message
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
    message = " ".join(message)
    cc = message
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
WHEN = datetime.time(13, 0, 5)   # set time here in UTC 
CHANNEL_ID = 1161012075460571167 # Put your channel id here

@tasks.loop(time=WHEN) 
async def card_of_the_day():
    channel = client.get_channel(CHANNEL_ID)
    pinned_messages = await channel.pins()
    for message in pinned_messages:
        await message.unpin()
        print(f"Unpinned message content: {message.content}")
    i = random.randint(1,len(CardListDay))
    await channel.send("**Card of the day!**")
    card = await channel.send(CardListDay[i]['imagesrc'])
    emojis = ["\u0031\ufe0f\u20e3", '\u0032\ufe0f\u20e3', '\u0033\ufe0f\u20e3', '\u0034\ufe0f\u20e3', '\u0035\ufe0f\u20e3']
    time.sleep(0.5)
    for emoji in emojis:
        await card.add_reaction(emoji)
    await card.pin()


# .day command
@client.command()
@commands.has_role(869589665043349504)  # ONLY USERS WITH THIS ROLE CAN USE THIS COMMAND
async def erday(ctx):
    channel = client.get_channel(CHANNEL_ID)
    pinned_messages = await channel.pins()
    for message in pinned_messages:
        await message.unpin()
        print(f"Unpinned message content: {message.content}")
    i = random.randint(1,len(CardListDay))
    await channel.send("**Card of the day!**")
    card = await channel.send(CardListDay[i]['imagesrc'])
    emojis = ["\u0031\ufe0f\u20e3", '\u0032\ufe0f\u20e3', '\u0033\ufe0f\u20e3', '\u0034\ufe0f\u20e3', '\u0035\ufe0f\u20e3']
    time.sleep(0.5)
    for emoji in emojis:
        await card.add_reaction(emoji)
    await card.pin()




@client.event
async def on_ready():
    card_of_the_day.start()
    print("Bot is Up and Ready!")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print("Warning: commands not synced!")


load_dotenv(find_dotenv())
client.run(os.getenv('TOKEN'))



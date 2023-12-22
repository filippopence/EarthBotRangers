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
    "role": "<:perranger:1082646522946138132>",
    } 

badge_dict = {'All Out Of Options': '<:All_Out_Of_Options:1174349162112888882>', 
        'Big Tech': '<:Big_Tech:1174349163627032636>', 
        'Electric Slide': '<:Electric_Slide:1174349165799682048>', 
        'Enough Already': '<:Enough_Already:1174349167364157532>', 
        'Hard Pass': '<:Hard_Pass:1174349170971246653>', 
        "Howd That Get in There": '<:Howd_That_Get_in_There:1174349173764665466>', 
        'Long Flume': '<:Log_Flume:1174349175169745018>', 
        'No Stone Unturned': '<:No_Stone_Unturned:1174349176654528603>', 
        'Noodling': '<:Noodling:1174349183344463952>', 
        'People Person': '<:People_Person:1174349187014471730>',
        'Pro Gamer': '<:Pro_Gamer:1174349188490854500>',
        'Shes A Natural': '<:Shes_A_Natural:1174349191435264111>', 
        'Ship of Theseus': '<:Ship_of_Theseus:1174349534701309982>', 
        'The Pentaverate': '<:The_Pentaverate:1174349537700220978>', 
        'Unlimited Power': '<:Unlimited_Power:1174349540267151483>', 
        'Unplanned Reunion': '<:Unplanned_Reunion:1174349545304494151>'
        }

badge_dict_bw = {'All Out Of Options': '<:All_Out_Of_Options_bw:1175611665430089738>', 
        'Big Tech': '<:Big_Tech:1175611667942486126>', 
        'Electric Slide': '<:Electric_Slide:1175611669548904488>', 
        'Enough Already': '<:Enough_Already:1175611670882689075>', 
        'Hard Pass': '<:Hard_Pass:1175611673512521809>', 
        "Howd That Get in There": '<:Howd_That_Get_in_There:1175611675584495616>', 
        'Long Flume': '<:Log_Flume:1175611678776377374>', 
        'No Stone Unturned': '<:No_Stone_Unturned:1175611680210829373>', 
        'Noodling': '<:Noodling:1175611682341523467>', 
        'People Person': '<:People_Person:1175611684254122144>',
        'Pro Gamer': '<:Pro_Gamer:1175611687072706702>',
        'Shes A Natural': '<:Shes_A_Natural:1175611688507166731>', 
        'Ship of Theseus': '<:Ship_of_Theseus:1175611690059038780>', 
        'The Pentaverate': '<:The_Pentaverate:1175611885832392755>', 
        'Unlimited Power': '<:Unlimited_Power:1175611693766811758>', 
        'Unplanned Reunion': '<:Unplanned_Reunion:1175611889389162566>'
        }

badge_list_of_list = [['All Out Of Options',
              'Big Tech',
              'Electric Slide',
              'Enough Already'],
            ['Hard Pass',
              "Howd That Get in There",
              'Long Flume',
              'No Stone Unturned'],
            ['Noodling',
              'People Person',
              'Pro Gamer',
              'Shes A Natural'],
            ['Ship of Theseus',
              'The Pentaverate',
              'Unlimited Power',
              'Unplanned Reunion']]


# File path for storing user information
data_file_path = 'users_badges.json'

# Check if the file exists, if not, create an empty file
if not os.path.exists(data_file_path):
    with open(data_file_path, 'w') as f:
        json.dump({}, f)




class MySelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.select(
        placeholder="Choose a badge to grab!",
        options=[
        discord.SelectOption(label='All Out Of Options', emoji='<:All_Out_Of_Options:1174349162112888882>', description="Have only four cards remaining in the challenge deck."),
        discord.SelectOption(label='Big Tech', emoji='<:Big_Tech:1174349163627032636>', description="Discard a gear with 10 or more tokens on it using Moment of Desperation."),
        discord.SelectOption(label='Electric Slide', emoji='<:Electric_Slide:1174349165799682048>', description="Complete the campaign using the Electric Fog weather every day."),
        discord.SelectOption(label='Enough Already', emoji='<:Enough_Already:1174349167364157532>', description="Play the same moment 10 times in one day."),
        discord.SelectOption(label='Hard Pass', emoji='<:Hard_Pass:1174349170971246653>', description="Finish the campaign without completing a single story mission."),
        discord.SelectOption(label="Howd That Get in There", emoji='<:Howd_That_Get_in_There:1174349173764665466>', description="Add a card without the printed flora trait to Hy’s soup."),
        discord.SelectOption(label='Long Flume', emoji='<:Log_Flume:1174349175169745018>', description="Travel from White Sky to Tumbledown in a single day."),
        discord.SelectOption(label='No Stone Unturned', emoji='<:No_Stone_Unturned:1174349176654528603>', description="Have every path card in the deck in play at the same time."),
        discord.SelectOption(label='Noodling', emoji='<:Noodling:1174349183344463952>', description="Catch a fish in the Black Mud."),
        discord.SelectOption(label='People Person', emoji='<:People_Person:1174349187014471730>', description="Clear three or more humans with the same test."),
        discord.SelectOption(label='Pro Gamer', emoji='<:Pro_Gamer:1174349188490854500>', description="Pet Oru 3R or more times during a single round."),
        discord.SelectOption(label='Shes A Natural', emoji='<:Shes_A_Natural:1174349191435264111>', description="Have Quisi cause a Cloudhive swarm to be discarded."),
        discord.SelectOption(label='Ship of Theseus', emoji='<:Ship_of_Theseus:1174349534701309982>', description="Replace every card in your deck with a reward card."),
        discord.SelectOption(label='The Pentaverate', emoji='<:The_Pentaverate:1174349537700220978>', description="Have five humans within reach of one Ranger at the same time."),
        discord.SelectOption(label='Unlimited Power', emoji='<:Unlimited_Power:1174349540267151483>', description="Have 7 or more energy in a single aspect."),
        discord.SelectOption(label='Unplanned Reunion', emoji='<:Unplanned_Reunion:1174349545304494151>', description="Have Dace and Aell in play at the same time.")
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
                msg = await interaction.followup.send(f'{interaction.user.mention} has obtained the **{values}** badge!')
        else:
            with open(data_file_path, 'w') as f:    
                # Add the user to the data and save it
                data[author_id] = { "name": author,
                                    str(select.values[0]): True}
                json.dump(data, f, indent=4)
            msg = await interaction.followup.send(f'{interaction.user.mention} has obtained their first badge: **{select.values[0]}**!')

class DeleteView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.select(
        placeholder="Choose a badge to drop!",
        options=[
        discord.SelectOption(label='All Out Of Options', emoji='<:All_Out_Of_Options:1174349162112888882>', description="Have only four cards remaining in the challenge deck."),
        discord.SelectOption(label='Big Tech', emoji='<:Big_Tech:1174349163627032636>', description="Discard a gear with 10 or more tokens on it using Moment of Desperation."),
        discord.SelectOption(label='Electric Slide', emoji='<:Electric_Slide:1174349165799682048>', description="Complete the campaign using the Electric Fog weather every day."),
        discord.SelectOption(label='Enough Already', emoji='<:Enough_Already:1174349167364157532>', description="Play the same moment 10 times in one day."),
        discord.SelectOption(label='Hard Pass', emoji='<:Hard_Pass:1174349170971246653>', description="Finish the campaign without completing a single story mission."),
        discord.SelectOption(label="Howd That Get in There", emoji='<:Howd_That_Get_in_There:1174349173764665466>', description="Add a card without the printed flora trait to Hy’s soup."),
        discord.SelectOption(label='Long Flume', emoji='<:Log_Flume:1174349175169745018>', description="Travel from White Sky to Tumbledown in a single day."),
        discord.SelectOption(label='No Stone Unturned', emoji='<:No_Stone_Unturned:1174349176654528603>', description="Have every path card in the deck in play at the same time."),
        discord.SelectOption(label='Noodling', emoji='<:Noodling:1174349183344463952>', description="Catch a fish in the Black Mud."),
        discord.SelectOption(label='People Person', emoji='<:People_Person:1174349187014471730>', description="Clear three or more humans with the same test."),
        discord.SelectOption(label='Pro Gamer', emoji='<:Pro_Gamer:1174349188490854500>', description="Pet Oru 3R or more times during a single round."),
        discord.SelectOption(label='Shes A Natural', emoji='<:Shes_A_Natural:1174349191435264111>', description="Have Quisi cause a Cloudhive swarm to be discarded."),
        discord.SelectOption(label='Ship of Theseus', emoji='<:Ship_of_Theseus:1174349534701309982>', description="Replace every card in your deck with a reward card."),
        discord.SelectOption(label='The Pentaverate', emoji='<:The_Pentaverate:1174349537700220978>', description="Have five humans within reach of one Ranger at the same time."),
        discord.SelectOption(label='Unlimited Power', emoji='<:Unlimited_Power:1174349540267151483>', description="Have 7 or more energy in a single aspect."),
        discord.SelectOption(label='Unplanned Reunion', emoji='<:Unplanned_Reunion:1174349545304494151>', description="Have Dace and Aell in play at the same time.")
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
#======================#
#   SLASH COMMANDS
#======================#

# BADGES
@client.tree.command(name="grab_badge", description = "Get badges for your achievements!")
async def grab_badge(interaction: discord.Interaction):
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
        embed = discord.Embed(title=f"Hey {interaction.user.name}, you have obtained {len(list(data[str(author_id)])) - 1}/16!", description="Here are all your obtained badges!")
        for badge_list in badge_list_of_list:
            for badge in badge_list:#(globals()[f'badge_list{i}']):
                if str(badge) in list(data[str(author_id)]):
                    print(badge_dict[str(badge)])
                    embed.add_field(name='', value=f"{badge_dict[str(badge)]} **{badge}**")
                else:
                    embed.add_field(name='', value=f"{badge_dict_bw[str(badge)]} {badge}")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("You haven't obtained a badge yet!\nGo and explore The Valley to get your first badge or use the `/badges` command to grab one.")   

@client.tree.command(name="my_badges_two", description = "Flex your badges!")
async def my_badges_two(interaction: discord.Interaction):
    author_id = interaction.user.id
    BADGES_CHANNEL_ID = 1082647909364924526
    badges_channel = await interaction.guild.fetch_channel(BADGES_CHANNEL_ID)
    # Load existing data from the file
    with open(data_file_path, 'r') as f:
        data = json.load(f)
    if str(author_id) in list(data):        
        embed0 = discord.Embed(title=f"{interaction.user.name} has obtained {len(list(data[str(author_id)])) - 1}/16!", description="Here are all your obtained badges!")
        for badge_list in badge_list_of_list:
            embeds = []
            for badge in badge_list:#(globals()[f'badge_list{i}']):
                if str(badge) in list(data[str(author_id)]):
                    single_badge = badge.split()
                    b_a_d_g_e = "_".join(single_badge)
                    embed = discord.Embed(url = 'https://github.com/filippopence/dragncards-ebr-plugin/wiki').set_image(url= f'https://earthborne-rangers.s3.eu-west-3.amazonaws.com/background-and-tokens/badges/{b_a_d_g_e}.png')
                else:
                    single_badge = badge.split()
                    b_a_d_g_e = "_".join(single_badge)
                    embed = discord.Embed(url = 'https://github.com/filippopence/dragncards-ebr-plugin/wiki').set_image(url= f'https://earthborne-rangers.s3.eu-west-3.amazonaws.com/background-and-tokens/badges/{b_a_d_g_e}_b&w.png')
                embeds.append(embed)
            if badge_list_of_list.index(badge_list) == 0:
                await badges_channel.send(embeds=[embed0] + embeds)
            else:
                await badges_channel.send(embeds=embeds)
    else:
        await badges_channel.send("You haven't obtained a badge yet!\nGo and explore The Valley to get your first badge or use the `/badges` command to grab one.")   
         



# GUESSING GAME
@client.tree.command(name="erguess", description= "Guessing game including only basic cards.")
async def erguess(interaction: discord.Interaction):
    i = random.randint(1,len(CardListDay))
    traits = CardListDay[i]['traits'].split("/")
    traits = list(map(lambda x : unidecode(x.strip()), traits))
    name = CardListDay[i]['name']
    print(i, name)
    dict_guess = {"<b>": "**",  # define desired replacements here
    "</b>": "**", 
    "<i>": "_", 
    "</i>": "_", 
    CardListDay[i]['name']: "This Card", 
    #"[": "<:", 
    "[harm]": "<:harm:1081588151530819644>",
    "[progress]": "<:progress:1081588156509462640>",
    "[reason]": "<:reason:1081588160779255938>",
    "[exploration]": "<:exploration:1081588142093635644>",
    "[connection]": "<:connection:1081588137987424286>",
    "[conflict]": "<:conflict:1081588168807153726>",
    "[ranger]": "<:ranger:1081588158849880169>"
    } 
    embed = discord.Embed(title = "What's the card?", description = "Guess the card name typing `is <query>`", color= discord.Color.green(), timestamp = datetime.datetime.now())
    
    if any(x == CardListDay[i]['type_name'] for x in ['Gear', 'Attachment', 'Attribute']):          # GEAR, ATTACHMENT, ATTRIBUTE
        embed.add_field(name = "Cost", value = CardListDay[i]['cost'])
        embed.add_field(name= "Type and traits", value = f"{CardListDay[i]['type_name']} / _{CardListDay[i]['traits']}_")
        if CardListDay[i]['sphere_code'] == 'awareness':
            card_sphere = '<:awareness:1081702479290450031>'
        elif CardListDay[i]['sphere_code'] == 'focus':
            card_sphere = '<:focus:1081702483568623696>'
        elif CardListDay[i]['sphere_code'] == 'fitness':
            card_sphere = '<:fitness:1081702482012549170>'
        elif CardListDay[i]['sphere_code'] == 'spirit':
            card_sphere = '<:spirit:1081702484784992289>'
        embed.add_field(name = "Sphere", value = card_sphere)
        if CardListDay[i]['equip_value'] == 3:
            a, b, c = "<:white_large_square:1082277091472588950>", "<:white_large_square:1082277091472588950>", "<:white_large_square:1082277091472588950>"
            d, e = "<:white_square_button:1082277094274371594>", "<:white_square_button:1082277094274371594>"
            embed.add_field(name= "Equip value", value= f"{a} {b} {c} {d} {e}")
        if CardListDay[i]['equip_value'] == 2:
            a, b = "<:white_large_square:1082277091472588950>", "<:white_large_square:1082277091472588950>"
            c, d, e = "<:white_square_button:1082277094274371594>", "<:white_square_button:1082277094274371594>", "<:white_square_button:1082277094274371594>"
            embed.add_field(name= "Equip value", value= f"{a} {b} {c} {d} {e}")
        if CardListDay[i]['equip_value'] == 1:
            a = "<:white_large_square:1082277091472588950>"
            b, c, d, e = "<:white_square_button:1082277094274371594>", "<:white_square_button:1082277094274371594>", "<:white_square_button:1082277094274371594>", "<:white_square_button:1082277094274371594>"
            embed.add_field(name= "Equip value", value= f"{a} {b} {c} {d} {e}")
        if CardListDay[i]['generic_token'] != '':
            embed.add_field(name= "Token", value= CardListDay[i]['generic_token'])
        test_icon = []
        for num in range(CardListDay[i]['conflict_number']):
            test_icon.append("<:conflict:1081588168807153726>")
        for num in range(CardListDay[i]['connection_number']):
            test_icon.append("<:connection:1081588137987424286>")
        for num in range(CardListDay[i]['exploration_number']):
            test_icon.append("<:exploration:1081588142093635644>")
        for num in range(CardListDay[i]['reason_number']):
            test_icon.append("<:reason:1081588160779255938>")
        test_icon = str(test_icon)
        test_icon = test_icon.replace(',', '')
        test_icon = test_icon.replace('[', '')
        test_icon = test_icon.replace(']', '')
        test_icon = test_icon.replace("'", '')
        embed.add_field(name= "Test icons", value= test_icon)
        embed.add_field(name = "Text", value = replace_all(CardListDay[i]['text'], dict_guess))
        embed.add_field(name = "Flavor", value = CardListDay[i]['flavor'])
        embed.add_field(name = "Box", value = CardListDay[i]['pack_name'])
        embed.add_field(name = "Set", value = f"{CardListDay[i]['set']} - {CardListDay[i]['position']}")
        embed.add_field(name= "Attribute requirement", value= f"{CardListDay[i]['sphere_cost']} **{CardListDay[i]['sphere_name']}**")

    elif CardListDay[i]['type_name'] == 'Role':                                                     # ROLE
        embed.add_field(name= "Type and traits", value = f"{CardListDay[i]['type_name']}")
        embed.add_field(name = "Text", value = replace_all(CardListDay[i]['text'], dict_guess))
        embed.add_field(name = "Flavor", value = CardListDay[i]['flavor'])
        embed.add_field(name = "Box", value = CardListDay[i]['pack_name'])
        embed.add_field(name = "Set", value = f"{CardListDay[i]['set']} - {CardListDay[i]['position']}")
    
    elif CardListDay[i]['type_name'] == 'Moment':                                                   # MOMENT
        embed.add_field(name = "Cost", value = CardListDay[i]['cost'])
        embed.add_field(name= "Type and traits", value = f"{CardListDay[i]['type_name']} / _{CardListDay[i]['traits']}_")
        if CardListDay[i]['sphere_code'] == 'awareness':
            card_sphere = '<:awareness:1081702479290450031>'
        elif CardListDay[i]['sphere_code'] == 'focus':
            card_sphere = '<:focus:1081702483568623696>'
        elif CardListDay[i]['sphere_code'] == 'fitness':
            card_sphere = '<:fitness:1081702482012549170>'
        elif CardListDay[i]['sphere_code'] == 'spirit':
            card_sphere = '<:spirit:1081702484784992289>'
        embed.add_field(name = "Sphere", value = card_sphere)
        test_icon = []
        for num in range(CardListDay[i]['conflict_number']):
            test_icon.append("<:conflict:1081588168807153726>")
        for num in range(CardListDay[i]['connection_number']):
            test_icon.append("<:connection:1081588137987424286>")
        for num in range(CardListDay[i]['exploration_number']):
            test_icon.append("<:exploration:1081588142093635644>")
        for num in range(CardListDay[i]['reason_number']):
            test_icon.append("<:reason:1081588160779255938>")
        test_icon = str(test_icon)
        test_icon = test_icon.replace(',', '')
        test_icon = test_icon.replace('[', '')
        test_icon = test_icon.replace(']', '')
        test_icon = test_icon.replace("'", '')
        embed.add_field(name= "Test icons", value= test_icon)
        embed.add_field(name = "Text", value = replace_all(CardListDay[i]['text'], dict_guess))
        embed.add_field(name = "Flavor", value = CardListDay[i]['flavor'])
        embed.add_field(name = "Box", value = CardListDay[i]['pack_name'])
        embed.add_field(name = "Set", value = f"{CardListDay[i]['set']} - {CardListDay[i]['position']}")
        embed.add_field(name= "Attribute requirement", value= f"{CardListDay[i]['sphere_cost']} **{CardListDay[i]['sphere_name']}**")

    elif CardListDay[i]['type_name'] == 'Being':                                                    # BEING  
        embed.add_field(name = "Cost", value = CardListDay[i]['cost'])
        embed.add_field(name= "Type and traits", value = f"{CardListDay[i]['type_name']} / _{CardListDay[i]['traits']}_")
        if CardListDay[i]['sphere_code'] == 'awareness':
            card_sphere = '<:awareness:1081702479290450031>'
        elif CardListDay[i]['sphere_code'] == 'focus':
            card_sphere = '<:focus:1081702483568623696>'
        elif CardListDay[i]['sphere_code'] == 'fitness':
            card_sphere = '<:fitness:1081702482012549170>'
        elif CardListDay[i]['sphere_code'] == 'spirit':
            card_sphere = '<:spirit:1081702484784992289>'
        embed.add_field(name = "Sphere", value = card_sphere)
        test_icon = []
        for num in range(CardListDay[i]['conflict_number']):
            test_icon.append("<:conflict:1081588168807153726>")
        for num in range(CardListDay[i]['connection_number']):
            test_icon.append("<:connection:1081588137987424286>")
        for num in range(CardListDay[i]['exploration_number']):
            test_icon.append("<:exploration:1081588142093635644>")
        for num in range(CardListDay[i]['reason_number']):
            test_icon.append("<:reason:1081588160779255938>")
        test_icon = str(test_icon)
        test_icon = test_icon.replace(',', '')
        test_icon = test_icon.replace('[', '')
        test_icon = test_icon.replace(']', '')
        test_icon = test_icon.replace("'", '')
        embed.add_field(name= "Test icons", value= test_icon)
        embed.add_field(name= "Presence", value= CardListDay[i]['presence'])
        embed.add_field(name= "Harm", value= CardListDay[i]['harm_threshold'])
        embed.add_field(name = "Text", value = replace_all(CardListDay[i]['text'], dict_guess))
        embed.add_field(name = "Flavor", value = CardListDay[i]['flavor'])
        embed.add_field(name = "Box", value = CardListDay[i]['pack_name'])
        embed.add_field(name = "Set", value = f"{CardListDay[i]['set']} - {CardListDay[i]['position']}")
        embed.add_field(name= "Attribute requirement", value= f"{CardListDay[i]['sphere_cost']} **{CardListDay[i]['sphere_name']}**")
    
    elif CardListDay[i]['type_name'] == 'Feature':                                                  # FEATURE  
        embed.add_field(name = "Cost", value = CardListDay[i]['cost'])
        embed.add_field(name= "Type and traits", value = f"{CardListDay[i]['type_name']} / _{CardListDay[i]['traits']}_")
        if CardListDay[i]['sphere_code'] == 'awareness':
            card_sphere = '<:awareness:1081702479290450031>'
        elif CardListDay[i]['sphere_code'] == 'focus':
            card_sphere = '<:focus:1081702483568623696>'
        elif CardListDay[i]['sphere_code'] == 'fitness':
            card_sphere = '<:fitness:1081702482012549170>'
        elif CardListDay[i]['sphere_code'] == 'spirit':
            card_sphere = '<:spirit:1081702484784992289>'
        embed.add_field(name = "Sphere", value = card_sphere)
        test_icon = []
        for num in range(CardListDay[i]['conflict_number']):
            test_icon.append("<:conflict:1081588168807153726>")
        for num in range(CardListDay[i]['connection_number']):
            test_icon.append("<:connection:1081588137987424286>")
        for num in range(CardListDay[i]['exploration_number']):
            test_icon.append("<:exploration:1081588142093635644>")
        for num in range(CardListDay[i]['reason_number']):
            test_icon.append("<:reason:1081588160779255938>")
        test_icon = str(test_icon)
        test_icon = test_icon.replace(',', '')
        test_icon = test_icon.replace('[', '')
        test_icon = test_icon.replace(']', '')
        test_icon = test_icon.replace("'", '')
        embed.add_field(name= "Test icons", value= test_icon)
        embed.add_field(name= "Presence", value= CardListDay[i]['presence'])
        embed.add_field(name= "Progress", value= CardListDay[i]['progress_threshold'])
        embed.add_field(name = "Text", value = replace_all(CardListDay[i]['text'], dict_guess))
        embed.add_field(name = "Flavor", value = CardListDay[i]['flavor'])
        embed.add_field(name = "Box", value = CardListDay[i]['pack_name'])
        embed.add_field(name = "Set", value = f"{CardListDay[i]['set']} - {CardListDay[i]['position']}")
        embed.add_field(name= "Attribute requirement", value= f"{CardListDay[i]['sphere_cost']} **{CardListDay[i]['sphere_name']}**")
    
    embed.set_footer(text=f"I'm thinking of a card... Try to guess which one!")
    await interaction.response.send_message(embed=embed)
    tries = 0
    def check(m: discord.Message):
        return m.channel == interaction.channel #m.author == interaction.author and 
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
                embed = discord.Embed(title = "You guessed correctly!", description = "The card was:", color= discord.Color.green())
                embed.set_image(url = data[i]['imagesrc'])
                await interaction.followup.send(embed=embed)
                break
            else:
                await interaction.followup.send(f"Nope.\n{4-tries} attempts left.")
                if tries == 4:
                    embed = discord.Embed(title = "Game lost, try again!", description = "The card was:", color= discord.Color.green())
                    embed.set_image(url = data[i]['imagesrc'])
                    await interaction.followup.send(embed=embed)
                    break
                tries += 1
        elif guess.content.startswith('idk'):
            embed = discord.Embed(title = "Game lost, try again!", description = "The card was:", color= discord.Color.green())
            embed.set_image(url = data[i]['imagesrc'])
            await interaction.followup.send(embed=embed)
            break
        else:
            pass


# SEARCH CARD
@client.tree.command(name="erimg", description= "Display the card you want.")
async def erimg(interaction: discord.Interaction, card_name: str):
    card_name = unidecode(card_name).upper()
    print(f"Looking for: {card_name}")
    def search(card_list, string):
        index_list = []
        for n in range(len(card_list)):
            if card_list[n].find(string) != -1:
                index_list.append(n)
        return index_list
    CardIndexes = search(CardListName, card_name)
    if len(CardIndexes) == len(CardList):
        await interaction.response.send_message('I am sorry, but I need at least a name to find a card')
    elif len(CardIndexes) == 1:
        if CardList[CardIndexes[0]]['set'] == 'Reward':
            await interaction.response.send_message(f"|| {CardList[CardIndexes[0]]['imagesrc']} ||")
        else:
            await interaction.response.send_message(CardList[CardIndexes[0]]['imagesrc'])
        try:
            await interaction.response.send_message(CardList[CardIndexes[0]]['imagesrc2'])
        except:
            pass
    elif len(CardIndexes) == 0:
        await interaction.response.send_message(f"No cards found matching '{card_name}'.")
    else:
        cards_found = []
        if len(CardIndexes) > 20:
            max = 20
            await interaction.response.send_message(f"I've found {len(CardIndexes)} cards (Sending 20). Reply with the number of the one you want")
        else:
            max = len(CardIndexes)
            await interaction.response.send_message(f"I've found {len(CardIndexes)} cards. Reply with the number of the one you want")
        for ids in range(max):
            sphere = replace_all(CardList[CardIndexes[int(ids)]]['sphere_code'], dict)
            cards_found.append((f"{ids+1}. {sphere} **{CardList[CardIndexes[int(ids)]]['name']}**\n_{CardList[CardIndexes[int(ids)]]['type_name']}_ ({CardList[CardIndexes[int(ids)]]['pack_name']})"))
        await interaction.followup.send('\n'.join(cards_found))
        def check(m: discord.Message):
            return m.channel == interaction.channel #m.author == ctx.author and 
        for j in range(1):
            id = await client.wait_for('message', check=check)
            id = id.content
            try:
                if CardList[CardIndexes[int(id)-1]]['set'] == 'Reward':
                    await interaction.followup.send(f"|| {CardList[CardIndexes[int(id)-1]]['imagesrc']} ||")
                else:
                    await interaction.followup.send(CardList[CardIndexes[int(id)-1]]['imagesrc'])
            except:
                await interaction.followup.send("You have to type the number of the card you want!")
            try:
                await interaction.followup.send(CardList[CardIndexes[int(id)-1]]['imagesrc2'])
            except:
                pass

      






### COMMANDS


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
    await channel.send(f"**Card of the day: {CardListDay[i]['name']}**")
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
client.run(os.getenv('TESTER_BOT'))



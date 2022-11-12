from bs4 import BeautifulSoup
import requests
from xlwt import Workbook

def HarvestInsta(tag):
    wb = Workbook()
    sheet = wb.add_sheet('Data')
    sheet.write(0,0,"Name")
    sheet.write(0,1,"Handle")
    sheet.write(0,2,"Followers")
    sheet.write(0,3,"Engagement")
    sheet.write(0,4,"Likes/Post")
    url = f"https://ninjaoutreach.com/search?categories_or={tag}"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    names = doc.findAll("div", {"class": "profile-name"})
    ids = doc.findAll("div", {"class": "profile-id"})
    cardfollowers = doc.findAll("div", {"class": "profile-value-large"})
    cardstats = doc.findAll("div", {"class": "profile-value"})
    current_index = 0
    card_index = 0
    stat_index = 3
    for name in names:
        print("\t---------------------------------")
        print(f"{name.string}{ids[current_index].string}{cardfollowers[current_index].string}")
        sheet.write(current_index+1,0,name.string)
        sheet.write(current_index+1,1,ids[current_index].string)
        sheet.write(current_index+1,2,cardfollowers[current_index].string)
        for i in range(card_index, card_index + 2):
            print(cardstats[i].string)
            sheet.write(current_index+1, stat_index, cardstats[i].string)
            stat_index+=1
        card_index += 2
        stat_index = 3
        current_index+=1
    wb.save("..//output.xls")


def HarvestYoutube(tag):
    wb = Workbook()
    sheet = wb.add_sheet('Data')
    sheet.write(0,0,"Name")
    sheet.write(0,1,"Engagement")
    sheet.write(0,2,"Avg Likes")
    sheet.write(0,3,"Subscribers")
    url = f"https://ninjaoutreach.com/youtube-influencers?categories_or={tag}"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    names = doc.findAll("div", {"class": "channel-title"})
    cardstats = doc.findAll(class_ = "card__stats__value")
    current_index = 0
    name_index = 1
    stat_index = 1
    for name in names:
        print("\t---------------------------------")
        print(name.string)
        sheet.write(name_index, 0, name.string)
        for i in range(current_index, current_index + 3):
            print(cardstats[i].string)
            sheet.write(name_index, stat_index, cardstats[i].string)
            stat_index+=1
        current_index+=3
        name_index+=1
        stat_index=1
    wb.save("..//output.xls")

def GetTags(type):
    if int(type) == 1:
        url = "https://ninjaoutreach.com/search"
    else:
        url = "https://ninjaoutreach.com/youtube-influencers"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    tags = doc.findAll("a", {"class": "category-tag"})
    for tag in tags:
        print(f"\t>{tag['data-value']}")
    

def Menu():
    print("""
    ---------------------------------
    |        [NinjaScraper]         |
    |Developed - Alexander Griffiths|
    |                               |
    |   Harvest analytics:          |
    |   (1) Instagram               |
    |   (2) Youtube                 |
    |   (3) Quit                    |
    |                               |
    ---------------------------------
    """)
    harvesttype = input("\n\t[INPUT]:")
    print("\n")
    GetTags(harvesttype)
    print("\n\tFilter by...")
    tag = input("\n\t[INPUT]: ")
    return harvesttype, tag

def Error(code):
    print(f"[FAILED]: Exception caught make sure connected to internet and spreadsheet is not open. [ERRORCODE - {code}]")

def Main():
    harvesttype, tag = Menu()
    if int(harvesttype) == 1:
        try:
            print(f"[INFO]: Harvesting Instagram influencer details using filter {tag}")
            HarvestInsta(tag)
        except:
            Error(1)
    elif int(harvesttype) == 2:
        try:
            print(f"[INFO]: Harvesting Youtube influencer details using filter {tag}")
            HarvestYoutube(tag)
        except:
            Error(1)
    else:
        print("Wrong input quitting...")
        exit(0)
    input("Quit with any key...")

if __name__ == "__main__":
    Main()
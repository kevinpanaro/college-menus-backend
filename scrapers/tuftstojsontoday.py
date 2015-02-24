# Gets TuftsToday.json
def tuftstoday():
    from bs4 import BeautifulSoup as bs
    import urllib2
    import os
    from datetime import date, timedelta

    try:
        import simplejson as json
    except:
        import json

    #HTML parsing. Define this first for easy reusability.


    def parse_meal_html(table):
        result = []
        current_category = []
        for item in table.findAll("div"):
            if "shortmenucats" in item["class"]:
                # If we get to a new category and the old category is full,
                # save the old category to result.
                if len(current_category) > 0:
                    result.append(current_category)
                    current_category = []
                # Regardless of the previous state of old category, remove leading
                # and trailing non-alpha characters. Then save the category.
                new_cat = "".join(item.findAll(text=True))
                # Remove spaces and hyphens.
                new_cat = new_cat.strip('- ').title()
                current_category.append(new_cat)
            if "shortmenurecipes" in item["class"]:
                current_category.append("".join(item.findAll(text=True)))
        # Catch the last category.
        result.append(current_category)
        # Save it all as a dict.
        dict_result = {}
        for category in result:
            title = category[0]
            dict_result[title] = []
            for food in category[1:]:
                dict_result[title].append(food)
        return dict_result


    #Dining hall to menu URL relationships
    today = date.today()
    url_date = "&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=" + today.strftime('%D')
    name_to_url = {
        "Dewick-MacPhie":
            "http://menus.tufts.edu/foodpro/shortmenu.asp?s"
            "Name=Tufts+Dining"
            "&locationNum=11"
            "&locationName=Dewick+MacPhie+Dining+Center"
            "&naFlag=1" + url_date,
        "Carmichael":
            "http://menus.tufts.edu/foodpro/shortmenu.asp?s"
            "Name=Tufts+Dining"
            "&locationNum=09"
            "&locationName=Carmichael+Dining+Center"
            "&naFlag=1" + url_date,
        "Commons":
            "http://menus.tufts.edu/foodpro/shortmenu.asp?s"
            "Name=Tufts+Dining"
            "&locationNum=03"
            "&locationName=The+Commons+Deli+%26+Grill"
            "&naFlag=1" + url_date,
        "Hodgdon":
            "http://menus.tufts.edu/foodpro/shortmenu.asp?s"
            "Name=Tufts+Dining"
            "&locationNum=14"
            "&locationName=Hodgdon+Good-+To-+Go+Take-+Out"
            "&naFlag=1" + url_date,
        "Mugar Cafe":
            "http://menus.tufts.edu/foodpro/shortmenu.asp?s"
            "Name=Tufts+Dining"
            "&locationNum=15"
            "&locationName=Mugar+Cafe"
            "&naFlag=1" + url_date,
    }

    # Locations holds a list(aka array) of {locations:[{"location":name, "meals":menus}, ...]}
    locations = []

    for key in name_to_url:
        URL = name_to_url[key]
        try:
            response = urllib2.urlopen(URL)
            html = response.read()
            soup = bs(html)
            #Mucky Scraping/Parsing - C'est la vie.
            # Pick out the breakfast, lunch, dinner tables by some specific attributes.
            tables = soup.findAll("table", width="100%", cellpadding="0", cellspacing="1")
            #Sometimes a dining hall doesn't server breakfast. When there isn't a breakfast column,
            #we need to adjust the indices.
            if len(tables) == 2:
                breakfast = []
                lunch = parse_meal_html(tables[0])
                dinner = parse_meal_html(tables[1])
            elif len(tables) == 3:
                breakfast = parse_meal_html(tables[0])
                lunch = parse_meal_html(tables[1])
                dinner = parse_meal_html(tables[2])
            else:
                # Sometimes a cafeteria isn't serving anything.
                breakfast = []
                lunch = []
                dinner = []
        except:
            # If something fails.. set up a blank one.
            breakfast = []
            lunch = []
            dinner = []
        location = {
            "location": key,
            "meals": {
                "Breakfast": breakfast,
                "Lunch": lunch,
                "Dinner": dinner
                }
            }
        locations.append(location)

    ########## KEV EDIT #########
    date_today_folder = date.today().strftime("%Y%m%d")
    ###### end of KEV EDIT ######

    # Save the json file.
    os.chdir('../dates/')
    path = os.path.join(os.getcwd(), date_today_folder + '/tufts.json')
    print "TuftsToday saved"
    with open(path, "w") as save_file:
        to_save = {"locations": locations, "date": today.strftime('%Y%m%d')}
        json.dump(to_save, save_file)


if __name__ == '__main__':
    tuftstoday()
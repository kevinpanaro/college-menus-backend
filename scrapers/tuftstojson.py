# Gets TuftsTomorrow.json
def tuftstomorrow():
    try:
        from BeautifulSoup import BeautifulSoup as bs
    except:
        from bs4 import BeautifulSoup as bs
    import urllib2
    import os
    import sys
    from datetime import date, timedelta

    try:
        import simplejson as json
    except:
        import json

    #Set up logging.
    import logging

    logging.basicConfig(filename='menuUpdate.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - tuftstojson - %(message)s')

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
                # Remove spaces and hyphens and fix capitalization.
                new_cat = new_cat.strip('- ').title()
                current_category.append(new_cat)
            #Add the food.
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

    def fix_Hodgdon(daily_selections):
        breakfast = {}
        lunch = {}
        dinner = {}
        for category, foods in daily_selections.iteritems():
            lowercat = category.lower()
            if (lowercat in  ["breakfast sandwiches"]):
                breakfast[category + " (Entree)"] = foods
            elif (lowercat in ["hot lunch sandwiches",
                                      "grilled hotdog station",
                                      "soups and chili"]):
                categoryToShow = category
                if (lowercat in ["hot lunch sandwiches"]):
                    categoryToShow += " (Entree)"
                lunch[categoryToShow] = foods
            elif (lowercat in ["churros caliente", 
                                      "churros toppings & sides", 
                                      "pan asia express", 
                                      "pan asia sides", 
                                      "roasters - bbq", 
                                      "roaster sides",
                                      "basils pasta grill",
                                      "soups and chili"]):
                categoryToShow = category
                if (lowercat not in ["soups and chili"]):
                    categoryToShow += " (Entree)"
                dinner[categoryToShow] = foods
            elif (lowercat in ["t-stop toppings"]):
                pass
            elif (lowercat in ["t-stop deli & wraps"]):
                lunch[category] = foods
                dinner[category] = foods
            else:
                breakfast[category] = foods
                lunch[category] = foods
                dinner[category] = foods
        return (breakfast, lunch, dinner)

    def fix_Commons(daily_selections):
        breakfast = {}
        lunch = {}
        dinner = {}
        for category, foods in daily_selections.iteritems():
            lowercat = category.lower()
            if (lowercat in ["hot bar"]):
                lunch[category + " (Entree)"] = foods
            elif(lowercat in ["after 5"]):
                dinner[category + " (Entree)"] = foods
            elif(lowercat in ["desserts & pastries"]):
                breakfast[category] = foods
            else:
                lunch[category] = foods
                dinner[category] = foods
        return (breakfast, lunch, dinner)

    def fix_Mugar(daily_selections):
        breakfast = {}
        lunch = {}
        dinner = {}
        for category, foods in daily_selections.iteritems():
            lowercat = category.lower()
            if (lowercat in ["starch & vegetables", "pasta", "daily hot entrees"]):
                if ("entree" not in lowercat): category += " (Entree)"
                lunch[category] = foods
            elif (lowercat in ["salads", "sandwiches"]):
                lunch[category] = foods
                dinner[category] = foods
            else:
                breakfast[category] = foods
                lunch[category] = foods
                dinner[category] = foods
        return (breakfast, lunch, dinner)

    #Dining hall to menu URL relationships
    tomorrow = date.today() + timedelta(days=1)
    url_date = "&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=" + tomorrow.strftime('%D')
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

    # name_to_url = {
    #     "Dewick-MacPhie":
    #         "/Users/Steve/Desktop/Dewick.html",
    #     "Carmichael":
    #         "/Users/Steve/Desktop/Carmichael.html",
    #     "Commons":
    #         "/Users/Steve/Desktop/Commons.html",
    #     "Hodgdon":
    #         "/Users/Steve/Desktop/Hodgdon.html",
    #     "Mugar Cafe":
    #         "/Users/Steve/Desktop/Mugar.html",
    # }

    # Locations holds a list(aka array) of {locations:[{"location":name, "meals":menus}, ...]}
    locations = []

    for key in name_to_url:
        URL = name_to_url[key]
        logging.debug("Fetching from URL %s" % URL)
        try:
            response = urllib2.urlopen(URL)
            html = response.read()
            # html = open(URL, 'r')
            soup = bs(html)
        except Exception, e:
            logging.exception("Failed to fetch menu. Error: %s" % e)
            # If something fails.. exit safely.
            sys.exit(0)
        if soup == None:
            logging.debug("Failed to create soup.")
            sys.exit(0)
        # Mucky Scraping/Parsing - C'est la vie.
        # Pick out the breakfast, lunch, dinner tables by some specific attributes. These tables include the meal name table.
        tables = soup.findAll("table", width="100%", height="100%", cellpadding="0", cellspacing="0")
        #Sometimes a dining hall doesn't serve every meal. Check the meal names.
        nameTableMap = {}
        for table in tables:
            #_class and find_all() aren't available until BeautifulSoup 4
            name = table.findAll(name="div", attrs={"class": "shortmenumeals"})[0].findAll(text=True)[0].lower()
            # This find_all removes the meal name table from the html by selecting the only other table.
            foodTable = table.findAll("table", width="100%", cellpadding="0", cellspacing="1")
            # If there is an empty table, then the text value will be a bunch of whitespace. In that case, there's no meal. 
            # Also, make sure there is a table. -- Should we? Is it better to have the app display wrong info for one location
            # or no menus for all locations? Actually, if they change the properties on the tables, all will fail. 
            # So it's better to not check and to let it fail, because, if we check, then we would probably show wrong menus
            # for ALL locations.
            if (foodTable[0].text.strip() != ""):
                nameTableMap[name] = parse_meal_html(foodTable[0])
        logging.debug("Found meals %s for location %s" % (nameTableMap.keys(), key))
        #Get the meal if it exists or set the meal as empty.
        breakfast = nameTableMap.get("breakfast", {})
        lunch = nameTableMap.get("lunch", {})
        dinner = nameTableMap.get("dinner", {})
        daily_selections = nameTableMap.get("daily menu selections", {})
        if (key == "Hodgdon"): 
            (breakfast, lunch, dinner) = fix_Hodgdon(daily_selections)
        if (key == "Commons"):
            (breakfast, lunch, dinner) = fix_Commons(daily_selections)
        if (key == "Mugar Cafe"):
            (breakfast, lunch, dinner) = fix_Mugar(daily_selections)
        location = {
            "location": key,
            "meals": {
                "Breakfast": breakfast,
                "Lunch": lunch,
                "Dinner": dinner
                }
            }
        locations.append(location)
        logging.debug("Successfully fetched %s" % key)

    ########## KEV EDIT #########
    date_tomorrow_folder = (date.today() + timedelta(days=1)).strftime("%Y%m%d")
    ###### end of KEV EDIT ######

    # Save the json file.
    os.chdir('../dates/')
    path = os.path.join(os.getcwd(), date_tomorrow_folder + '/tufts.json')
    print "TuftsTomorrow saved"
    with open(path, "w") as save_file:
        to_save = {"locations": locations, "date": tomorrow.strftime('%Y%m%d')}
        json.dump(to_save, save_file)
        logging.debug("Successfully saved file.")

if __name__ == '__main__':
    tuftstomorrow()
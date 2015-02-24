# Gets HarvardTomorrow.json
def harvardtomorrow():
    import json, urllib2, os
    from datetime import date, timedelta

    #Set up logging.
    import logging

    logging.basicConfig(filename='menuUpdate.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - harvardtojson - %(message)s')


    #Format URL.

    url_base = "http://food.cs50.net/api/1.3/menus?sdt="
    url_format = "&output=json"
    # Get tomorrow's date.
    tomorrow_date = date.today() + timedelta(days=1)
    url_date = tomorrow_date.strftime("%Y-%m-%d")

    URL = url_base + url_date + url_format

    logging.debug("Fetching from URL %s" % URL)


    ########## KEV EDIT #########
    date_tomorrow_folder = (date.today() + timedelta(days=1)).strftime("%Y%m%d")
    ###### end of KEV EDIT ######


    ##
    ## DEBUG ONLY
    ##
    #URL = "http://food.cs50.net/api/1.3/menus?sdt=2011-03-21&output=json"

    # Get json.

    try:
        response = urllib2.urlopen(URL)
        js = json.loads(response.read())
    except:
        logging.debug("Failed to fetch URL")
        js = {}

    # Format for app.

    location = {"location": "Annenberg", "meals": {}}
    meals = {}

    for item_dict in js:
        # meal_dict: a dict of categories in the meal
        meal_dict = meals.get(item_dict["meal"].title())
        if meal_dict == None:
            meals[item_dict["meal"].title()] = {}
            meal_dict = meals[item_dict["meal"].title()]
        # category_list: a list of foods in the category
        category_list = meal_dict.get(item_dict["category"].title())
        if category_list == None:
            meal_dict[item_dict["category"].title()] = []
            category_list = meal_dict[item_dict["category"].title()]
        category_list.append(item_dict["name"])

    location["meals"] = meals
    locations = [location]

    tomorrow = tomorrow_date
    logging.debug("Setting tomorrow's date to %s" % tomorrow.strftime('%y%m%d'))
    to_save = {"locations": locations, "date": tomorrow.strftime('%Y%m%d')}

    # Save the json.
    #### KEV EDIT AGAIN ####
    os.chdir('../dates/')
    path = os.path.join(os.getcwd(), date_tomorrow_folder + '/harvard.json')
    print "HarvardTomorrow saved"
    with open(path, "w") as f:
        json.dump(to_save, f)
        logging.debug("Successfully saved file.")


if __name__ == '__main__':
    harvardtomorrow()
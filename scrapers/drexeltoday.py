from scrapy.spider import Spider
from scrapy.selector import Selector
from urlparse import urljoin
from scrapy.http import Request               
# from college_menus.items import menu_items
import re
import datetime
import json

########################################################################
# you may have to insert a path to get it to work. this did it for me. #
#import sys                                                           #
#sys.path.insert(0, '/Users/kevinpanaro/college_menus/')              #
########################################################################



#############################################################
#############################################################
##                                                         ##
##         TO RUN: scrapy crawl menu_crawler_today         ##
##                                                         ##
#############################################################
#############################################################


###############
# MAIN SPIDER #
###############
class college_menus_spider(Spider):

    name = "menu_crawler_today"                                                                     # name of spider
    allowed_domains = ["www.drexelcampusdining.com"]                                                # only searches on this domain
    start_urls = ["http://www.drexelcampusdining.com/WeeklyMenu.htm"]                               # spider starts here
    

    #################################
    # finds menu items for each day #
    #################################
    def parse(self, response):

        # constants
        xpath_meals = ["brk", "lun", "din"]
        meal_names = ["Breakfast", "Lunch", "Dinner"]
        selected_date = [datetime.date.today().strftime("%m/%d/%Y"), datetime.date.today().strftime("%Y%m%d"), datetime.date.today().strftime("%A").lower()]

        sel = Selector(response)

        day_of_week_selector = ("//td[@id='" + selected_date[2] + "']")         # selects xpath for day of week
        station_list = []                                                       # will be list of stations
        station_counter = []                                                    # list of numbers where stations are in xpath
        

        ## Creates list of 3 lists, each of which are either breakfast, lunch, or dinner.
        for meal in range(len(xpath_meals)):
            temp_list = []
            temp_station_counter = []
            temp_list_2 = []
            meal_selector = day_of_week_selector + ("//tr[@class='" + xpath_meals[meal] + "']")
            station_names = (meal_selector + "//td[@class='station']/text()")
            temp_list.append(station_names)
            counter = -1
            while True:
                for item in sel.xpath(temp_list[0]).extract():
                    if len(item) > 1 and item[1::] not in temp_list_2:
                        temp_station_counter.append(counter)
                        temp_list_2.append(item[1::])
                    counter += 1
                break
            station_list.append(temp_list_2)
            station_counter.append(temp_station_counter)

        ## Grabs Meals. fucking hard to explain especially since i didnt make comments while making it
        meals_dict = {}
        for day in range(len(station_counter)):
            meal_selector = day_of_week_selector + ("//tr[@class='" + xpath_meals[day] + "']")
            meals = meal_selector + ("//td[@class='menuitem']/div[@class='menuitem']/span/text()")
            temp_dict = {}
            count = 0
            for station_name in range(len(station_counter[day])):
                temp_list = []
                if station_name == len(station_counter[day])-1:
                    for item_4 in range(station_counter[day][station_name], 900):
                        try:
                            meal_item = sel.xpath(meals).extract()[item_4]
                            temp_list.append(meal_item)
                        except IndexError:
                            break
                else:
                    count = station_counter[day][station_name]
                    for item_4 in range(count, station_counter[day][(station_name+1)]):
                        meal_item = sel.xpath(meals).extract()[item_4]
                        temp_list.append(meal_item.encode("utf-8"))
                temp_dict[(station_list[day][station_name])] = temp_list
            meals_dict[meal_names[day]] = temp_dict

        # these are the hours. they never change. next version these will be scraped cuz im anal
        hours_the_hans = {
            "Monday": ["07:00", "20:00"],
            "Tuesday": ["07:00", "20:00"],
            "Friday": ["07:00", "20:00"],
            "Wednesday": ["07:00", "20:00"],
            "Thursday": ["07:00", "20:00"],
            "Sunday": ["11:00", "19:30"],
            "Saturday": ["11:00", "19:30"]
        }


        # sets up final product
        final_dict = {}
        final_dict["date"] = str(selected_date[1])
        final_dict["locations"] = [{"location": "The Hans","meals": meals_dict, "hours" : hours_the_hans}]
        
        final_dict_json = (json.dumps(final_dict))
        
        # opens and writes to drexel.json
        f = open('drexel.json','w')
        f.write(final_dict_json) 
        f.close()



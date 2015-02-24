import os, shutil, datetime, subprocess, re, sys
from scrapers.harvardtojsontoday import harvardtoday
from scrapers.harvardtojson import harvardtomorrow
from scrapers.tuftstojson import tuftstomorrow
from scrapers.tuftstojsontoday import tuftstoday
from webserver import s3_upload




# constants
date_today_folder = datetime.date.today().strftime("%Y%m%d")
date_tomorrow_folder = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y%m%d")
date_yesterday_folder = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y%m%d")
date_today = datetime.date.today().strftime("%m/%d/%Y")
date_tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%m/%d/%Y")

def make_folders():
    '''
    This removes yesterday's folders, and creates two new folders for both today, and tomorrow.
    '''
    # Variables
    date_list = [date_today_folder, date_tomorrow_folder]

    # Folder make and remove
    file_path = os.path.dirname(__file__)       # variable to file path
    update_path = os.path.join(file_path, "dates")
    os.chdir(update_path)                         # changes working directory
    dates_file_path = os.path.join(os.getcwd())
    # Makes a directory according to date, replacing the old one, or creating a new one if none are there.
    if os.access(dates_file_path + "/" + date_yesterday_folder, os.F_OK) == True:
            shutil.rmtree(dates_file_path + "/" + date_yesterday_folder)
    for date in date_list:
        date_path = dates_file_path + "/" + date
        if os.access(date_path, os.F_OK) == True:
            shutil.rmtree(date_path)
            os.mkdir(date_path)
        else:
            os.mkdir(date_path)


def get_drexel_menus():
    ''' 
    It's gonna get menus... eventually...
    '''
    os.chdir("../scrapers")
    # Ugly, I know. Ghetto, I know.
    today_menu = 'scrapy runspider drexeltoday.py; cp ./drexel.json ../dates/' + date_today_folder
    tomorrow_menu = 'scrapy runspider drexeltomorrow.py; cp ./drexel.json ../dates/' + date_tomorrow_folder
    subprocess.call(today_menu, shell=True)
    subprocess.call(tomorrow_menu, shell=True)


def get_menus():
    # make sure your import the functions. duh.
    harvardtoday()
    harvardtomorrow()
    tuftstomorrow()
    tuftstoday()




if __name__ == '__main__':
    make_folders()
    get_drexel_menus()
    get_menus()
    s3_upload()
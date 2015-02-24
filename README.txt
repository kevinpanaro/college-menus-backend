sup.

backend.py is the main script. Run it (“python2.7 backend.py”) and everything will work. Hopefully. If anything messes up here it because of a path.

dates is the folder with the dates. This folder is whats uploaded to the s3.

menuUpdate.log is a file created by your scripts… doesn’t do anything with my scripts. I could probably get rid of it but it’s doesn’t hurt anything.

scrapers is the folder where all the scrapers are. When adding new scrapers, you can look at the changes I made to your scripts so that it saves them in the correct location. and then you need to just import them into backend.py and add it the get_menus function in backend.py

webserver.py uploads all the stuff to s3. change the access_key, access_secret, bucket_name, and final_dest variables to yours.

you might have to install scrapy (pip install scrapy).

end of shittiest README ever.
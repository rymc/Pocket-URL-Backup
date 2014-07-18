#!/usr/bin/python
import sqlite3, os, sys

def get_db_path():
	if os.name == 'nt':
		os_path_root = "C:/Users/"
		mozilla_dir = "/AppData/Roaming/Mozilla/Firefox/Profiles/"
	else:
		os_path_root= "/home/"
		mozilla_dir = "/.mozilla/firefox/"

	firefox_profile_path = os_path_root+os.getenv('USERNAME')+ mozilla_dir
	profile_name = os.listdir(firefox_profile_path)[0];

	return firefox_profile_path+profile_name+"/readItLater.sqlite"

def get_items(db_location):
	conn = sqlite3.connect(db_location)
	cur = conn.cursor()

	try:
		ut = cur.execute("SELECT url, title FROM items")
	except sqlite3.OperationalError as error:
		print "An error occurred.\nWe looked for the database at the following path: "+db_location
		print "Is this correct?"
		print "Here's the actual error: "+str(error)
		return -1
	else:
		items = ut.fetchall()
		return items
	finally:
		cur.close()
		conn.close()

def write_as_html(items):
	with open("pocket_links.html", "wb") as backup_file:
		backup_file.write("<html>\n\t<head><title>Pocket Links</title></head>\n\t<body>\n")

		for item in items:
			url = item[0].encode('ascii', 'ignore')
			title = item[1].encode('ascii', 'ignore')
		
			if title == "":
				title = url
			
			backup_file.write('\t\t<a href="'+url+'">')
			backup_file.write(title+"</a>")
			backup_file.write("<br /><br />\n")
			
		backup_file.write("\t</body>\n</html>")

db_location = get_db_path()
items = get_items(db_location)

if items == -1:
	sys.exit(-1)
	
items.reverse()
write_as_html(items)

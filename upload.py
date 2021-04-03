import datetime
import json
import mwclient
import os
import requests

# CONFIGURATION
# // Make sure your account is an admin!!! (Just in case)
url = "INSERT URL HERE"
useragent = "mwbackup/1.0 "
username = "INSERT USERNAME HERE"
password = "INSERT PASSWORD HERE"

# INITIALIZATION
site = mwclient.Site(host=url, reqs={"verify": False}, path="/", clients_useragent=useragent)
site.login(username, password)
if not site.logged_in:
    print("Failed to login >:(")
    exit(-1)

# WRITE DATA
pages_dir = "./pages"
images_dir = "./images"
if not os.path.exists(pages_dir):
    print("Error: Cannot find page data!")
    exit(-1)
if not os.path.exists(images_dir):
    print("Error: Cannot find image data!")
    exit(-1)
pages = []
for path, dirs, files in os.walk(pages_dir):
    for dir in dirs:
        pages.append((path.replace("\\", "/") + "/" + dir).replace("//", "/")[8:])
images = [d for d in os.listdir(images_dir) if os.path.isdir(images_dir + "/" + d)]
print("Found " + str(len(pages)) + " pages...")
print("Found " + str(len(images)) + " images...")

done = 0
for page in pages:
    if done < 2:
        done += 1
        continue
    revs = json.load(open(pages_dir + "/" + page + "/revs.json", "r", encoding="utf8"))
    meta = json.load(open(pages_dir + "/" + page + "/meta.json", "r", encoding="utf8"))
    print("Restoring page: " + meta["base_title"])
    _page = site.pages[meta["name"]]
    revs = sorted(revs, key=lambda rev: rev["revid"])
    for rev in revs:
        rev_file = open(pages_dir + "/" + page + "/" + str(rev["revid"]) + ".mw", "r", encoding="utf8")
        rev_text = rev_file.read()
        if len(rev_text) == 0:
            print("Skipped empty revision #" + str(rev["revid"]) + "...")
            continue
        timestr = datetime.datetime(rev["timestamp"][0], rev["timestamp"][1], rev["timestamp"][2], rev["timestamp"][3], rev["timestamp"][4], rev["timestamp"][5]).isoformat()
        comment = rev["comment"] if not rev["comment"].startswith("Created page with \"") else "(default message)"
        _page.edit(rev_text, "Restored Old Revision #" + str(rev["revid"]) + " by " + rev["user"] + " from " + timestr + " | " + comment)
        print("Restored revision: " + str(rev["revid"]))
    done += 1
    print("Completed: " + str(done) + "/" + str(len(pages)) + " (" + str(int((done / len(pages)) * 100)) + "%)")

exit(0)

done = 0
for image in images:
    meta = json.load(open(images_dir + "/" + image + "/meta.json", "r", encoding="utf8"))
    if done < 680:
        done += 1
        print("Skipped " + meta["base_title"])
        continue
    print("Restoring file: " + meta["base_title"])
    img_file = open(images_dir + "/" + image + "/" + image, "rb")
    uploadmsg = "Restored " + meta["base_title"] + " from old site."
    site.upload(img_file, meta["base_title"], uploadmsg)
    done += 1
    print("Completed: " + str(done) + "/" + str(len(images)) + " (" + str(int((done / len(images)) * 100)) + "%)")

print("Completed!")

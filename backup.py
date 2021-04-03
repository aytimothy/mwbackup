import json
import mwclient
import os

# CONFIGURATION
url = "INSERT URL HERE"
useragent = "mwbackup/1.0"

# INITIALIZATION
site = mwclient.Site(host=url, reqs={"verify": False}, path="/", clients_useragent=useragent)

# READ DATA
pages = []
for i in range(0, 16):
    _pages = list(site.allpages(namespace=str(i)))
    for _page in _pages:
        pages.append(_page)
print("Found " + str(len(pages)) + " pages...")
images = list(site.allimages())
print("Found " + str(len(images)) + " images...")

print("Backing up pages...")
if not os.path.exists("./pages"):
    os.mkdir("./pages")
done = 0
for page in pages:
    print("Backing up: " + page.name)
    safepagedir = page.name.replace("<", "").replace(">", "").replace(":", "").replace("\"", "").replace("|", "").replace("?", "").replace("*", "").replace(" ", "_").replace("\\", "/")
    safepagename = safepagedir.replace("/", "").replace("\\", "")
    while safepagename.endswith("."):
        safepagename = safepagename[:-1]
    if not os.path.exists("./pages/" + safepagedir):
        os.mkdir("./pages/" + safepagedir)
    revs = list(page.revisions())
    revs_texts = [rev for rev in page.revisions(prop="content")]
    print("Found " + str(len(revs)) + " revisions...")
    # Clean results
    for rev in revs:
        while rev["user"].startswith("imported>"):
            rev["user"] = rev["user"][9:]
    # Actually backup
    revs_file = open("./pages/" + safepagedir + "/revs.json", "w", encoding="utf8")
    json.dump(revs, revs_file, ensure_ascii=False)
    revs_file.close()
    meta_file = open("./pages/" + safepagedir + "/meta.json", "w", encoding="utf8")
    json.dump({
        "base_name": page.base_name,
        "base_title": page.base_title,
        "contentmodel": page.contentmodel,
        "length": page.length,
        "name": page.name,
        "namespace": page.namespace,
        "page_title": page.page_title,
        "pageid": page.pageid,
        "pagelanguage": page.pagelanguage,
        "protection": page.protection,
        "redirect": page.redirect,
        "restrictiontypes": page.restrictiontypes,
        "revision": page.revision,
        "touched": page.touched
    }, meta_file, ensure_ascii=False)
    meta_file.close()
    for rev in revs:
        rev_text = list(page.revisions(rev["revid"], rev["revid"], prop="content"))[0]["*"]
        backup_file = open("./pages/" + safepagedir + "/" + str(rev["revid"]) + ".mw", "w", encoding="utf8")
        backup_file.write(rev_text)
        backup_file.close()
        print("Backing up Revision " + str(rev["revid"]))
    backup_file = open("./pages/" + safepagedir + "/latest.mw", "w", encoding="utf8")
    backup_file.write(page.text())
    backup_file.close()
    done += 1
    print("Completed: " + str(done) + "/" + str(len(pages)) + " (" + str(int((done/len(pages)) * 100)) + "%)")


print("Backing up images...")
done = 0
if not os.path.exists("./images"):
    os.mkdir("./images")
for image in images:
    safepagename = image.base_title.replace("<", "").replace(">", "").replace(":", "").replace("\"", "").replace("/", "").replace("\\", "").replace("|", "").replace("?", "").replace("*", "").replace(" ", "_")
    print("Backing up: " + image.base_title)
    if not os.path.exists("./images/" + safepagename):
        os.mkdir("./images/" + safepagename)
    img_file = open("./images/" + safepagename + "/" + safepagename, "wb")
    image.download(img_file)
    meta_file = open("./images/" + safepagename + "/meta.json", "w", encoding="utf8")
    json.dump({
        "base_name": image.base_name,
        "base_title": image.base_title,
        "contentmodel": image.contentmodel,
        "edit_time": image.edit_time,
        "exists": image.exists,
        "imageinfo": image.imageinfo,
        "imagerepository": image.imagerepository,
        "last_rev_time": image.last_rev_time,
        "length": image.length,
        "name": image.name,
        "namespace": image.namespace,
        "page_title": image.page_title,
        "pageid": image.pageid,
        "pagelanguage": image.pagelanguage,
        "protection": image.protection,
        "redirect": image.redirect,
        "restrictiontypes": image.restrictiontypes,
        "revision": image.revision,
        "touched": image.touched
    }, meta_file, ensure_ascii=False)
    meta_file.close()
    done += 1
    print("Completed: " + str(done) + "/" + str(len(images)) + " (" + str(int((done/len(images)) * 100)) + "%)")

print("Completed!")

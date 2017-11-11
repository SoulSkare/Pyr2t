import urllib2
import feedparser
from bs4 import BeautifulSoup
import json

def cleanLink(summary):
    soup = BeautifulSoup(summary, 'html.parser')
    strOut = str(soup.span.a)
    strOut = strOut.replace('<a href=', "")
    strOut = strOut.replace('"', "")
    strOut = strOut.replace('>[link]</a>', "")
    strOut = strOut.replace('amp;', '')
    return strOut

def scrapeReddit(sub):
    sub = sub
    d = feedparser.parse('http://www.reddit.com/r/' + sub + '/.rss')
    outJson = []

    for post in d.entries:
        title = post.title
        link = post.link
        summary = post.summary
        outLink = cleanLink(post.summary)

        outJson.append({"title": title, "link": link, "outLink": outLink})
    return json.dumps(outJson)

def insideTumblr(link):
    e = feedparser.parse('http://esper-bros.tumblr.com/post/156486677738/sharplmages-context/rss')
    for item in e.entries:
        print item.summary_detail.value
    return

def checkLink(link):
    # gfycat parser
    if link.find("gfycat.com") != -1:
        link = link.replace('://gfycat.com/', '://giant.gfycat.com/')
        link = link + '.gif'
        return link

    # gifv to gif
    if link[-4:] == 'gifv':
        link = link.replace('.gifv', '.gif')
        return link

    # imgur mp4 to gif
    if link.find("imgur.com") != -1 and link[-4:] == '.mp4':
        link = link.replace('.mp4', '.gif')
        return link

    # generic passthrough
    if link[-4:] == '.jpg' or link[-4:] == 'jpeg' or link[-4:] == '.png' or link[-4:] == '.gif':
        return link

    # single imgur image
    if link.find("://imgur.com") != -1 and link.find("/album/") == -1:
        link = link.replace('://imgur.com', '://i.imgur.com')
        link = link + '.jpg'
        return link

    # reddituploads passthrough
    if link.find("://i.reddituploads.com") != -1:
        return link
    else:
        return "oops"

def scrape(subName):
    subData = json.loads(scrapeReddit(subName))
    print len(subData)
    for entry in subData:
        link = entry['outLink']
        linkProc = checkLink(link)
        print "-------------------------------------------------------------------"
        print "Title: " + entry['title'] + ""
        print "Link: " + entry['link'] + ""
        print "Out Link: " + entry['outLink'] + ""
        print "Processed Link: " + linkProc + ""
        print "-------------------------------------------------------------------" + "\n"

    return subData

scrape()



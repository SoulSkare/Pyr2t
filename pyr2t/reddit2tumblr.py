import urllib2
import feedparser
from bs4 import BeautifulSoup
import json
from tumblpy import Tumblpy


class Reddit:
    def cleanLink(self, summary):
        soup = BeautifulSoup(summary, 'html.parser')
        strOut = str(soup.span.a)
        strOut = strOut.replace('<a href=', "")
        strOut = strOut.replace('"', "")
        strOut = strOut.replace('>[link]</a>', "")
        strOut = strOut.replace('amp;', '')
        return strOut

    def filter(self, sub, filter):
        f = filter
        d = ""
        if f == 'hot' or f == 'new' or f == 'hot' or f == 'rising' or f == 'controversial':
            d = feedparser.parse('http://www.reddit.com/r/' + sub + '/' + f + '/.rss')
        if f == 'topAll':
            d = feedparser.parse('http://www.reddit.com/r/' + sub + '/' + 'top/?sort=top&t=all' + '/.rss')
        if f == 'topHour':
            d = feedparser.parse('http://www.reddit.com/r/' + sub + '/' + 'top/?sort=top&t=hour' + '/.rss')
        if f == 'topDay':
            d = feedparser.parse('http://www.reddit.com/r/' + sub + '/' + 'top/?sort=top&t=day' + '/.rss')
        if f == 'topWeek':
            d = feedparser.parse('http://www.reddit.com/r/' + sub + '/' + 'top/?sort=top&t=week' + '/.rss')
        if f == 'topMonth':
            d = feedparser.parse('http://www.reddit.com/r/' + sub + '/' + 'top/?sort=top&t=month' + '/.rss')
        if f == 'topYear':
            d = feedparser.parse('http://www.reddit.com/r/' + sub + '/' + 'top/?sort=top&t=year' + '/.rss')
        if f == 'gilded':
            d = feedparser.parse('http://www.reddit.com/r/' + sub + '/' + 'top/?sort=top&t=gilded' + '/.rss')
        if f == 'promoted':
            d = feedparser.parse('http://www.reddit.com/r/' + sub + '/' + 'top/?sort=top&t=promoted' + '/.rss')
        return d

    def scrape(self, sub, filter, tumblrFormat):
        sub = sub
        filter = filter

        # filters are
        # 'hot'
        # 'new'
        # 'rising'
        # 'controversial'
        # 'topAll'
        # 'topHour'
        # 'topDay'
        # 'topWeek'
        # 'topMonth'
        # 'topYear'
        # 'gilded'
        # 'promoted

        d = self.filter(sub, filter)
        #d = feedparser.parse('http://www.reddit.com/r/' + sub + '/' + filter + '/.rss')

        dict_data = []

        if tumblrFormat == 'true':
            for post in d.entries:
                title = post.title
                link = post.link
                summary = post.summary
                outLink = self.cleanLink(summary)
                procLink = self.checkLink(self.cleanLink(summary))

                params = {
                    'type': 'photo',
                    'state': 'published',
                    'caption': title,
                    'source': procLink,
                    'data': '',
                    'tags': ''
                }
                dict_data.append(params)


        elif tumblrFormat == 'false':
            for post in d.entries:
                title = post.title
                link = post.link
                summary = post.summary
                outLink = self.cleanLink(summary)
                procLink = self.checkLink(self.cleanLink(summary))

                dict_data.append({"title": title, "link": link, "outLink": outLink, "procLink": procLink})

            json_data = json.dumps([{"post": title} for title in dict_data])


        json_data = json.dumps([{"post": title} for title in dict_data])
        return json_data


    # optimized for download
    def checkLink(self, link):
        # tumblr parser
        if link.find("tumblr.com") != -1:
            link = link + 'rss'
            e = feedparser.parse(link)
            for item in e.entries:
                link = item.summary_detail.value
                return link

        # gfycat parser
        if link.find("gfycat.com") != -1:
            #print link
            link = link.replace('://gfycat.com/', '://thumbs.gfycat.com/')
            link = link + '-mobile.mp4'
            return link

        # gifv to gif
        if link[-4:] == 'gifv':
            link = link.replace('.gifv', '.mp4')
            return link

        # imgur mp4 to gif
        if link.find("://imgur.com") != -1 and link[-4:] == '.mp4':
            #link = link.replace('.mp4', '.gif')
            return link

        # generic passthrough
        if link[-4:] == '.jpg' or link[-4:] == 'jpeg' or link[-4:] == '.png' or link[-4:] == '.gif':
            return link

        # imgur
        if link.find("://imgur.com") != -1 and link.find("/gallery/") != -1:
            return 'oops album: ' + link
        elif link.find("://imgur.com") != -1:
            # single imgur image
            link = link.replace('://imgur.com', '://i.imgur.com')
            link = link + '.jpg'
            return link

        # reddituploads passthrough
        if link.find("://i.reddituploads.com") != -1:
            link = link + '.jpg'
            return link
        else:
            return "oops: " + link


class Tumblr:
    def __init__(self, YOUR_CONSUMER_KEY, YOUR_CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET):
        self.YOUR_CONSUMER_KEY = YOUR_CONSUMER_KEY
        self.YOUR_CONSUMER_SECRET = YOUR_CONSUMER_SECRET
        self.OAUTH_TOKEN = OAUTH_TOKEN
        self.OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRET
        return


    def post(self, blog_url, params):
        # Get the final tokens from the database or wherever you have them stored
        t = Tumblpy(self.YOUR_CONSUMER_KEY, self.YOUR_CONSUMER_SECRET,
                    self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)

        # let's get the first blog url...
        blog_url = t.post('user/info')
        blog_url = blog_url['user']['blogs'][0]['url']

        post = t.post('post', blog_url=blog_url, params=params)
        return post


    # experimental
    def postJson(self, blog_url, tags, params):
        # Get the final tokens from the database or wherever you have them stored
        t = Tumblpy(self.YOUR_CONSUMER_KEY, self.YOUR_CONSUMER_SECRET,
                    self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)

        # let's get the first blog url...
        blog_url = t.post('user/info')
        blog_url = blog_url['user']['blogs'][0]['url']

        print blog_url
        dict_params = json.loads(params)

        print 'Posts length: ' + str(len(dict_params))

        for i in range(0, len(dict_params)):
            try:
                source = dict_params[i]['post']['source']
                caption = dict_params[i]['post']['caption']
                params = {
                    'type': 'photo',
                    'state': 'published',
                    'caption': caption,
                    'source': source,
                    'data': '',
                    'tags': tags + ',' + caption
                }

                post = t.post('post', blog_url=blog_url, params=params)
                raw_input("Downloading....")
            except Exception as e:
                print '------------------------------------------'
                print(e)
                print source

        return post
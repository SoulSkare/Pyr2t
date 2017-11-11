import reddit2tumblr
from pprint import pprint


YOUR_CONSUMER_KEY = ''
YOUR_CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''


reddit_sub = 'gifs'
reddit_filter = 'hot'


Reddit = reddit2tumblr.Reddit()
Tumblr = reddit2tumblr.Tumblr(YOUR_CONSUMER_KEY,
                              YOUR_CONSUMER_SECRET,
                              OAUTH_TOKEN,
                              OAUTH_TOKEN_SECRET)


def testSingle():
    params = {
        'type': 'photo',
        'state': 'published',
        'caption': '',
        'source': 'http://i.imgur.com/3RVC5vy.gif',
        'data': '',
        'tags': '!!!!!!!!!1'
    }

    #print type(params)
    print Tumblr.post('kieronwelman.tumblr.com', params)
    return


def testMulti():
    reddit_json_data = Reddit.scrape(reddit_sub, reddit_filter, tumblrFormat='true')
    print Tumblr.postJson('kieronwelman.tumblr.com', 'hello,hello2', reddit_json_data)
    return


testSingle()
#testMulti()

# TODO: callback function or wait for each post request
# TODO: test different formats for video and gifs
# TODO: try get reddit and tumblr as modules in their own directory
# TODO: make 2 different projects, on going posting and full scrape upload
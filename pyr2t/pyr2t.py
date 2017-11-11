import reddit2tumblr
import urllib
import json
import os.path
import argparse
from pprint import pprint


with open('config.json') as data_file:
    config = json.load(data_file)

pprint(config)

YOUR_CONSUMER_KEY = config["YOUR_CONSUMER_KEY"]
YOUR_CONSUMER_SECRET = config["YOUR_CONSUMER_SECRET"]
OAUTH_TOKEN = config["OAUTH_TOKEN"]
OAUTH_TOKEN_SECRET = config["OAUTH_TOKEN_SECRET"]

# # Instantiate the parser
# parser = argparse.ArgumentParser(description='Optional app description')
#
# # Required positional argument
# parser.add_argument('pos_arg', type=int,
#                     help='A required integer positional argument')
#
# # Optional positional argument
# parser.add_argument('opt_pos_arg', type=int, nargs='?',
#                     help='An optional integer positional argument')
#
# # Optional argument
# parser.add_argument('--opt_arg', type=int,
#                     help='An optional integer argument')
#
# # Switch
# parser.add_argument('--switch', action='store_true',
#                     help='A boolean switch')
#
# args = parser.parse_args()
#
# print("Argument values:")
# print(args.pos_arg)
# print(args.opt_pos_arg)
# print(args.opt_arg)
# print(args.switch)


# Filters are
# 'hot'
# 'new'
# 'rising'
# 'controversial'
# 'topAll'# 'topHour'# 'topDay'# 'topWeek'# 'topMonth'# 'topYear'
# 'gilded'
# 'promoted


def get(url, file=None, encoding='utf-8'):
    result = ""
    url = url.encode(encoding)
    try:
        if file == None :
            f = urllib.urlopen(url)
            for line in f.readlines():
                result += line
        else:
            result = urllib.urlretrieve(url, file)
            result = result[0]
    except IOError:
        pass
    return result


def dosinglething():
    f = get('https://78.media.tumblr.com/3159ea38accf211e20a549ce9cb8071c/tumblr_oqzpo5j1Nr1qh588ko1_500.png', 'test.jpg')
    data = open(f)
    params = {
        'type': 'photo',
        'state': 'published',
        'caption': '',
        'source': '',
        'data': data,
        'tags': '!!!!!!!!!1'
    }

    # print type(params)
    print Tumblr.post(config["tumblr_name"] + ".tumblr.com", params)
    return


def dothethings(reddit_sub, reddit_filter, temp_folder):
    reddit_json_data = Reddit.scrape(reddit_sub, reddit_filter, tumblrFormat='true')
    reddit_dict_params = json.loads(reddit_json_data)
    temp_sub_full = temp_folder + reddit_sub + '/'

    try:
        os.makedirs(temp_sub_full)
    except OSError:
        if not os.path.isdir(temp_sub_full):
            raise

    for i in range(0, len(reddit_dict_params)):
        try:
            source = reddit_dict_params[i]['post']['source']
            caption = reddit_dict_params[i]['post']['caption']

            pieces = source.split("/")
            length = len(pieces)
            filename = pieces[length - 1:length][0]
            ext = os.path.splitext(filename)[1]
            type = ''

            if os.path.exists(temp_sub_full + filename):
                print 'Skipping ' + filename + ' - Already exists'
                print '------------------------------------------'
                continue

            if ext == '.mp4' or ext == '.webm':
                type = 'video'

            if ext == '.jpg' or ext == '.jpeg' or ext == '.png' or ext == '.gif':
                type = 'photo'

            print 'Downloading: ' + source
            f = get(source, temp_sub_full + filename)
            data = open(f)

            params = {
                'type': type,
                'state': config["state"],
                'caption': caption,
                'source': '',
                'data': data,
                'tags': config["tags"] + ", " + caption
            }

            out = Tumblr.post(config["tumblr_name"] + ".tumblr.com", params)
            print 'Post: ' + temp_sub_full + filename
            print out
            print '------------------------------------------'
        except Exception as e:
            print(e)
            print source
            print '------------------------------------------'
    return

# =================================================================================

Reddit = reddit2tumblr.Reddit()
Tumblr = reddit2tumblr.Tumblr(config["YOUR_CONSUMER_KEY"], config["YOUR_CONSUMER_SECRET"], config["OAUTH_TOKEN"], config["OAUTH_TOKEN_SECRET"])
#Tumblr = reddit2tumblr.Tumblr("", "", "", "")


#dothethings(reddit_sub=config["reddit_sub"], reddit_filter=config["reddit_filter"], temp_folder=config["temp_folder"])
#dothethings(reddit_sub='gifs', reddit_filter='hot', temp_folder='./temp/')

dosinglething()


# TODO: cross folder/database checking if posted already (filename check)
# TODO: fix imgur.com/a/ album scrape
# TODO: scrape 500px NOTE: easyish
# <img class="photo" src="https://drscdn.500px.org/photo/198112363/q%3D80_m%3D1500_k%3D1/c6931ca5244e1b0884e5de2b2557f8d7" alt="Deep Sky Objects by Tehmina Beg on 500px" style="display: inline; margin-top: 0px; width: auto; height: auto;">
# TODO: fix filter for top - NOTE: PROBLEM WITH TOP
# TODO: add database - check database if the post has been made before
# TODO: detect file size before downloading because ram
# TODO: try get reddit and tumblr as modules in their own directory

# TODO: each sub in its own folder in temp - DONE
# TODO: test different formats for video and gifs - DONE
# TODO: make 2 different projects, on going posting and full scrape upload - DONE

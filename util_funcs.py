from   tqdm         import tqdm
from   rich.console import Console
from   rich         import inspect
from   pygal.style  import NeonStyle, Style
import requests     as     rq
import pygal

from   datetime     import datetime
import json



# ------------------------------------------------------------ PARSING REDDIT POSTS ------------------------------------------------------------


def parse_image_post(post_data:dict):
    return {
            post_data['id']: {
                'created_utc':  post_data['created_utc'],
                'domain':       post_data['domain'],
                'filename':     post_data['url'].split('/')[-1],
                'media_url':    post_data['url'],
                'op':           post_data['author'],
                'post_id':      post_data['id'],
                'post_url':     f'https://reddit.com{post_data["permalink"]}',
                'score':        post_data['score'],
                'subreddit':    post_data['subreddit'],
                'title':        post_data['title'],
                'type':         'image',
                'extension':    post_data['url'].split('/')[-1].split(".")[-1].split('?')[0],    # after spliting url, result can be like filename.jpg?vbnojh76
            }
        }


def parse_video_post(post_data:dict):
    filename = post_data['url'].split('/')[-1]  # This returns filename aka ID without the extension
    return { 
            post_data['id']: {
                'created_utc':  post_data['created_utc'],
                'domain':       post_data['domain'],
                'filename':     f'{filename}.mpd',
                'media_url':    f'https://v.redd.it/{filename}/DASHPlaylist.mpd',
                'op':           post_data['author'],
                'post_id':      post_data['id'],
                'post_url':     f'https://reddit.com{post_data["permalink"]}',
                'score':        post_data['score'],
                'subreddit':    post_data['subreddit'],
                'title':        post_data['title'],
                'type':         'video',
                'extension':    'mpd',
            }
        }


def parse_gallery_post(post_data:dict, image_url:str):
    ret     = {}
    post_id = post_data['id']

    images = post_data['media_metadata']  # This returns a dictionary which contains filenames (without ext) as keys
    if not images:    return {}           # Sometimes `images` can be "null", god knows why, here is a post like that: https://reddit.com/r/CatsWhoYawn/comments/z4rllw/beeper_yawns_still_hungover_from_tryptophan_ig/

    for img in images.keys():
        ext = post_data['media_metadata'][img]['m'].split('image/')[-1]
        ret[f'{post_id}+{img}'] = {
            'created_utc':  post_data['created_utc'],
            'domain':       post_data['domain'],
            'filename':     f'{img}.{ext}',
            'media_url':    image_url.format(filename=f'{img}.{ext}'),
            'op':           post_data['author'],
            'post_id':      post_id,
            'post_url':     f'https://reddit.com{post_data["permalink"]}',
            'score':        post_data['score'],
            'subreddit':    post_data['subreddit'],
            'title':        post_data['title'],
            'type':         'image',
            'extension':    ext,   # Its always jpg (Narrator: That wasnt the case, like here: https://www.reddit.com/r/blurrypicturesofcats/comments/10ane0m/blurry_picture_of_a_cat/)
        }

    return ret






# ------------------------------------------------------------ GENERATING CHARTS ------------------------------------------------------------



def upvote_chart(raw_data, style:Style):
    # Initialises chart
    chart = pygal.Bar(human_readable=True, style=style, show_legend=False)
    chart.title = 'Distribution of upvotes per subreddit'
    chart.value_formatter = lambda x: f'{x:,}'
    data = {}

    # Parses the raw data
    for dic in raw_data:
        sub       = dic['subreddit']
        score     = dic['score']
        if not sub in data.keys():    data[sub] = 0
        data[sub] += score

    # Adds the parsed data into the chart
    data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
    for key in data.keys():
        chart.add(key, data[key])

    # data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
    # for n, key in enumerate(data.keys()):
    #     chart.add(n+1, data[key])
    
    chart.render_to_file('docs/stats/charts/1-upvotes.svg') 
    return data 


def extension_chart(raw_data, style:Style):
    # Initialises chart
    chart = pygal.Pie(human_readable=True, style=style)
    chart.title = 'Distribution of extensions'
    data = {}

    # Parses the raw data
    for dic in raw_data:
        ext = dic['extension']
        if not ext in data.keys():    data[ext] = 0
        data[ext] += 1

    # Adds the parsed data into the chart
    for key in data.keys():
        chart.add(key, data[key])
    
    chart.render_to_file('docs/stats/charts/2-extensions.svg')
    return data 


def domain_chart(raw_data, style:Style):
    # Initialises chart
    chart = pygal.Pie(human_readable=True, style=style)
    chart.title = 'Distribution of domains'
    data = {}

    # Parses the raw data
    for dic in raw_data:
        domain = dic['domain']
        if not domain in data.keys():    data[domain] = 0
        data[domain] += 1

    # Adds the parsed data into the chart
    for key in data.keys():
        chart.add(key, data[key])
    
    chart.render_to_file('docs/stats/charts/3-domains.svg')  
    return data 


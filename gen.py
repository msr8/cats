from   tqdm         import tqdm
from   rich.console import Console
from   rich         import inspect
from   pygal.style  import NeonStyle
import requests     as     rq
import pygal

from   datetime     import datetime as dt
import json

NeonStyle.transition = '0.3s ease-out'
NeonStyle.colors = (
    '#ff5995',
    '#b6e354',
    '#feed6c',
    '#8cedff',
    '#9e6ffe',
    '#899ca1',
    '#f8f8f2',
    '#bf4646',
    # '#516083',
    '#f92672',
    '#82b414',
    '#fd971f',
    '#56c2d6',
    '#808384',
    '#8c54fe',
    # '#465457'
)
# NeonStyle.plot_background = 'rgba(1,1,1,0.5)'
# NeonStyle.plot_background = '#111'
NeonStyle.background = 'rgba(0,0,0,0)'
# NeonStyle.value_background = 'rgba(0,255,0,1)'

NeonStyle.foreground        = 'rgba(200, 200, 200, 1)'
NeonStyle.foreground_strong = 'rgba(255, 255, 255, 1)'
# NeonStyle.foreground_subtle = 'rgba(0,0,255,1)'








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



def upvote_chart(raw_data):
    # Initialises chart
    chart = pygal.Bar(human_readable=True, style=NeonStyle, show_legend=False)
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


def extension_chart(raw_data):
    # Initialises chart
    chart = pygal.Pie(human_readable=True, style=NeonStyle)
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


def domain_chart(raw_data):
    # Initialises chart
    chart = pygal.Pie(human_readable=True, style=NeonStyle)
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













def gen_files_json():
    # So that previous posts are preserved
    with open('docs/files.json') as f:
        raw_data = json.load(f)['data']

    pbar = tqdm(leave=True, colour=COLOR, total=len(SUBREDDITS))
    for sub in SUBREDDITS:
        # printf(f'[b GREEN1][JSON][/]  {n+1}/{len(SUBREDDITS)}) {sub}')
        pbar.set_description(sub)
        url      = URL.format(subreddit=sub)
        r        = rq.get(url, headers=HEADERS)
        sub_data = r.json()
        posts    = sub_data['data']['children'] # This returns a list of posts (dictionaries)

        for post in posts:
            post_data = post['data']

            # Checks if its a crosspost
            if post_data.get('crosspost_parent_list'):
                continue

            # Checks if its a gallery
            if post_data.get('is_gallery'):
                dics = parse_gallery_post(post_data, IMAGE_URL)
                raw_data.update(dics)
                continue

            # Checks if its a video
            if post_data.get('is_video'):
                dic = parse_video_post(post_data)
                raw_data.update(dic)
                continue

            # Checks if its an image
            if post_data.get('post_hint') == 'image':    # Used .get() because images removed by REDDIT dont have a post_hint attribute, like https://www.reddit.com/r/Kitten/comments/tnilow/baby_kitten_summer_adventures/
                dic = parse_image_post(post_data)
                raw_data.update(dic)
        pbar.update()
    pbar.close()

    
    ts = dt.utcnow()
    to_dump = {
        'total':                      len(raw_data),
        'last_updated_utc':           int(ts.timestamp()),
        'last_updated_utc_readable':  ts.strftime('%Y-%m-%d %H:%M:%S'),
        'data':                       raw_data,
    }

    to_dump_min = {}
    for fid in to_dump['data']:
        to_dump_min[fid]      = {}
        to_dump_min[fid]['t'] = to_dump['data'][fid]['type']
        to_dump_min[fid]['f'] = to_dump['data'][fid]['filename']
        to_dump_min[fid]['p'] = to_dump['data'][fid]['post_url']
        to_dump_min[fid]['m'] = to_dump['data'][fid]['media_url']

    with open('docs/files.json', 'w') as f:
        json.dump(to_dump,     f, indent=4)
    with open('docs/files.min.json', 'w') as f:
        json.dump(to_dump_min, f)


    # with open('testing/test10.json', 'w') as f:
    #     json.dump(to_write, f, indent=4)



def gen_stats():
    # Gets the raw data
    with open('docs/files.json') as f:
        raw_data      = json.load(f)['data'].values()
    # Generates the charts
    data = {}
    data['upvotes']    = upvote_chart(raw_data)
    data['extensions'] = extension_chart(raw_data) 
    data['domains']    = domain_chart(raw_data)
    # Writes it to processed_data.json
    with open('docs/stats/processed_data.json', 'w') as f:
        json.dump(data, f, indent=4)



def gen_subs_md():
    # Initialises text
    text =  '|   | Subreddit | Description | Members |\n'
    text += '| - | --------- | ----------- | ------- |\n'

    # Gets all the data
    pbar = tqdm(leave=True, colour=COLOR, total=len(SUBREDDITS))
    for n, sub in enumerate(SUBREDDITS):
        # printf(f'[b GREEN3][MARKDOWN][/]  {n+1}/{len(SUBREDDITS)}) {sub}')
        pbar.set_description(sub)

        r        = rq.get(f'https://www.reddit.com/r/{sub}/about.json', headers=HEADERS)
        sub_data = r.json()['data']
        name     = sub_data['display_name_prefixed']
        about    = '-' if not sub_data['public_description'] else sub_data['public_description'].splitlines()[0]    # Incase the about is empty
        members  = sub_data['subscribers']

        text    += f'| {n+1} | [{name}](https://reddit.com/r/{sub}) | {about} | {members:,} |\n'
        pbar.update()
    pbar.close()

    # Writes it
    with open('subreddits.md', 'w') as f:
        f.write(text)













URL        = 'https://www.reddit.com/r/{subreddit}/top/.json?limit=100&t=year'
IMAGE_URL  = 'https://i.redd.it/{filename}' # i is for images, v is for videos
HEADERS    = {'User-Agent': 'https://github.com/msr8/cats'}
COLOR      = '#696969'
SUBREDDITS =  [
    'activationsound',
    'airplaneears',
    'blurrypicturesofcats',
    'catculations',
    'catfaceplant',
    'cathostage',
    'catloaf',
    'catpics',
    'catpictures',
    'cats',
    'catsarealiens',
    'catsarealiens',
    'catsareassholes',
    'catsareliquid',
    'catsbeingbanks',
    'catsbeingcats',
    'catsinsinks',
    'catsmirin',
    'catsoncats',
    'catsonkeyboards',
    'catsridingroombas',
    'catsstandingup',
    'catsvstechnology',
    'catswhosmoke',
    'catswhosqueak',
    'catswhoyawn',
    'catswhoyell',
    'catswithjobs',
    'catswithsocks',
    'curledfeetsies',
    'cuteguyswithcats',
    'drillcats',
    'floof',
    'gingerkitty',
    'holdmycatnip',
    'ififitsisits',
    'illegallysmolcats',
    'kitten',
    'legalcatadvice',
    'meow_irl',
    'meowow',
    'miscatculations',
    'motorboat',
    'murdermittens',
    'myhatisacat',
    'nebelung',
    'nervysquervies',
    'noodlebones',
    'notmycat',
    'oneorangebraincell',
    'petthedamncat',
    'petthedamncat',
    'pointytailedkittens',
    'politecats',
    'pottedcats',
    'purrkour',
    'sadcats',
    'shouldercats',
    'siamesecats',
    'standardissuecat',
    'startledcats',
    'stuffoncats',
    'supermodelcats',
    'thecatdimension',
    'thecattrapisworking',
    'thisismylifemeow',
    'turkishcats',
    'whatswrongwithyourcat',
    'whiskerfireworks',
]



if __name__ == '__main__':
    try:
        console = Console()
        
        gen_files_json()
        gen_stats()
        gen_subs_md()
    except Exception as e:
        console.print_exception()


    # HEADERS    = {'User-Agent': 'your_user_agent'}
    # url = 'https://www.reddit.com/r/kitten/top/.json?limit=100&t=year'

    # r        = rq.get(url, headers=HEADERS)
    # to_write = r.json()
    # with open('testing/test9.json', 'w') as f:
    #     json.dump(to_write, f, indent=4)





'''
REMEMBER, GALLERY POSTS DONT HAVE "post_hint"

test.json:    ALL
test2.json:   Having the "is_gallery" attribute
test3.json:   Not having the "i.redd.it" domain
test4.json:   The post_data of all images and non-galleries
test5.json:   The needed data of all images (including galleries) scraped from one sub
test6.json:   The needed data of all images and videos scraped from one sub
test7.json:   The needed data of all images and videos scraped from different subs
test8.json:   ALL the data of r/catswhoyawn, because that subreddit was giving me an error 
test9.json:   ALL the data of r/kitten,      because that subreddit was giving me an error 
test10.json:  ALL the data of all posts having the "is_gallery" attribute




TO-DO

-> add /library
-> minify dash-js
-> minify files.json (make a files.min.json or smth)








CustomStyle = Style(
    background='black',
    ci_colors=(),
    colors=('#ff5995', '#b6e354', '#feed6c', '#8cedff', '#9e6ffe', '#899ca1', '#f8f8f2', '#bf4646', '#516083', '#f92672', '#82b414', '#fd971f', '#56c2d6', '#808384', '#8c54fe', '#465457'),
    dot_opacity='1',
    font_family='Consolas, "Liberation Mono", Menlo, Courier, monospace',
    foreground='#999',
    foreground_strong='#eee',
    foreground_subtle='#555',
    guide_stroke_color='black',
    guide_stroke_dasharray='4,4',
    label_font_family=None,
    label_font_size=10,
    legend_font_family=None,
    legend_font_size=14,
    major_guide_stroke_color='black',
    major_guide_stroke_dasharray='6,6',
    major_label_font_family=None,
    major_label_font_size=10,
    no_data_font_family=None,
    no_data_font_size=64,
    opacity='.1',
    opacity_hover='.75',
    plot_background='#111',
    stroke_opacity='.8',
    stroke_opacity_hover='.9',
    stroke_width='1',
    stroke_width_hover='4',
    title_font_family=None,
    title_font_size=16,
    tooltip_font_family=None,
    tooltip_font_size=14,
    transition='0.5s ease-out',
    value_background='rgba(229, 229, 229, 1)',
    value_colors=(),
    value_font_family=None,
    value_font_size=16,
    value_label_font_family=None,
    value_label_font_size=10
)

.ok {
    background-color: #ff5995;
    background-color: #b6e354;
    background-color: #feed6c;
    background-color: #8cedff;
    background-color: #9e6ffe;
    background-color: #899ca1;
    background-color: #f8f8f2;
    background-color: #bf4646;
    background-color: #516083;
    background-color: #f92672;
    background-color: #82b414;
    background-color: #fd971f;
    background-color: #56c2d6;
    background-color: #808384;
    background-color: #8c54fe;
    background-color: #465457;
}

'''



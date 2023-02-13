from   tqdm         import tqdm
from   rich.console import Console
from   rich         import print as printf
import requests     as     rq

import json



def parse_image_post(post_data:dict):
    return {
            'created_utc':  post_data['created_utc'],
            'domain':       post_data['domain'],
            'filename':     post_data['url'].split('/')[-1],
            'media_url':    post_data['url'],
            'op':           post_data['author'],
            'post_url':     f'https://reddit.com{post_data["permalink"]}',
            'score':        post_data['score'],
            'subreddit':    post_data['subreddit'],
            'title':        post_data['title'],
            'type':         'image',
            'extension':    post_data['url'].split('/')[-1].split(".")[-1],
        }



def parse_video_post(post_data:dict):
    filename = post_data['url'].split('/')[-1]  # This returns filename aka ID without the extension
    return {
            'created_utc':  post_data['created_utc'],
            'domain':       post_data['domain'],
            'filename':     f'{filename}.mpd',
            'media_url':    f'https://v.redd.it/{filename}/DASHPlaylist.mpd',
            'op':           post_data['author'],
            'post_url':     f'https://reddit.com{post_data["permalink"]}',
            'score':        post_data['score'],
            'subreddit':    post_data['subreddit'],
            'title':        post_data['title'],
            'type':         'video',
            'extension':    'mpd',
        }



def parse_gallery_post(post_data:dict, image_url:str):
    ret = []

    images = post_data['media_metadata']  # This returns a dictionary which contains filenames (without ext) as keys
    if not images:                        # Sometimes `images` can be "null", god knows why, here is a post like that: https://reddit.com/r/CatsWhoYawn/comments/z4rllw/beeper_yawns_still_hungover_from_tryptophan_ig/
        return []
    for img in images.keys():
        ret.append({
            'created_utc':  post_data['created_utc'],
            'domain':       post_data['domain'],
            'filename':     f'{img}.jpg',
            'media_url':    image_url.format(filename=f'{img}.jpg'),
            'op':           post_data['author'],
            'post_url':     f'https://reddit.com{post_data["permalink"]}',
            'score':        post_data['score'],
            'subreddit':    post_data['subreddit'],
            'title':        post_data['title'],
            'type':         'image',
            'extension':    'jpg',   # Its always jpg (Narrator: That wasnt the case, like here: https://www.reddit.com/r/blurrypicturesofcats/comments/10ane0m/blurry_picture_of_a_cat/)
        })

    return ret





def main():
    URL        = 'https://www.reddit.com/r/{subreddit}/top/.json?limit=100&t=year'
    IMAGE_URL  = 'https://i.redd.it/{filename}' # i is for images, v is for videos
    HEADERS    = {'User-Agent': 'https://github.com/msr8/cats'}
    SUBREDDITS =  [
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
        'holdmycatnip',
        'illegallysmolcats',
        'kitten',
        'legalcatadvice',
        'meow_irl',
        'meowow',
        'miscatculations',
        'motorboat',
        'murdermittens',
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
        'sadcats',
        'shouldercats',
        'siamesecats',
        'standardissuecat',
        'startledcats',
        'startledcats',
        'stuffoncats',
        'supermodelcats',
        'thecatdimension',
        'thecattrapisworking',
        'thisismylifemeow',
        'turkishcats',
        'whatswrongwithyourcat'
    ]
    to_write = []


    for num, sub in enumerate(SUBREDDITS):
        print(f'{num+1}/{len(SUBREDDITS)}: {sub}')
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
                to_write.extend(dics)
                continue

            # Checks if its a video
            if post_data.get('is_video'):
                dic = parse_video_post(post_data)
                to_write.append(dic)
                continue

            # Checks if its an image
            if post_data.get('post_hint') == 'image':    # Used .get() because images removed by REDDIT dont have a post_hint attribute, like https://www.reddit.com/r/Kitten/comments/tnilow/baby_kitten_summer_adventures/
                dic = parse_image_post(post_data)
                to_write.append(dic)


        with open('docs/files.json', 'w') as f:
            json.dump(to_write, f, indent=4)










if __name__ == '__main__':
    try:
        console = Console()
        main()
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

test.json:   ALL
test2.json:  Having the "is_gallery" attribute
test3.json:  Not having the "i.redd.it" domain
test4.json:  The post_data of all images and non-galleries
test5.json:  The needed data of all images (including galleries) scraped from one sub
test6.json:  The needed data of all images and videos scraped from one sub
test7.json:  The needed data of all images and videos scraped from different subs
test8.json:  ALL the data of r/catswhoyawn, because that subreddit was giving me an error 
test9.json:  ALL the data of r/kitten,      because that subreddit was giving me an error 





TO-DO

-> Fix ext issue in parse_gallery_post()
-> add stats.html
-> add /
-> Add sub arg in js
-> Check TOR req

'''



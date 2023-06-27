import requests as rq
from tqdm import tqdm

import os
import json
from concurrent.futures import ThreadPoolExecutor

config = {
    'dir': '/Users/mark/Pictures/Reddit Downloads'
}

with open('docs/files.json') as f:
    files: dict = json.load(f)['data']
pbar = tqdm(total=len(files), leave=False, colour='#696969')




class File:
    def __init__(self, info: dict):
        self.url      = info['media_url']
        self.type     = info['type']
        self.filename = info['filename']
        # If its a video, change the url
        if self.type=='video':
            a             = self.filename[:-4]
            self.url      = f'https://sd.redditsave.com/download.php?permalink=https://reddit.com/&video_url=https://v.redd.it/{a}/DASH_1080.mp4?source=fallback&audio_url=https://v.redd.it/{a}/DASH_audio.mp4?source=fallback'
            self.filename = f'{a}.mp4'

    def download(self, dir: str):
        # print(self.url)
        fp = os.path.join(dir, self.filename)
        with open(fp, 'wb') as f:
            f.write(rq.get(self.url).content)


def download_file(file:File, dir):
    global pbar
    file.download(dir)
    pbar.update()




dir = config['dir']
os.makedirs(dir, exist_ok=True)


# Create a ThreadPoolExecutor with a specified number of workers
with ThreadPoolExecutor(max_workers=100) as executor:
    # Submit each file download as a separate task to the executor
    futures = []
    for i in files.values():
        future = executor.submit(download_file, File(i), dir)
        futures.append(future)



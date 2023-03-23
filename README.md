msr8.github.io/cats

This is a minimal site for showing various cat pictures/videos people have posted on reddit and which members have upvoted. How it works is basically I have a python script [gen.py](https://github.com/msr8/cats/blob/main/gen.py) that scrapes various cat posts in [these](https://github.com/msr8/cats/blob/main/subreddits.md) cat subreddits, and store all the data in a file called [files.json](https://github.com/msr8/cats/blob/main/docs/files.json). This contains information about the post ID, link to the post, number of upvotes, username of OP, etc. Then in [/random](msr8.github.io/cats/random), [script.js](https://github.com/msr8/cats/blob/main/docs/random/script.json) chooses random image/video from the scraped data and displays it on the page. The various endpoints available are:

<br>

## /

## /random

## /stats

## /files.json

## /files.min.json
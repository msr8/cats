<!-- <html>

<style>
    #button {
        font-size: 2.5em;
        color: #fca311;
        background-color: #24252a;
        text-align: center;
        padding: 0.4em;
        text-decoration: none;

        font-family: 'Comfortaa';
        font-weight: 700;
        letter-spacing: 0.09em;

        border-radius: 13px;
        border-width: 3px;
        border-style: solid;
        border-top-color:    rgb(229, 229, 229);
        border-left-color:   rgb(229, 229, 229);
        border-right-color:  rgb(105, 105, 105);
        border-bottom-color: rgb(105, 105, 105);
        transition: 0.5s;
    }
</style>

<center>
    <div id="button">
        Random Cat
    </div>
</center>

</html> -->


<!-- <div align="center">
    <img src="button.svg">
</div> -->

<div align='center'>
    [ ![img](button.svg) ](https://msr8.github.io/cats)
</div>

<br><br><br><br>

This is the source code of a simple [site](https://msr8.github.io/cats) for showing various cat pictures/videos people have posted on reddit and which members have upvoted. How it works is basically I have a python script [gen.py](https://github.com/msr8/cats/blob/main/gen.py) that scrapes various cat posts in [these](https://github.com/msr8/cats/blob/main/subreddits.md) cat subreddits, and stores all the data in a JSON file called [files.json](https://github.com/msr8/cats/blob/main/docs/files.json). This contains information about the post ID, link to the post, number of upvotes, username of OP, etc. Then in [/random](msr8.github.io/cats/random), [script.js](https://github.com/msr8/cats/blob/main/docs/random/script.json) chooses a random image/video from the scraped data and displays it on the page. The various endpoints available are:

<br>

## /
Homepage. Contains an inroduction to the site as well as links to other resources/webpages

## /random
The main highlight of the site, shows a random cat image/video upon visiting/reloading the page

## /stats
Contains various statistics about the scraped data (such as distribution of upvotes and domains) in the form of interactive graphs

## /files.json
Contains all the scraped data in a human readable JSON format

## /files.min.json
Contains the scraped data in a minified way, and is almost 4x as small as files.json
function get_url_args() {
    var params = {};
    var search = window.location.search;
    if (search) {
        search = search.substring(1);
        var parts = search.split("&");
        for (var i = 0; i < parts.length; i++) {
            var pair = parts[i].split("=");
            params[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1]);
        }
    }
    return params;
}



function process_args() {
    let args = get_url_args();
    console.log(args);

    let my_args = {};

    // TYPE
    my_args.type = 'any';
    if (args.type != undefined) {
        if      (args.type.toLowerCase() == 'image')    {my_args.type='i';}
        else if (args.type.toLowerCase() == 'video')    {my_args.type='v';}
    }

    // SUBREDDIT
    my_args.sub = 'any';

    return my_args;
}


function change_content(div_content) {
    const mediabox     = document.getElementById('mediabox');
    mediabox.innerHTML = div_content;
}


function get_rand_key(dict) {
    keys     = Object.keys(dict);
    rand_key = keys[ Math.floor(Math.random() * keys.length) ];
    return rand_key;
}




function process_files(files, args) {
    let div_content;
    let file_data = {};
    let key;

    do {
        key       = get_rand_key(files);
        file_data = files[key];
    }
    while ( args.type!='any' && args.type!=file_data.t );

    console.log(file_data);
    document.title = key;

    // Checks if its an image
    if (file_data.t == 'i') {
        div_content = IMG_DATA;
        div_content = div_content.replace('{{post_url}}',  file_data.p);
        div_content = div_content.replace('{{media_url}}', file_data.m);
    }
    // Else, also loads dash.js
    else {
        div_content  = VID_DATA;
        div_content  = div_content.replace('{{media_url}}', file_data.m);
        const script = document.createElement('script');
        script.src   = 'https://cdn.dashjs.org/latest/dash.all.min.js';
        document.head.appendChild(script);
    }

    // Adds the img/vid to the page
    change_content(div_content);
}




function main() {
    let my_args = process_args();
    console.log(my_args);

    // Need to do this because the div_content can only be changed when DOM and files.json has loaded
    window.onload = function() {
        fetch('../files.min.json')
            .then(response => response.json())
            .then(data => {
                process_files(data, my_args);
            });
    };
}



const IMG_DATA = '<a href="{{post_url}}" target="_blank">  <img class="center-fit" src="{{media_url}}">  </a>';
const VID_DATA = '<video data-dashjs-player autoplay src="{{media_url}}" controls>  </video>';
main();
// window.onload = main;




// Reminder of whats logged:
// 1) args
// 2) my_args
// 3) file_data

// File attributes being used:
// .type
// .post_url
// .media_url

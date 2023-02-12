

function change_content(div_content) {
    console.log(div_content);
    const mediabox     = document.getElementById('mediabox');
    mediabox.innerHTML = div_content;
}


function rand(arr) {
    return arr[ Math.floor(Math.random() * arr.length) ]
}


function process_files(files) {
    const IMG_DATA = '<img class="center-fit" src="{{url}}">';
    const VID_DATA = '<video data-dashjs-player autoplay src="{{url}}" controls>  </video>';
    let   div_content;

    let file_data = rand(files);
    console.log(file_data);

    // Checks if its an image
    if (file_data.type == 'image') {
        div_content = IMG_DATA.replace('{{url}}', file_data.media_url);
    }
    else {
        div_content = VID_DATA.replace('{{url}}', file_data.media_url);
    }

    change_content(div_content);
    if (file_data.type != 'image') {
        const script = document.createElement('script');
        script.src = 'dash-4.5.2.js';
        document.head.appendChild(script);
    }
}




function main() {
    fetch('../files.json')
        .then(response => response.json())
        .then(data => {
            process_files(data);
        });
}




window.onload = main;


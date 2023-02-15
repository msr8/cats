function change_content(content) {
    let pre       = document.getElementById('raw_data');
    pre.innerHTML = content;
}


function main() {
    // Need to do this because the content can only be changed when DOM and processed_data.json has loaded
    window.onload = function() {
        fetch('processed_data.json')
            .then(response => response.text())
            .then(data => {
                change_content(data);
            });
    };
}



main();
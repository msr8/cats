function change_content(content) {
    let pre       = document.getElementById('raw_data');
    pre.innerHTML = content;
}


function main() {
    fetch('processed_data.json')
        .then(response => response.text())
        .then(data => {
            change_content(data);
        });
}



main();
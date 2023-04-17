function process_files(files_info, args) {
    const span_files = document.getElementById('span_files');
    const span_subs  = document.getElementById('span_subs');

    console.log(files_info);

    span_files.textContent = files_info.total_files;
    span_subs.textContent  = files_info.total_subreddits;
}





function main() {
    // Need to do this because the div_content can only be changed when DOM and files.json has loaded
    window.onload = function() {
        fetch('files_info.json')
            .then(response => response.json())
            .then(data => {
                process_files(data);
            });
    };
}


main();


function toggleAdvancedSettings() {
    if (document.getElementById("advanced-settings-toggler").checked) {
        document.querySelector(".advanced-settings").style.display = "block";
    } else {
        document.querySelector(".advanced-settings").style.display = "none";
    }
}

function showProgressBar() {
    document.querySelector(".progress").style.display = "flex";
    // Animation duration of progress bar (0 to 100%) is set to the filesize divided by 2,000 in ms
    document.querySelector(".progress-bar").style.animationDuration =
        document.getElementById('formFile').files[0].size / 2000 + "ms";
}

function copyToClipboard() {
    const copyText = document.querySelector(".result-text").innerHTML;
    navigator.clipboard.writeText(copyText).then(() => {
        // Alert the user that the action took place.
        alert("Copied to clipboard");
    });
}

function downloadFile(elem) {
    const text = document.getElementById("result-text").innerHTML;
    elem.setAttribute("href", "data:text/plain;charset=utf-8," + encodeURIComponent(text));
}

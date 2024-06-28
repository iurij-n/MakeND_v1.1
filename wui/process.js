var admittingParent = document.querySelector('p#progress_bar');

eel.expose(progress_bar);
function progress_bar(progress_bar_value) {
    document.getElementById('progress_bar').innerHTML = progress_bar_value
}
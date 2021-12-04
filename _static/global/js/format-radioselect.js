function format_radioSelect() {
    // find dom elements of class "controls"
    controls = document.getElementsByClassName('controls');
    for (c of controls) {
        for (label of c.getElementsByTagName('label')) {
            // set inner html as inner text for all labels
            label.innerHTML = label.innerText;
        }
    }
}

format_radioSelect();

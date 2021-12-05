function format(li) {
    // need to move input tag out of ul
    label = li.getElementsByTagName('label')[0];
    li.appendChild(label.getElementsByTagName('input')[0]);
    li.appendChild(label);
    // set inner html of label as inner text, so tags are processed
    label.innerHTML = label.innerText;
}



function format_radioSelect() {
    // find dom elements of class "controls"
    controls = document.getElementsByClassName('controls');
    for (c of controls) {
        for (li of c.getElementsByTagName('li')) {
            // set inner html as inner text for all labels
            format(li);
        }
    }
}

format_radioSelect();

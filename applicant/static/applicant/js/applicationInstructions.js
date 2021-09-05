// check if understanding question already answered and zoom to it if wrong
let buttons = document.getElementById('id_understanding3').getElementsByClassName('form-check-input');
let checked = false;
for (let i = 0; i < buttons.length; i++) {
    if (buttons[i].checked) {
        checked = true;
        break;
    }
}
if (checked) {
    show('page3', 'page1');
}

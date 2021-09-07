// check if understanding question already answered and zoom to it if wrong
function checkUnderstanding(form_id, show_id, hide_id) {
    let buttons = document.getElementById(form_id).getElementsByClassName('form-check-input');
    let checked = false;
    for (let i = 0; i < buttons.length; i++) {
        if (buttons[i].checked) {
            checked = true;
            break;
        }
    }
    if (checked) {
        show(show_id, hide_id);
    }
}

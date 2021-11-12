const agree = document.getElementById('agree');
const rangeInput = document.getElementById('rangeInput');
const amount = document.getElementById('amount');


function updateAgreeResponse() {
    agree.value = rangeInput.value;
    amount.innerHTML = rangeInput.value;
}

function checkAgreeForAnswer() {
    if (amount.innerHTML == '--') {
        document.getElementById('not-complete-error2').style.display = 'block';
        return false;
    }
    else {
        document.getElementById('not-complete-error2').style.display = 'none';
        return true;
    }
}

function checkForAnswer(form_id) {
    let form = document.getElementById(form_id);
    let buttons = form.getElementsByClassName('form-check-input');
    let checked = false;
    for (i = 0; i < buttons.length; i++) {
      if (buttons[i].checked) {
        checked = true;
        break;
      }
    }
    let nce_id = 'not-complete-error' + (form_id == 'id_self_eval' ? '1' : '3');
    if (!checked) {
        document.getElementById(nce_id).style.display = 'block';
        return false;
    }
    else {
        document.getElementById(nce_id).style.display = 'none';
        return true;
    }
}

function seeProfile() {
  if (checkForAnswer('id_self_eval')
        & checkAgreeForAnswer()
        & checkForAnswer('id_self_eval_statement')) {
    // switch to profile screen
    show("page4", "page3");
  }
}


// prevent using Enter key to submit form
forms = document.getElementsByTagName('form');
for (let i = 0; i < forms.length; i++) {
    forms[i].onkeydown = ()=>(event.key != 'Enter');
}

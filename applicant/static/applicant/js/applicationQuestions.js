const treatment = parseInt(document.getElementById('treatment').innerHTML);

function initiate() {
  // set avatar
  gender = document.getElementById('gender').innerHTML.toLowerCase();
  if (gender == 'other') {
      gender = ['male', 'female'][Math.floor(Math.random() * 2)]
  }
  let num = Math.floor(Math.random() * 3) + 1;  // random int in (1, 2, 3)
  let avatar = gender + num + '.jpg';
  document.getElementById('id_avatar').value = avatar;
  document.getElementById('avatar_demo').src = '/static/applicant/' + avatar;
  if (treatment == 0) {
      // skip first page
      show('page2', 'page1');
  }
}

function checkForAnswer(form_id) {
    let form = document.getElementById(form_id);
    if (form_id == 'id_avatar') {
      var buttons = form.getElementsByClassName('input-hidden');
    }
    else {
      var buttons = form.getElementsByClassName('form-check-input');
    }
    let checked = false;
    for (i = 0; i < buttons.length; i++) {
      if (buttons[i].checked) {
        checked = true;
        break;
      }
    }
    if (!checked) {
      document.getElementById('not-complete-error').style.display = 'block';
      return false;
    }
    else {
      return true;
    }
}

function seeProfile() {
  if (checkForAnswer('id_self_eval')
        && checkForAnswer('id_self_eval_statement')) {
    // switch to profile screen
    show("page4", "page3");
    document.getElementById('not-complete-error').style.display = 'none';
  }
}

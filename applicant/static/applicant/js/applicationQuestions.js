function getTreatment() {
  var treatment = document.getElementById('treatment').innerHTML;
  return parseInt(treatment);
}

function initiate() {
  if (getTreatment() == 0) {
    show('page3', 'page1');
  }
  else {
    show('page2', 'page1');
  }
}

function checkForAnswer(form_id) {
  try {
    var form = document.getElementById(form_id);
    if (form_id == 'id_avatar') {
      var buttons = form.getElementsByClassName('input-hidden');
    }
    else {
      var buttons = form.getElementsByClassName('form-check-input');
    }
    var checked = false;
    for (i=0; i<buttons.length; i++) {
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
  catch(error) {
    console.log(error);
  }
}

function nextQuestion() {
  if (checkForAnswer('id_avatar')) {
    show("page3", "page2");
    document.getElementById('not-complete-error').style.display = 'none';
  }
}

function backQuestion() {
  if (getTreatment() == 0) {
    show('page1', 'page3');
  }
  else {
    show('page2', 'page3');
  }
}

function seeProfile() {
  if (checkForAnswer('id_self_eval') && checkForAnswer('id_self_eval_relative')
        && checkForAnswer('id_self_eval_usual')) {
    // switch to profile screen
    show("page4", "page3");
    document.getElementById('not-complete-error').style.display = 'none';
  }
}

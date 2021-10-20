let currentQuestion;
let questionIndex = 0;

function getOrder() {
    let string = document.getElementById('display-order').innerHTML.replace(/\s+/g, '');
    return string.split("-");
}

const numQuestions = getOrder().length;
const bankSize = document.getElementById('bank-size').innerHTML;

function updateCurrentQuestion() {
    currentQuestion = getOrder()[questionIndex];
    document.getElementById(currentQuestion).style.display = 'block';
}

function isChecked(q_num) {
    let buttons = document.getElementById('id_q' + q_num)
                          .getElementsByClassName('form-check-input');
    let checked = false;
    for (let i = 0; i < buttons.length; i++) {
      if (buttons[i].checked) {
        checked = true;
        break;
      }
    }
    return checked;
}

function finish() {
    document.getElementById('done').style.display = 'block';
    document.getElementById('question-indicator').style.display = 'none';
    // give default answers for any questions the user didn't see
    for (let i = 1; i <= bankSize; i++) {
        if (!isChecked(i)) {
            let buttons = document.getElementById('id_q' + i)
                                  .getElementsByClassName('form-check-input');
            buttons[0].checked = true;
        }
    }
}

function nextQuestion() {
  // Check that an answer is selected
    if (!isChecked(currentQuestion)) {
      document.getElementById('not-complete-error').style.display = 'block';
      return;
    }
    questionIndex++;
    // hide current question and move to next
    document.getElementById(currentQuestion).style.display = 'none';
    if (questionIndex == numQuestions) {
        finish();
    }
    else {
        updateCurrentQuestion();
    }
    // advance displayed question number and hide error message
    var qnum = document.getElementById('question-number');
    qnum.innerHTML = questionIndex + 1;
    document.getElementById('not-complete-error').style.display = 'none';
}

function beginQuestions() {
    document.getElementById('0').style.display = 'none';
    document.getElementById('question-indicator').style.display = 'block';
    updateCurrentQuestion();
}

function skip() {
    // for developer's eyes only ;)
    if (document.getElementById('0').style.display != 'none') {
        beginQuestions();
    }
    while (questionIndex < numQuestions) {
        document.getElementById('id_q' + currentQuestion).getElementsByClassName('form-check-input')[0].checked = true;
        nextQuestion();
    }
}

// prevent using Enter key to submit form
forms = document.getElementsByTagName('form');
for (let i = 0; i < forms.length; i++) {
    forms[i].onkeydown = ()=>(event.key != 'Enter');
}

let currentQuestion;
let questionIndex = 0;

function getOrder() {
    let string = document.getElementById('display-order').innerHTML.replace(/\s+/g, '');
    return string.split("-");
}

let numQuestions = getOrder().length;

function updateCurrentQuestion() {
    currentQuestion = getOrder()[questionIndex];
    document.getElementById(currentQuestion).style.display = 'block';
}

function nextQuestion() {
  // Check that an answer is selected
    let buttons = document.getElementById('id_q' + currentQuestion
                            ).getElementsByClassName('form-check-input');
    let checked = false;
    for (let i = 0; i < buttons.length; i++) {
      if (buttons[i].checked) {
        checked = true;
        break;
      }
    }
    if (!checked) {
      document.getElementById('not-complete-error').style.display = 'block';
      return;
    }
    questionIndex++;
    // hide current question and move to next
    document.getElementById(currentQuestion).style.display = 'none';
    if (questionIndex == numQuestions) {
        // finished
        document.getElementById('done').style.display = 'block';
        document.getElementById('question-indicator').style.display = 'none';
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

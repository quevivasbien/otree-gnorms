function getOrder() {
  var string = document.getElementById('display-order').innerHTML.replace(/\s+/g, '');
  return string.split("-");
}

function firstQuestion() {
  var first = getOrder()[0];
  document.getElementById(first).style.display = 'block';
}

function nextQuestion(currentQuestion) {
  // Check that an answer is selected
  try {
    var buttons = document.getElementById('id_q' + currentQuestion
                            ).getElementsByClassName('form-check-input');
    var checked = false;
    for (i=0; i<buttons.length; i++) {
      if (buttons[i].checked) {
        checked = true;
        break;
      }
    }
    if (!checked) {
      document.getElementById('not-complete-error').style.display = 'block';
      return;
    }
  }
  catch(error) {
    console.log(error);
  }
  // hide current question and move to next
  document.getElementById(currentQuestion).style.display = 'none';
  var order = getOrder();
  if (currentQuestion == order[order.length - 1]) {
    document.getElementById('done').style.display = 'block';
    document.getElementById('question-indicator') = 'none';
  }
  else {
    for (i = 0; i < order.length - 1; i++) {
      if (order[i] == currentQuestion) {
        document.getElementById(order[i+1]).style.display = 'block';
        break;
      }
    }
  }
  // advance question number and hide error message
  var qnum = document.getElementById('question-number');
  qnum.innerHTML = parseInt(qnum.innerHTML) + 1;
  document.getElementById('not-complete-error').style.display = 'none';
}

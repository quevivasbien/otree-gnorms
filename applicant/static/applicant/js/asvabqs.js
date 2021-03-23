function getOrder() {
  var string = document.getElementById('display-order').innerHTML.replace(/\s+/g, '');
  return string.split("-");
}

function firstQuestion() {
  var first = getOrder()[0]
  document.getElementById(first).style.display = 'block';
}

function nextQuestion(currentQuestion) {
  // TODO: Add check to check that the question is answered
  document.getElementById(currentQuestion).style.display = 'none';
  var order = getOrder();
  if (currentQuestion == order[order.length - 1]) {
    document.getElementById('done').style.display = 'block';
  }
  else {
    for (i = 0; i < order.length - 1; i++) {
      if (order[i] == currentQuestion) {
        document.getElementById(order[i+1]).style.display = 'block';
        break;
      }
    }
  }
}

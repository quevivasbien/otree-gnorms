var currentQuestion = 0;

var promote1_dict = {
  '0': 'terrible',
  '1': 'not good',
  '2': 'neutral',
  '3': 'good',
  '4': 'very good',
  '5': 'excellent'
}

var promote2_dict = {
  '0': 'representative of my ability at the task.',
  '1': 'too low compared to my ability; I expect to do better in general.',
  '2': 'too high compared to my ability; I expect to do worse in general.'
}

var promote3_dict = {
  '0': '“Usually I am the best at what I do.”',
  '1': '“I conduct all tasks assigned to me, no matter how small, with the needed attention.”'
}

function getVals(id) {
  let string = document.getElementById(id).innerHTML;
  return string.split("-");
}

function displayQuestion(n) {
  var treatments = getVals('wg-treatment');
  // check to see if that's all the questions
  if (n >= treatments.length) {
    return false;
  }
  var treatment = treatments[n];
  // set up pronoun and avatar image
  if (treatment != 0) {
    // get gender
    var gender = getVals('wg-gender')[n];
    if (gender == "Male") {
      var pronoun = "his";
    }
    else {
      var pronoun = "her";
    }
    // display correct image
    let image = document.getElementById('app-avatar');
    image.style.display = 'block';
    let imagenum = parseInt(getVals('wg-image')[n]);
    image.src = '/static/applicant/' + gender.toLowerCase() + (imagenum + 1) + '.jpg';
  }
  else {
    var pronoun = "their";
    document.getElementById('app-avatar').style.display = 'none';
  }
  // display or hide performance
  let perform = document.getElementById('app-performance');
  if (treatment == 2) {
    perform.style.display = 'block';
    perform.innerHTML = 'The applicant correctly answered ' + getVals('wg-perform')[n] + ' out of 10 evaluation questions.';
  }
  else {
    perform.style.display = 'none';
  }
  // set up self-promotion
  let promote_type = getVals('wg-promote-type')[n];
  let message = document.getElementById('app-self-eval');
  if (promote_type == '0') {
    let promote1 = getVals('wg-promote1')[n];
    message.innerHTML = '<p>The applicant rated ' + pronoun + ' performance as ' + promote1_dict[promote1] + '.</p>';
  }
  else if (promote_type == '1') {
    let promote2 = getVals('wg-promote2')[n];
    message.innerHTML = '<p>When asked to assess ' + pronoun + ' performance, the applicant stated, "I would say my performance here is ' + promote2_dict[promote2] + '"</p>';
  }
  else {
    let promote3 = getVals('wg-promote3')[n];
    if (promote3 != '2') {
      message.innerHTML = '<p>The applicant chose the following statement to accompany ' + pronoun + ' application:</p><p>' + promote3_dict[promote3] + '</p>';
    }
    else {
      message.innerHTML = '<p>The applicant chose to not include any statement with ' + pronoun + ' application.</p>';
    }
  }
  // display the correct value in the bidding bar
  let wg_other = document.getElementById('hidden-input').value.split('-');
  let rangeInput = document.getElementById('rangeInput4');
  let amountInput = document.getElementById('amount4');
  if (wg_other.length < currentQuestion + 1 || !wg_other[0]) {
    rangeInput.value = 0.5;
    amountInput.value = 0.5;
  }
  else {
    let value = parseFloat(wg_other[currentQuestion]);
    rangeInput.value = value;
    amountInput.value = value;
  }
  // signal that we've completed successfully
  return true;
}

function startOther() {
  displayQuestion(0);
  show('page6', 'page5');
}

function updateHiddenInput() {
  let hidden_input = document.getElementById('hidden-input');
  let wg_other = hidden_input.value.split('-');
  let rangeInputValue = document.getElementById('rangeInput4').value;
  if (wg_other.length < currentQuestion + 1) {
    wg_other.push(rangeInputValue);
  }
  else {
    wg_other[currentQuestion] = rangeInputValue;
  }
  hidden_input.value = wg_other.join('-');
}

function nextQuestion() {
  // update output for wage_guess_other
  updateHiddenInput();
  // advance question
  currentQuestion++;
  if (!displayQuestion(currentQuestion)) {
    // go to the finish page
    currentQuestion--;
    show('page7', 'page6');
  }
}

function backQuestion() {
  updateHiddenInput();
  currentQuestion--;
  if (currentQuestion < 0) {
    show("page5", "page6");
    currentQuestion = 0;
  }
  else {
    displayQuestion(currentQuestion);
  }
}

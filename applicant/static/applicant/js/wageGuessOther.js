var currentQuestion = 0;
let treatments = getVals('wg-treatment');
let defaultRangeValue = parseFloat(document.getElementById('default-range-val').innerHTML);

const promote1_dict = {
  '0': 'terrible',
  '1': 'not good',
  '2': 'neutral',
  '3': 'good',
  '4': 'very good',
  '5': 'excellent'
}

const promote3_dict = {
  '0': '“Usually I am the best at what I do, and therefore I would succeed in a job that required me to perform well in tasks similar to the test in Part 1.”',
  '1': '“I conduct all tasks assigned to me with the needed attention, and therefore I would work hard in a job that required me to perform well in tasks similar to the test in Part 1.”'
}

function getVals(id) {
  // get array of values associated with html DOM id
  let string = document.getElementById(id).innerHTML;
  return string.split("-");
}

function setUpQuestion(n) {
    // check to see if that's all the questions
    if (n >= treatments.length) {
      return false;
    }
    let treatment = treatments[n];
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
      perform.innerHTML = 'The applicant correctly answered ' + getVals('wg-perform')[n] + ' out of 10 application questions.';
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
      let promote2a = getVals('wg-promote2a')[n];
      let promote2b = getVals('wg-promote2b')[n];
      let promote2c = getVals('wg-promote2c')[n];
      message.innerHTML = '<p>When asked to rate ' + pronoun + ' level of agreement with the following questions on a scale from 0 (entirely disagree) to 100 (entirely agree), the applicant gave the following answers:</p>'
          + '<p>"I performed well on the test I took in Part 1." <b>' + promote2a + ' out of 100</b></p>'
          + '<p>"Usually I am the best at what I do." <b>' + promote2b + ' out of 100</b></p>'
          + '<p>"I conduct all tasks assigned to me with the needed attention." <b>' + promote2c + ' out of 100</b></p>';
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
    // update question number indicator
    document.getElementById('other-app-num').innerHTML = (n+1) + ' of ' + treatments.length;
    return true;  // successfully completed
}

function displayQuestion() {
  // set up and signal problem if not successful
  if (!setUpQuestion(currentQuestion)) return false;
  // display the correct value in the bidding bar
  let wg_other = document.getElementById('hidden-input').value.split('-');
  let rangeInput = document.getElementById('rangeInput4');
  let amountInput = document.getElementById('amount4');
  if (wg_other.length < currentQuestion + 1 || !wg_other[0]) {
    rangeInput.value = defaultRangeValue;
    amountInput.value = defaultRangeValue;
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
  displayQuestion();
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
  if (!displayQuestion()) {
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
    displayQuestion();
  }
}

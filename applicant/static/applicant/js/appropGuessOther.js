// overrides some functions from wageGuessOther.js to work with radio select in SocAppropGuess.html
let buttons = document.getElementById('id_approp_guess_other').getElementsByClassName('form-check-input');
let missing_response = document.getElementById('missing-response-error');

function checkBeforeAdvance(i) {
    // checks if no response on ith own appropriateness guess, goes to next question otherwise
    let buttons_self = document.getElementById('id_approp_guess' + i).getElementsByClassName('form-check-input');
    let checked = false;
    for (let i = 0; i < buttons_self.length; i++) {
        if (buttons_self[i].checked) {
            checked = true;
            break;
        }
    }
    if (checked) {
        missing_response.style.display = 'none';
        show('page' + (i+2), 'page' + (i+1));
    }
    else {
        missing_response.style.display = 'block';
    }
}

function updateRadioSelect() {
    let guess_other = document.getElementById('hidden-input').value.split('-').map(str => parseInt(str));
    if (guess_other.length < currentQuestion + 1 || isNaN(guess_other[0])) {
        // uncheck all
        for (let i = 0; i < buttons.length; i++) {
            buttons[i].checked = false;
        }
    }
    else {
        // if guess_other[currentQuestion] is a valid integer, check button with that index
        buttons[guess_other[currentQuestion]].checked = true;
    }

}

function displayQuestion() {
  // set up and signal problem if not successful
  if (!setUpQuestion(currentQuestion)) return false;
  // display the correct input in the radio select
  updateRadioSelect();
  // signal that we've completed successfully
  return true;
}

function updateHiddenInput() {
  // get response for current question
  let response = NaN;
  for (let i = 0; i < buttons.length; i++) {
      if (buttons[i].checked) {
          response = i;
          break;
      }
  }
  if (isNaN(response)) {
      // stop here and don't allow progression to next question
      return false;
  }
  let hidden_input = document.getElementById('hidden-input');
  let guess_other = hidden_input.value.split('-');
  if (guess_other.length < currentQuestion + 1) {
    guess_other.push(response);
  }
  else {
    guess_other[currentQuestion] = response;
  }
  hidden_input.value = guess_other.join('-');
  return true;
}

function nextQuestion() {
  // update output for wage_guess_other and check if we can proceed
  if (updateHiddenInput()) {
      // advance question
      currentQuestion++;
      if (!displayQuestion()) {
        // go to the finish page
        currentQuestion--;
        show('page7', 'page6');
      }
      missing_response.style.display = 'none';
  }
  else {
      // display error message
      missing_response.style.display = 'block';
  }
}

function backQuestion() {
  updateHiddenInput();
  currentQuestion--;
  displayQuestion();
  missing_response.style.display = 'none';
  if (currentQuestion < 0) {
    show("page5", "page6");
    currentQuestion = 0;
  }
  else {
    displayQuestion();
  }
}

var currentTab = 1;
var currentPart = 1;

document.getElementById('player-bids').value = '0.5-'.repeat(30).slice(0, -1);

function getVar(id) {
  let string = document.getElementById(id).innerHTML;
  return string.split('-')[currentTab-1];
}

function getPronoun() {
  let treatment = parseInt(getVar('participant-treatment'));
  if (treatment == 0) {
    return 'their';
  }
  else {
    let gender = getVar('participant-gender');
    if (gender == "Male") {
      return 'his';
    }
    else if (gender == "Female") {
      return 'her';
    }
    else {
      return 'their';
    }
  }
}

function setSelfEval(self_eval) {
  let div = document.getElementById('self-eval');
  div.innerHTML = '<p>The applicant rated ' + getPronoun()
                    + ' performance as <em>' + self_eval + '</em>.</p>';
}

function setSelfEvalRelative(self_eval) {
  let div = document.getElementById('self-eval-relative');
  div.innerHTML = '<p>When asked to assess ' + getPronoun()
                    + ' performance, the applicant stated, "I would say my performance here is '
                    + self_eval + '"</p>';
}

function setSelfEvalUsual(self_eval) {
  let div = document.getElementById('self-eval-usual');
  if (self_eval.startsWith("I prefer")) {
    div.innerHTML = '<p>The applicant chose to not include any statement with '
                      + getPronoun() + ' application.</p>';
  }
  else {
    div.innerHTML = '<p>The applicant chose the following statement to accompany '
                      + getPronoun() + ' application:</p><p>'
                      + self_eval + '</p>';
  }
}

function updateDisplay() {
  // update question number indicator
	document.getElementById('question-number').innerHTML = currentTab;
  let treatment = getVar('participant-treatment');
  // set up avatar
  let image = document.getElementById('avatar');
  if (treatment == 0) {
    image.style.display = 'none';
  }
  else {
    image.style.display = 'block';
    image.src = '/static/applicant/' + getVar('participant-avatar');
  }
  // set up self-evaluation
  if (currentPart == 1) {
    let self_eval = getVar('participant-self-eval');
    document.getElementById('self-eval').style.display = 'block';
    document.getElementById('self-eval-relative').style.display = 'none';
    document.getElementById('self-eval-usual').style.display = 'none';
  	setSelfEval(self_eval);
  }
  else if (currentPart == 2) {
    let self_eval = getVar('participant-self-eval-rel');
    document.getElementById('self-eval').style.display = 'none';
    document.getElementById('self-eval-relative').style.display = 'block';
    document.getElementById('self-eval-usual').style.display = 'none';
  	setSelfEvalRelative(self_eval);
  }
  else {
    let self_eval = getVar('participant-self-eval-usu');
    document.getElementById('self-eval').style.display = 'none';
    document.getElementById('self-eval-relative').style.display = 'none';
    document.getElementById('self-eval-usual').style.display = 'block';
  	setSelfEvalUsual(self_eval);
  }
  // set up performance
  if (treatment == 2) {
    let eval_correct = parseInt(getVar('participant-eval-correct'));
    document.getElementById('display-eval-correct').style.display = 'block';
    document.getElementById('eval-correct').innerHTML = eval_correct;
  }
  else {
    document.getElementById('display-eval-correct').style.display = 'none';
  }
  // set up slider
	let rangeInput = document.getElementById('rangeInput');
	rangeInput.value = parseFloat(
    document.getElementById('player-bids').value.split('-')[currentTab - 1]
  );
	document.getElementById('amount').value = rangeInput.value;
}

function sendEntry() {
	let playerBids = document.getElementById('player-bids');
	let bids = playerBids.value.split("-");
	let new_bid = document.getElementById('rangeInput').value;
	bids[currentTab-1] = new_bid;
	playerBids.value = bids.join("-");
}

function startPart1() {
  show('questions', 'part1explain');
  currentTab = 1;
  updateDisplay();
}

function startPart2() {
  show('questions', 'part2explain');
  currentTab = 11;
  currentPart = 2;
  updateDisplay();
}

function startPart3() {
  show('questions', 'part3explain');
  currentTab = 21;
  currentPart = 3;
  updateDisplay();
}

function backToPart1() {
  show('questions', 'part2explain');
  currentTab = 10;
  currentPart = 1;
  updateDisplay();
}

function backToPart2() {
  show('questions', 'part3explain');
  currentTab = 20;
  currentPart = 2;
  updateDisplay();
}

function forward() {
  sendEntry();
  currentTab++;
  if (currentTab == 11) {
    show('part2explain', 'questions');
  }
  else if (currentTab == 21) {
    show('part3explain', 'questions');
  }
	else if (currentTab == 31) {
    show('finished', 'questions');
	}
	else {
		updateDisplay();
	}
}

function back() {
  if (currentTab > 30) {
    show('questions', 'finished');
    currentTab--;
  }
  else {
    sendEntry();
    currentTab--;
    if (currentTab == 0) {
      show('part1explain', 'questions');
      currentTab++;
    }
    else if (currentTab == 10) {
      show('part2explain', 'questions');
    }
  	else if (currentTab == 20) {
      show('part3explain', 'questions');
  	}
  	else {
      updateDisplay();
    }
  }
}

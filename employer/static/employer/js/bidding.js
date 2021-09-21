let currentTab = 1;
let currentPart = 1;

function getVar(id) {
  let string = document.getElementById(id).innerHTML;
  return string.split('-')[currentTab-1];
}

const treatment = parseInt(document.getElementById('participant-treatment'));
const numApplicants = getVar('participant-gender').length;

document.getElementById('player-bids').value = '0.5-'.repeat(numApplicants * 3).slice(0, -1);

function getPronoun() {
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

function setSelfEvalVisible(currentPart) {
    document.getElementById('self-eval').style.display = ((currentPart == 1) ? 'block' : 'none');
    document.getElementById('self-eval-agree').style.display = ((currentPart == 2) ? 'block' : 'none');
    document.getElementById('self-eval-statement').style.display = ((currentPart == 3) ? 'block' : 'none');
}

function setSelfEval(self_eval) {
  let div = document.getElementById('self-eval');
  div.innerHTML = '<p>The applicant rated ' + getPronoun()
                    + ' performance as <em>' + self_eval + '</em>.</p>';
}

function setSelfEvalAgree(agree0, agree1, agree2) {
  let div = document.getElementById('self-eval-agree');
  div.innerHTML = '<p>When asked to rate ' + getPronoun() + ' level of agreement with the following questions on a scale from 0 (entirely disagree) to 100 (entirely agree), the applicant gave the following answers:</p>'
      + '<p>"I performed well on the test I took in part 1." <b>' + parseInt(agree0) + ' out of 100</b></p>'
      + '<p>"Usually I am the best at what I do." <b>' + parseInt(agree1) + ' out of 100</b></p>'
      + '<p>"I conduct all tasks assigned to me with the needed attention." <b>' + parseInt(agree2) + ' out of 100</b></p>';
}

function setSelfEvalStatement(self_eval) {
  let div = document.getElementById('self-eval-statement');
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
  setSelfEvalVisible(currentPart);
  if (currentPart == 1) {
    let self_eval = getVar('participant-self-eval');
  	setSelfEval(self_eval);
  }
  else if (currentPart == 2) {
    let agree0 = getVar('participant-self-eval-agree0');
    let agree1 = getVar('participant-self-eval-agree1');
    let agree2 = getVar('participant-self-eval-agree2');
  	setSelfEvalAgree(agree0, agree1, agree2);
  }
  else {
    let self_eval = getVar('participant-self-eval-statement');
  	setSelfEvalStatement(self_eval);
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
  currentTab = numApplicants + 1;
  currentPart = 2;
  updateDisplay();
}

function startPart3() {
  show('questions', 'part3explain');
  currentTab = numApplicants * 2 + 1;
  currentPart = 3;
  updateDisplay();
}

function backToPart1() {
  show('questions', 'part2explain');
  currentTab = numApplicants;
  currentPart = 1;
  updateDisplay();
}

function backToPart2() {
  show('questions', 'part3explain');
  currentTab = numApplicants * 2;
  currentPart = 2;
  updateDisplay();
}

function forward() {
  sendEntry();
  currentTab++;
  if (currentTab == numApplicants + 1) {
    show('part2explain', 'questions');
  }
  else if (currentTab == numApplicants * 2 + 1) {
    show('part3explain', 'questions');
  }
	else if (currentTab == numApplicants * 3 + 1) {
    show('finished', 'questions');
	}
	else {
		updateDisplay();
	}
}

function back() {
  if (currentTab > numApplicants * 3) {
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
    else if (currentTab == numApplicants) {
      show('part2explain', 'questions');
    }
  	else if (currentTab == numApplicants * 2) {
      show('part3explain', 'questions');
  	}
  	else {
      updateDisplay();
    }
  }
}

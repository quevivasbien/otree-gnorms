let currentTab = 1;
let currentPart = 1;

function getVar(id) {
  let string = document.getElementById(id).innerHTML;
  return string.split('-')[currentTab-1];
}

const treatment = parseInt(document.getElementById('participant-treatment').innerHTML);
const numApplicants1 = parseInt(document.getElementById('apps-per-emp1').innerHTML);
const numApplicants2 = parseInt(document.getElementById('apps-per-emp2').innerHTML);
const numApplicants3 = parseInt(document.getElementById('apps-per-emp3').innerHTML);

const defaultBid = document.getElementById('default-bid').innerHTML;
const bidIsInt = parseInt(defaultBid) == defaultBid;

const rangeInput = document.getElementById('rangeInput');
const amount = document.getElementById('amount');
const no_response_message = document.getElementById('no-response-message');

const playerBids = document.getElementById('player-bids');

const performCDF = document.getElementById('perform-cdf').innerHTML.split('-').map(parseFloat);

playerBids.value = ('?-').repeat(numApplicants1 + numApplicants2 + numApplicants3).slice(0, -1);

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

function setSelfEvalAgree(agree) {
  let div = document.getElementById('self-eval-agree');
  div.innerHTML = '<p>When asked to rate ' + getPronoun() + ' level of agreement with the statement</p><p>"I performed well on the test I took in Part 1,"</p><p>on a scale from 0 (entirely disagree) to 100 (entirely agree), the applicant gave the following rating:</p>'
      + '<p><b>' + parseInt(agree) + ' out of 100</b></p>';
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

function toggleHelp() {
    help_div = document.getElementById('help');
    if (help == null) {
        return;
    }
    toggler_button = document.getElementById('toggle-help');
    if (help_div.style.display == 'none') {
        help_div.style.display = 'block';
        toggler_button.innerHTML = '[Hide help]';
        toggler_button.style.fontStyle = 'italic';
    }
    else {
        help_div.style.display = 'none';
        toggler_button.innerHTML = '[Show help]';
        toggler_button.style.fontStyle = 'normal';
    }
}

function updateAmount() {
    if (bidIsInt) {
        amount.innerHTML = rangeInput.value;
    }
    else {
        amount.innerHTML = parseFloat(rangeInput.value).toFixed(2);
    }
}

function updateInputDisplay() {
    // set up slider
    let value = playerBids.value.split('-')[currentTab - 1];
    if (value == '?') {
        rangeInput.value = defaultBid;
        amount.innerHTML = '--';
    }
    else {
        rangeInput.value = value;
        updateAmount();
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
    let agree = getVar('participant-self-eval-agree');
  	setSelfEvalAgree(agree);
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
    document.getElementById('eval-correct-percentile').innerHTML = parseInt(performCDF[eval_correct] * 100);
  }
  else {
    document.getElementById('display-eval-correct').style.display = 'none';
  }
  updateInputDisplay();
}

function sendEntry() {
	let new_bid = amount.innerHTML;
    if (new_bid == '--') {
        return false;
    }
    else {
        let bids = playerBids.value.split("-");
    	bids[currentTab-1] = new_bid;
    	playerBids.value = bids.join("-");
        return true;
    }
}

function startPart1() {
  show('questions', 'part1explain');
  currentTab = 1;
  updateDisplay();
}

function startPart2() {
  show('questions', 'part2explain');
  currentTab = numApplicants1 + 1;
  currentPart = 2;
  updateDisplay();
}

function startPart3() {
  show('questions', 'part3explain');
  currentTab = numApplicants1 + numApplicants2 + 1;
  currentPart = 3;
  updateDisplay();
}

function backToPart1() {
  show('questions', 'part2explain');
  currentTab = numApplicants1;
  currentPart = 1;
  updateDisplay();
}

function backToPart2() {
  show('questions', 'part3explain');
  currentTab = numApplicants1 + numApplicants2;
  currentPart = 2;
  updateDisplay();
}

function forwardTab() {
    currentTab++;
    if (currentTab == numApplicants1 + 1) {
      show('part2explain', 'questions');
    }
    else if (currentTab == numApplicants1 + numApplicants2 + 1) {
      show('part3explain', 'questions');
    }
  	else if (currentTab == numApplicants1 + numApplicants2 + numApplicants3 + 1) {
      show('finished', 'questions');
  	}
  	else {
  		updateDisplay();
  	}
}

function backTab() {
    currentTab--;
    if (currentTab == 0) {
      show('part1explain', 'questions');
      currentTab++;
    }
    else if (currentTab == numApplicants1) {
      show('part2explain', 'questions');
    }
  	else if (currentTab == numApplicants1 + numApplicants2) {
      show('part3explain', 'questions');
  	}
  	else {
      updateDisplay();
    }
}

function forward() {
    if (sendEntry()) {
        forwardTab();
        no_response_message.style.display = 'none';
    }
    else {
        no_response_message.style.display = 'block';
    }
}

function back() {
    if (currentTab > numApplicants1 + numApplicants2 + numApplicants3) {
        show('questions', 'finished');
        currentTab--;
    }
    else {
        sendEntry();
        backTab();
        no_response_message.style.display = 'none';
    }
}

// prevent using Enter key to submit form
forms = document.getElementsByTagName('form');
for (let i = 0; i < forms.length; i++) {
    forms[i].onkeydown = ()=>(event.key != 'Enter');
}

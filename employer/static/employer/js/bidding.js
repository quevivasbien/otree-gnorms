var currentTab = 0;

function getEvalCorrect() {
  let string = document.getElementById('participant-eval-correct').innerHTML.replace(/\s+/g, '');
  return string.split("-")[currentTab-1];
}

function getGender() {
	let string = document.getElementById('participant-gender').innerHTML.replace(/\s+/g, '');
  return string.split("-")[currentTab-1];
}

function getSelfEval() {
	let string = document.getElementById('participant-self-eval').innerHTML.replace(/\s+/g, '');
  return string.split("-")[currentTab-1];
}

function getBid() {
	let string = document.getElementById('player-bids').innerHTML.replace(/\s+/g, '');
  return string.split("-")[currentTab-1];
}

function numQs() {
	return document.getElementById('player-bids').innerHTML.replace(/\s+/g, '').split("-").length
}

function updateDisplay() {
	document.getElementById('question-number').innerHTML = currentTab;
	document.getElementById('self-eval').innerHTML = getSelfEval();
	let gender = document.getElementById('gender');
	if (gender) {
		gender.innerHTML = getGender();
	}
	let evalCorrect = document.getElementById('eval-correct')
	if (evalCorrect) {
		evalCorrect.innerHTML = getEvalCorrect();
	}
	let rangeInput = document.getElementById('rangeInput');
	rangeInput.value = getBid();
	document.getElementById('amount').value = rangeInput.value;
}

function sendEntry() {
	let playerBids = document.getElementById('player-bids');
	let bids = playerBids.innerHTML.replace(/\s+/g, '').split("-");
	let new_bid = document.getElementById('rangeInput').value;
	bids[currentTab-1] = new_bid;
	liveSend(bids);
	playerBids.innerHTML = bids.join("-");
}

function forward() {
	if (currentTab == 0) {
		document.getElementById('intro').style.display = 'none';
		document.getElementById('questions').style.display = 'block';
		currentTab++;
		updateDisplay();
	}
	else if (currentTab == numQs()) {
		sendEntry();
		currentTab++;
		document.getElementById('questions').style.display = 'none';
		document.getElementById('finished').style.display = 'block';
	}
	else {
		sendEntry();
		currentTab++;
		updateDisplay();
	}
}

function back() {
	if (currentTab <= numQs()) {
		sendEntry();
	}
	currentTab--;
	if (currentTab == 0) {
		document.getElementById('intro').style.display = 'block';
		document.getElementById('questions').style.display = 'none';
	}
	else if (currentTab == numQs()) {
		document.getElementById('questions').style.display = 'block';
		document.getElementById('finished').style.display = 'none';
	}
	else {
		updateDisplay();
	}
}

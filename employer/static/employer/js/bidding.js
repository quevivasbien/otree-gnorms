var currentTab = 0;

function getEvalCorrect() {
  let string = document.getElementById('participant-eval-correct').innerHTML.replace(/\s+/g, '');
  return string.split("-")[currentTab];
}

function getGender() {
	let string = document.getElementById('participant-gender').innerHTML.replace(/\s+/g, '');
  return string.split("-")[currentTab];
}

function getSelfEval() {
	let string = document.getElementById('participant-self-eval').innerHTML.replace(/\s+/g, '');
  return string.split("-")[currentTab];
}

function numQs() {
	return document.getElementById('participant-self-eval').innerHTML.replace(/\s+/g, '').split("-").length
}

function updateDisplay() {
	document.getElementById('question-number').innerHTML = currentTab;
	document.getElementById('self-eval').innerHTML = getSelfEval();
	document.getElementById('gender').innerHTML = getGender();
	document.getElementById('eval-correct').innerHTML = getEvalCorrect();
	document.getElementById('range-input').value = 0.5;
}

function sendEntry() {
	let bid = document.getElementById('range-input').value;
	liveSend({"currentTab": currentTab, "bid": bid});
}

function forward() {
	if (currentTab == 0) {
		document.getElementById('intro').style.display = 'none';
		document.getElementById('questions').style.display = 'block';
		currentTab++;
		updateDisplay();
	}
	else if (currentTab == numQs() - 1) {
		sendEntry();
		// TODO: validate that the user really wants to submit
		$('#form').submit();
	}
	else {
		sendEntry();
		currentTab++;
		updateDisplay();
	}
}

function back() {
	sendEntry();
	currentTab--;
	if (currentTab == 0) {
		document.getElementById('intro').style.display = 'block';
		document.getElementById('questions').style.display = 'none';
	}
	else {
		updateDisplay();
	}
}

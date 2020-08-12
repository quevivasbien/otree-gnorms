function show() {
	var questions = document.getElementById('to_show');
	if (questions.style.display == 'none') {
		questions.style.display = 'block';
	}
	var button = document.getElementById('button');
	if (button.style.display == 'block') {
		button.style.display = 'none';
	}
}

function displayErrorMessage() {
	var error_message = document.getElementById('error_message');
	error_message.style.display = 'block';
}

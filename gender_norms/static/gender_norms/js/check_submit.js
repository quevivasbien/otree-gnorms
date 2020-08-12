function checkSelectSubmit() {
	var values = $('select').map(function() { return this.value; })
	for (i = 0, len = values.length; i < len; i++) {
		if (values[i] === '') {
			alert('The form is missing a response. Go back and answer any unanswered questions.');
			break;
		}
	}
}

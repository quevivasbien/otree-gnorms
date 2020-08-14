function show(to_show = 'to_show', my_id = 'button') {
	var questions = document.getElementById(to_show);
	if (questions.style.display == 'none') {
		questions.style.display = 'block';
	}
	var button = document.getElementById(my_id);
	button.style.display = 'none';
}

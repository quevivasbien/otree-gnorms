function hide_nondisplay_buttons() {
	let btns = document.getElementsByClassName('btn-primary');
	for (button of buttons) {
		let parent = button.parentNode;
		if (parent.style.display == 'none') {
			button.hidden = true;
		}
		else {
			button.hidden = false;
		}
	}
}

function show(id_to_show = 'to_show', id_to_hide = 'button') {
	document.getElementById(id_to_show).style.display = 'block';
	document.getElementById(id_to_hide).style.display = 'none';
	// hide buttons in blocks not currently displayed, to try to fix double buttons problem in Safari
	hide_nondisplay_buttons();
}

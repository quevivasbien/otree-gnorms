function show(id_to_show = 'to_show', id_to_hide = 'button') {
	var to_show = document.getElementById(id_to_show);
	if (to_show.style.display == 'none') {
		to_show.style.display = 'block';
	}
	var to_hide = document.getElementById(id_to_hide);
	to_hide.style.display = 'none';
}

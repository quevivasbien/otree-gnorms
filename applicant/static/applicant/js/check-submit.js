function checkSubmit() {
	var forms = document.getElementsByClassName('form-group');
	for (let i = 0; i < forms.length; i++) {
		var radios = forms[i].getElementsByTagName('input');
		for (var j = 0; j < radios.length; j++) {
			if (radios[j].checked) {
				break;
			}
		}
		if (j === radios.length) {
			var navlinks = document.getElementsByClassName('nav-link');
			var tabpanes = document.getElementsByClassName('tab-pane');
			for (let k = 0; k < navlinks.length; k++) {
				if (k === i) {
					$(navlinks[k]).addClass('active');
					$(tabpanes[k]).addClass('show active');
				}
				else {
					$(navlinks[k]).removeClass('active');
					$(tabpanes[k]).removeClass('show active');
				}
			}
			break;
		}
	}
}

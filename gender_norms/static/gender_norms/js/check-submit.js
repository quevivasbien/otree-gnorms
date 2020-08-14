function checkSubmit() {
	var controls = document.getElementsByClassName('controls');
	for (let i = 0; i < controls.length; i++) {
		var radios = controls[i].getElementsByTagName('li');
		for (var j = 0; j < radios.length; j++) {
			if (radios[j].getElementsByTagName('input')[0].checked) {
				break;
			}
		}
		if (j === radios.length) {
			var navlinks = document.getElementsByClassName('nav-link');
			var tabpanes = document.getElementsByClassName('tab-pane');
			for (let k = 0; k < navlinks.length; k++) {
				if (k === i - 1) {
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

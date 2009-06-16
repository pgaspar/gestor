function showPwdForm(){
	$('password_form').show();
	$('password_form').focusFirstElement();
	$('private_img').hide();
}

function hidePwdForm(){
	$('password_form').hide();
	$('private_img').show();
	$('pwd_input').clear();
}
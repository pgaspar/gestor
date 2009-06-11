function showPwdForm(){
	$('password_form').show();
	Form.focusFirstElement( $('password_form') );
	$('private_img').hide();
}

function hidePwdForm(){
	$('password_form').hide();
	$('private_img').show();
}
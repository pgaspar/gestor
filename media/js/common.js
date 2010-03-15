function build_base_url(){ return window.location['protocol'] + '//' + window.location['host'] }

function followLink(obj) { window.location.href = obj.firstChild; }
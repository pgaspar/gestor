(function() {
	Event.observe(window, 'load',function() { 
		
		// Toggle history in Projects
		
		if ($('toggle-history')) {
			$$('.action-items li.green').each(function(i) {
				i.hide();
			});
			$('toggle-history').onclick = function() {
				$$('.action-items li.green').each(function(i) {
					i.toggle();
				});
			};
		}
		
		
		//Edit in place.
		if ($('editable_description')) {
			makeEditable('editable_description');
		}
	});
	
})();

function makeEditable(id){
	Event.observe(id, 'click', function(){edit($(id))}, false);
	Event.observe(id, 'mouseover', function(){showAsEditable($(id))}, false);
	Event.observe(id, 'mouseout', function(){showAsEditable($(id), true)}, false);
}

function showAsEditable(obj, clear){
	if (!clear){
		Element.addClassName(obj, 'editable');
	}else{
		Element.removeClassName(obj, 'editable');
	}
}

function edit(obj){
	Element.hide(obj);
	Element.show(obj.id + "_editor");
	
	Event.observe(obj.id+'_save', 'click', function(){saveChanges(obj)}, false);
	Event.observe(obj.id+'_cancel', 'click', function(){cleanUp(obj)}, false);

}

function cleanUp(obj, keepEditable){
	Element.hide(obj.id + "_editor");
	Element.show(obj);
	if (!keepEditable) showAsEditable(obj, true);
}

function saveChanges(obj){
	var new_content = $F(obj.id+'_edit');
	
	obj.preUpdate = new_content;
	obj.innerHTML = "Saving...";
	cleanUp(obj, true);

	var success = function(t){editComplete(t, obj);}
	var failure = function(t){editFailed(t, obj);}

	var url = 'fast_edit/';
	var pars = 'id=' + obj.id + '&content=' + new_content;
	var myAjax = new Ajax.Request(url, {method:'post',
		postBody:pars, onSuccess:success, onFailure:failure});
}

function editComplete(t, obj){
	obj.innerHTML = t.responseText;
	showAsEditable(obj, true);
}

function editFailed(t, obj){
	alert('Update failed!');
	obj.innerHTML = obj.preUpdate;
	cleanUp(obj);
}
(function() {
	
	Event.observe(window, 'load',function() { 
		
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
	});
	
	
})();
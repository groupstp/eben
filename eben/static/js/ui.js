$(document).ready(function(){
	
	$(".popup").magnificPopup();
	
	$("#edit_profile").on('submit', function(e){
	e.preventDefault();
    $.post($('#edit_profile').attr('action'))
	 .done(Ok);
    });
	
	function Ok(){
		setTimeout(function(){
				$.magnificPopup.close();
				location.reload();
			}, 500);
	}
			
})
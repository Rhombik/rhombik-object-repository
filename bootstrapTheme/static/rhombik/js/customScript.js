
  
//Stuff for image-tab controlling the large gallery pic.
//Call the flag
window.clickifyGallery = (function(){
  $('.imageSwitch').click(function(e){
  	var image = $(this).attr('rel');
  	var height = $('.printableImageContainer').height();
  	$('.printableImageContainer').css('height', height);
		// This is a bad if statement. Don't do this. Use better function.
	if($(this).attr("class")=="imageSwitch iframe jsc3d"){
        	$('.printableImageContainer').html('<iframe style="height:'+height+'px;width:100%;" src="' + image + '">');
	}else{
        	$('.printableImageContainer').html('<img src="' + image + '">');
	}
        $('.printableImageContainer').css('height', 'auto');
        e.preventDefault();
  });
});


$(document).ready(function(){

window.clickifyGallery();


});

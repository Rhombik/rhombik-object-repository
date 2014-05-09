
  
//Stuff for image-tab controlling the large gallery pic.
//Call the flag
$(document).ready(function(){
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


//tabbed text viewer switching. I'm hoping to move this in with project/static/script/tabbeler.coffee
  
	//$('#tabs article').hide();// this functionality is now covered by the tabbeler.
 


//scrolly top menu

$(window).scroll(function () {
  if($(this).scrollTop() > 58 && !$('header').hasClass('fixed') ){
  	$('header').addClass('fixed');
  } else if ($(this).scrollTop() <= 58 ) {
  	$('header').removeClass('fixed');
  }

  
});


//Other stuff!

var searchToggle = false;
var navToggle = false;
if(Modernizr.csstransitions){
    //CSS3 support method
    $('#navToggle, #mobileNav a').click(function() {
    	if(!navToggle){
    		navToggle = true;
		    $('#mobileNav').css({
		         'left' : '0px'
		    });
		    $('#innerWrap').css({
		    	'margin-right' : '-260px'
		    });
		    $('header').css({
		    	'left' : '260px'
		    });
		} else{
			navToggle = false;
			$('#mobileNav').css({
		         'left' : '-260px'
			});
			$('#innerWrap').css({
		    	'margin-right' : '0px'
		    });
		    $('header').css({
		    	'left' : '0px'
		    });
		}
	});
	
	$('#searchToggle').click(function(){
	if(!searchToggle){
		searchToggle = true;
		$('#mobileSearch').css({
			'margin-top' : '0px'
		});
	} else {
		searchToggle = false;
		$('#mobileSearch').css({
			'margin-top' : '-58px'
		});
	}
	});
}
else {
    //jQuery support usings to transition speed 
    //from the settings object
       $('#navToggle, #mobileNav a').click(function() {
    	if(!navToggle){
    		navToggle = true;
		    $('#mobileNav').animate({
		         'left' : '0px'
		    },200);
		    $('#innerWrap').animate({
		    	'margin-right' : '-260px'
		    },200);
		    $('header').animate({
		    	'left' : '260px'
		    },200);
		} else{
			navToggle = false;
			$('#mobileNav').animate({
		         'left' : '-260px'
			},200);
			$('#innerWrap').animate({
		    	'margin-right' : '0px'
		    },200);
		    $('header').animate({
		    	'left' : '0px'
		    },200);
		}
	});
	
	$('#searchToggle').click(function(){
	if(!searchToggle){
		searchToggle = true;
		$('#mobileSearch').animate({
			'margin-top' : '0px'
		},200);
	} else {
		searchToggle = false;
		$('#mobileSearch').animate({
			'margin-top' : '-58px'
		},200);
	}
});
}
});

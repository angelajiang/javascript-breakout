jQuery(document).ready(jQuery(function($) {
    $('.botname').change(function(){
	console.log('changed');
	newBot = $(this).val();
	
	game.reset(newBot);
    });
}));

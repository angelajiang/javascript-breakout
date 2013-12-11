jQuery(document).ready(jQuery(function($) {
    $('.botname').change(function(){
	console.log('changed');
	newBot = $(this).val();
	console.log(newBot);
	game.reset(newBot);
    });
}));

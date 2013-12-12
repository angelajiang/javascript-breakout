jQuery(document).ready(jQuery(function($) {
    init_bot = $('.botname:checked').val();
    
    $('.botname').change(function(){
	// console.log('changed');
	var newBot = $(this).val();
	// console.log(newBot);
	game.reset(newBot);
    });
}));

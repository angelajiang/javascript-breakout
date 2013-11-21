//===========================
//	Handmade Bot
//===========================

Breakout.bot = {
	initialize: function(game, cfg) {
	      this.game = game;
	      this.cfg  = cfg;
   	},
    
	
	update:function(dt){
		paddleX = this.game.paddle.getX();
		ballX = this.game.ball.getX();
        if(this.game.ball.moving){
            if(ballX > paddleX){
                this.game.paddle.stopMovingLeft();
                this.game.paddle.moveRight();
            }
            else{
                this.game.paddle.stopMovingRight();
                this.game.paddle.moveLeft();
            }
        }
        
	}
	
}
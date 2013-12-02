//===========================
//	Handmade Bot
//===========================

Breakout.bot = {
    initialize: function(game, cfg) {
	this.game = game;
	this.cfg  = cfg;
	this.minballX = 15;
	this.maxballX = 15;
	this.minballY = 15;
	this.maxballY = 15;
	this.minpaddleX = 5;
	this.maxpaddleX = 5;

    },
    
    update:function(dt){
	paddleX = this.game.paddle.getX();
	ballX = this.game.ball.getX();
        ballY = this.game.ball.getY();
        balldx = this.game.ball.getDX();
        balldy = this.game.ball.getDY();
	b = this.game.court.getBricks();
	v = this.game.ball.getVelocity();        
        if(this.game.ball.moving){
	    var p = Math.random();
	    if(p < .99){
                if(ballX+8 > paddleX+11){
                    this.game.paddle.stopMovingLeft();
                    this.game.paddle.moveRight();
                }
	        else if(ballX+8 === paddleX+11){
		    this.game.paddle.stopMovingLeft();
		    this.game.paddle.stopMovingRight();
		}
                else{
                    this.game.paddle.stopMovingRight();
                    this.game.paddle.moveLeft();
                }
            }
        }
    }
}

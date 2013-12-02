//===========================
//	Learning bot
//===========================
jQuery(document).ready(jQuery(function($) {
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
                gameObj = this.game;
                paddleX = this.game.paddle.getX();
                ballX = this.game.ball.getX();
                ballY = this.game.ball.getY();
                balldx = this.game.ball.getDX();
                balldy = this.game.ball.getDY();
	        ballV = this.game.ball.getVelocity();        
                b = this.game.court.getBricks();
                if(this.game.ball.moving){
                    $.ajax({
                      type: "POST",
                      data: {
                          'paddleX': paddleX,
                          'ballX': ballX,
                          'ballV': ballV,
                          'ballY': ballY,
                      },
                      url: "/get_move"
                    }).success(function(move) {
                        if(move == 'right'){
                            gameObj.paddle.stopMovingLeft();
                            gameObj.paddle.moveRight();
                        }
                        else if (move == 'stay'){
                            gameObj.paddle.stopMovingLeft();
                            gameObj.paddle.stopMovingRight();
                        }
                        else if (move == 'left'){
                            gameObj.paddle.stopMovingRight();
                            gameObj.paddle.moveLeft();
                        }else{
                            console.log("ballY: " + ballY + " ballV: " + ballV);
                        }
                    });
                }
            }
    }
}));

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

        loseBall: function() {
            this.get_move("lose");
        },
        winLevel: function() {
            this.get_move("win");
        },

        update: function(){
            if(this.game.ball.moving) {
                this.get_move("move");
            }
        },

        get_move: function(msgName) {
            data = this.getState();
            data.msgName = msgName;
            gameObj = this.game;
            
            $.ajax({
                type: "POST",
                data: data,
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
            })
        },
                
        getState: function() {
            paddleX = this.game.paddle.getX();
            ballX = this.game.ball.getX();
            ballY = this.game.ball.getY();
	    ballV = this.game.ball.getVelocity();        

            return {
                'paddleX': paddleX,
                'ballX': ballX,
                'ballV': ballV,
                'ballY': ballY,
            };
        }
    }
}));

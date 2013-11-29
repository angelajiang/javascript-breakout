//===========================
//	Learning bot
//===========================
jQuery(document).ready(jQuery(function($) {
    Breakout.bot = {
            initialize: function(game, cfg) {
                this.game = game;
                this.cfg  = cfg;
            },
            
            update:function(dt){
                gameObj = this.game;
                paddleX = this.game.paddle.getX();
                ballX = this.game.ball.getX();
                ballV = 1;
                if(this.game.ball.moving){
                    $.ajax({
                      type: "POST",
                      data: {
                          'paddleX': paddleX,
                          'ballX': ballX,
                          'ballV': ballV,
                      },
                      url: "/get_move"
                    }).success(function(move) {
                        if(move == 'right'){
                            gameObj.paddle.stopMovingLeft();
                            gameObj.paddle.moveRight();
                        }
                        else{
                            gameObj.paddle.stopMovingRight();
                            gameObj.paddle.moveLeft();
                        }
                    });
                }
            }
    }
}));

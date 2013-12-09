Breakout
========

To run:
1. Start server
    >> python server.py 5000
2. Reach file in browser
    http://localhost:5000/index.html

Configure server:
    Configurations found in appconfig.py
    Set environ variable $APPMODE
        "Config" - training
        "TestingConfig" - testing
        "DevConfig" - development

Persistent qTable:
    To create a table and write to filename: 
        create_table/<filename>
    Changes written to qTable when server.py gets ctrl-c. 


Another HTML5 experiment to implement BREAKOUT in a `<canvas>`

 * You can find the [game here](http://codeincomplete.com/posts/2011/6/11/javascript_breakout/demo.html)
 * You can find out [how it works](http://codeincomplete.com/posts/2011/6/11/javascript_breakout/index.html)
   * [Managing Game State](http://codeincomplete.com/posts/2011/6/12/game_state_in_breakout/)
   * [Rendering Performance](http://codeincomplete.com/posts/2011/6/12/rendering_breakout/)
   * [Collision Detection](http://codeincomplete.com/posts/2011/6/12/collision_detection_in_breakout/)
   * [Gameplay Balance](http://codeincomplete.com/posts/2011/6/13/gameplay_in_breakout/)
   * [Adding Sound](http://codeincomplete.com/posts/2011/6/16/adding_sound_to_breakout/)
   * [Touch Events](http://codeincomplete.com/posts/2011/6/24/adding_touch_to_breakout/)

# Implementation of classic arcade game Pong
# Written and run through codeskulptor.org, a web Python IDE written for
#	a Coursera.org Python course

# Follow the link below and hit run to see the program run
# http://www.codeskulptor.org/#user23_n0e07Ov7JQZktab_0.py

# Note: if the link has expired, copy this code into Codeskulptor.org and run

# Author: Kevin Jordan Wong

#Note: simplegui is a graphics module written specifically for Codeskulptor.org
import simplegui
import random

# initialize global constants
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [300,200]
    
    #start at a random velocity in a specific range
    vert = random.randrange(60, 180)/60
    horz = random.randrange(120, 240)/60
    
    #set ball velocity depending on direction
    if direction == RIGHT:
        ball_vel = [horz, vert * -1]
    else:
        ball_vel = [horz * -1, vert * -1]
    

# function: new_game()
#	Is called whenever you start a new game
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    
    score1 = 0
    score2 = 0
    
    #reset the paddles to the middle
    paddle1_pos = [0, (HEIGHT/2) - HALF_PAD_HEIGHT]
    paddle1_vel = 0
    paddle2_pos = [WIDTH - PAD_WIDTH, (HEIGHT/2) - HALF_PAD_HEIGHT]
    paddle2_vel = 0
    
    #spawn the ball in the middle going right and new game begins
    spawn_ball(RIGHT)

# function: draw
#	handler for drawing to the canvas
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball position (and velocity if it hits the top or bottom wall)
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if (ball_pos[1] - BALL_RADIUS) <= 0 or (ball_pos[1] + BALL_RADIUS) >= HEIGHT:
        ball_vel[1] *= -1
    
    #if ball hits left gutter
    if (ball_pos[0] - BALL_RADIUS) <= PAD_WIDTH:
        #if paddle is behind the ball, bounce back; else the other player scores
        if (ball_pos[1] >= paddle1_pos[1]) and (ball_pos[1] <= (paddle1_pos[1] + PAD_HEIGHT)):
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
        else:
            score2 += 1
            spawn_ball(RIGHT)
    #hits right gutter
    elif (ball_pos[0] + BALL_RADIUS) > (WIDTH - PAD_WIDTH):
        #if paddle behind the ball, bounce back: else, player1 scores a point
        if (ball_pos[1] >= paddle2_pos[1]) and (ball_pos[1] <= (paddle2_pos[1] + PAD_HEIGHT)):
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
        else:
            score1 += 1
            spawn_ball(LEFT)
            
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 2, 'White', 'White')
    
    # update paddle's vertical position while keeping paddle on the screen
    if (paddle1_pos[1] + paddle1_vel >= 0) and (paddle1_pos[1] + PAD_HEIGHT + paddle1_vel <= HEIGHT): 
        paddle1_pos[1] += paddle1_vel
    if (paddle2_pos[1] + paddle2_vel >= 0) and (paddle2_pos[1] + PAD_HEIGHT + paddle2_vel <= HEIGHT):
        paddle2_pos[1] += paddle2_vel
    
    # draw paddle1
    c.draw_polygon([
                paddle1_pos,
                (paddle1_pos[0], paddle1_pos[1] + PAD_HEIGHT),
                (paddle1_pos[0] + PAD_WIDTH, paddle1_pos[1] + PAD_HEIGHT),
                (paddle1_pos[0] + PAD_WIDTH, paddle1_pos[1]),
                paddle1_pos],
                1, "White", "White")
    
    #draw paddle2
    c.draw_polygon([
                paddle2_pos,
                (paddle2_pos[0], paddle2_pos[1] + PAD_HEIGHT),
                (paddle2_pos[0] + PAD_WIDTH, paddle2_pos[1] + PAD_HEIGHT),
                (paddle2_pos[0] + PAD_WIDTH, paddle2_pos[1]),
                paddle2_pos],
                1, "White", "White")
    
    # draw scores
    c.draw_text(str(score1), (150, 60), 40, 'White')
    c.draw_text(str(score2), (450, 60), 40, 'White')

# function: keydown
#	Event handler for when a key is pressed down (move paddles up and down)	
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    #paddle 1    
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= 3
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel += 3
    
    #paddle 2
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= 3
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel += 3

#function: keyup
#	Event handler for when you let go of a key (stop the paddle from moving)		
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    #paddle 1    
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    
    #paddle 2
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

# function: reset
#	Event handler for the reset button (just starts a new game)
def reset():
    new_game()

# create frame and declare control elements
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
reset_button = frame.add_button('Restart', reset, 100)

# start frame and start a new game
new_game()
frame.start()

# Implementation of Asteroids (Called RiceRocks from the coursera.org Python course)
# Author: Kevin Jordan Wong
#	with some starter code given through Python programming course on coursera.org

# Written and run through codeskulptor.org, a web Python IDE written for
#	a Coursera.org Python course

# Follow the link below and hit run to see the program run
# http://www.codeskulptor.org/#user27_ph0QtLNgMybdpUu.py

# Note: if the link has expired, copy this code into Codeskulptor.org and run

#Note: simplegui is a graphics module written specifically for Codeskulptor.org
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 0
time = 0.5
max_rocks = 7
started = False
acc_constant = 0.03
friction_constant = 0.05

# Class: ImageInfo
#	Each image in the project corresponds to an ImageInfo object and
#	contains useful information about each image
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    # Method: get_center
    #	Returns the center point of the image
    def get_center(self):
        return self.center

    # Method: get_size
    #	Returns the size of the image
    def get_size(self):
        return self.size

    # Method: get_radius
    #	Returns the radius of the actual image
    def get_radius(self):
        return self.radius

    # Method: get_liftspan
    #	(Optional) the length/lifespan of the image(for tiled images)
    def get_lifespan(self):
        return self.lifespan

    # Method: get_animated
    #	Returns true if image is supposed to be animated
    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack.set_volume(.5)
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound.set_volume(.5)
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
explosion_sound.set_volume(.5)

#-----------------------------------------------------
# Helper Functions
#-----------------------------------------------------
# Function: reset_game
#	Helper function to initializes a new game
def reset_game():
    global lives, score, started, my_ship
    score = 0
    lives = 3
    started = True
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    soundtrack.rewind()
    soundtrack.play()

# Function: angle_to_vector
#	Helper function that converts and angle (in rad) to a vector
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

# Function: dist
#	Helper function to calculate the distance between 2 points
def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Function: process_sprite_group
#	Draws and updates the position & velocity of every sprite in a set
def process_sprite_group(sprite_set, canvas):
    temp_set = set(sprite_set)
    for s in temp_set:
        s.draw(canvas)
        #if the age >= lifespan (for missiles), remove missile
        if s.update() == True:
            sprite_set.remove(s)

# Function: group collide
#	Helper function that determines if the object collides with any sprites in the given group
#	Returns true if a collision happens
def group_collide(group, other_object):
    temp_group = set(group)
    for s in temp_group:
        if s.collide(other_object):
            group.remove(s)
            explosion = Sprite(s.get_pos(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
            return True
    return False

# Function: group_group_collide
#	Helper function that determines if any objects in group 1 collide with any objects in group 2
#	Returns the number of collisions that occur between the 2 groups
def group_group_collide(group1, group2):
    total_collided = 0
    temp_group1 = set(group1)
    for s in temp_group1:
        if group_collide(group2, s) == True:
            total_collided += 1
            group1.discard(s)
    return total_collided
        

#-----------------------------------------------------
# Classes (excluding ImageInfo class)
#-----------------------------------------------------
# Class: Ship
#	This class represents the spaceship
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    # Method: draw
    #    Draws the spaceship, depending on whether or not the thrust is on
    def draw(self,canvas):
        if self.thrust == True:
            canvas.draw_image(ship_image, [self.image_center[0] + 90, self.image_center[1]], self.image_size ,self.pos ,self.image_size ,self.angle)
        else:
            canvas.draw_image(ship_image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    # Method: update
    #	Updates the position, angle and velocity of the ship
    def update(self):
        vec = angle_to_vector(self.angle)
        self.angle += self.angle_vel
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        self.vel[0] *= (1 - friction_constant)
        self.vel[1] *= (1 - friction_constant)
        
        if self.thrust == True:
            self.vel[0] += vec[0] * 0.5
            self.vel[1] += vec[1] * 0.5
    
    # Method: get_pos
    #	Returns the position of the ship
    def get_pos(self):
        return self.pos
    
    # Method: get_radius
    #	Returns the radius of the ship (from the image)
    def get_radius(self):
        return self.radius
    
    # Method: change_ang_vel
    #	Changes the angular velocity of the ship
    def change_ang_vel(self,vel):
        self.angle_vel = vel
    
    # Method: change_thrust
    #	Sets the ship's thrust to either True or False
    def change_thrust(self, t, sound = None):
        self.thrust = t
        if sound:
            sound.play()
    
    # Method: shoot
    #	Shoots a missile from the tip of the ship
    def shoot(self):
        global missile_group
        vel_constant = 7
        
        vec = angle_to_vector(self.angle)
        pos = [self.pos[0] + self.radius * vec[0], self.pos[1] + self.radius * vec[1]]
        vel = [self.vel[0] + vel_constant * vec[0], self.vel[1] + vel_constant * vec[1]]
        
        a_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    

# Class: Sprite
#	Generic class that can have objects of asteroids, missiles or explosions
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    # Method: get_pos
    #	Returns the position of the sprite
    def get_pos(self):
        return self.pos
    
    # Method: get_radius
    #	Returns the radius of the object
    def get_radius(self):
        return self.radius
    
    # Method: draw
    #	Draws the object's image on the canvas
    #	The condition checking animation applies only to the explosion (multiple images)
    def draw(self, canvas):
        if self.animated == True:
            center = self.image_center
            size = self.image_size
            canvas.draw_image(self.image,[center[0]+self.age*size[0],center[1]],self.image_size,self.pos,self.image_size)
        else:
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
    
    # Method: update
    #	Updates the sprite's current position, angle and age
    def update(self):
        self.angle += self.angle_vel
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        self.age += 1
        if self.age >= self.lifespan:
            return True
        else:
            return False
    
    # Method: collide
    #	Determines if the current object collides with a given object
    def collide(self, other_object):
        dist_between = dist(self.pos, other_object.get_pos())
        if dist_between <= self.radius + other_object.get_radius():
            return True
        else:
            return False


#-----------------------------------------------------
# GUI Handlers
#-----------------------------------------------------
# Function: draw
#	The draw handler to draw to the canvas
def draw(canvas):
    global time, lives, score, started
    global rock_group
    
    # animiated background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    #update all objects
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    my_ship.draw(canvas)
    my_ship.update()
    
    #check collisions
    score += group_group_collide(missile_group, rock_group)
    if group_collide(rock_group, my_ship) == True:
        lives -= 1
    #if lives run out, stop the game, and reset the group of asteroids
    if lives <= 0:
        started = False
        rock_group = set()
    #if the game has not started yet, draw the image depicting rice rocks
    if started == False:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
    
    #write out lives and score
    canvas.draw_text("Lives: " + str(lives), [50, 50], 20, 'White')
    canvas.draw_text("Score: " + str(score), [600, 50], 20, 'White')
    
    
# Function: rock_spawner
#	The timer handler
#	Will spawn a new random rock every second
#	Caps the number of rocks to the global var max_rocks
def rock_spawner():
    global rock_group
    
    #do not spawn rocks if the game has not begun
    if started == False:
        return
    
    #determine random position
    pos = [random.randrange(0, WIDTH),random.randrange(0, HEIGHT)]
    
    #determine a random velocity between -2 and 2 pix/sec
    rand_hor = random.random() * 4 - 2
    rand_ver = random.random() * 4 - 2
    vel = [rand_hor,rand_ver]
    
    #determines a random angular velocity between -0.2 and 0.2 rad/sec
    rand = random.random() * 0.4 - 0.2
    angle_vel = rand
    
    a_rock = Sprite(pos, vel, 0, angle_vel, asteroid_image, asteroid_info)
    #only spawn rock if the number of current rocks is not above the max number AND
    #only if the rock's position is not near the ship (don't want rocks spawning on top of the ship)
    if (len(rock_group) < max_rocks) and dist(a_rock.get_pos(),my_ship.get_pos()) > 200:
        rock_group.add(a_rock)

        
# Function: keydown
#	Handler for when a key is pressed down
def keydown(key):
    if key==simplegui.KEY_MAP["right"]:
        my_ship.change_ang_vel(0.1)
        
    if key==simplegui.KEY_MAP["left"]:
        my_ship.change_ang_vel(-0.1)
        
    if key==simplegui.KEY_MAP["up"]:
        my_ship.change_thrust(True, ship_thrust_sound)
        
    if key==simplegui.KEY_MAP["space"]:
        my_ship.shoot()

        
# Function: keyup
#	Handler for when a key is released
def keyup(key):
    if key==simplegui.KEY_MAP["right"] or key==simplegui.KEY_MAP["left"]:
        my_ship.change_ang_vel(0)
        
    if key==simplegui.KEY_MAP["up"]:
        my_ship.change_thrust(False)
        ship_thrust_sound.rewind()

        
# Function: mouse_handler
#	if a game has not started yet, allow to the user to click (which starts the game)
def mouse_handler(position):
    if started == False:
        reset_game()

        
#-----------------------------------------------------
# Initializing the GUI and the game
#-----------------------------------------------------
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and the groups of objects
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouse_handler)
timer = simplegui.create_timer(1000.0, rock_spawner)

# start the game!
timer.start()
frame.start()

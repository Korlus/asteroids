import pygame
import math
import random

SCREEN_WIDTH = 640     # For demo mode, this will suffice
SCREEN_HEIGHT = 480
CENTRE_X = SCREEN_WIDTH / 2  # Centre of our screen, which for our demo also
CENTRE_Y = SCREEN_HEIGHT / 2 # represents the centre of any object
WHITE = (255,255,255)  # A couple of tuples for colour constants
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
MEDIUMGREY = (127,127,127)
BUTTON_WIDTH = 120     # For the buttons
BUTTON_HEIGHT = 38
ARBITRARY_BORDER = 2   # How many pixels a button needs to be away from the screen

# Set up PyGame
pygame.init()

# Establish the screen variables
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Set up that all-important surface
blank_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))   # A blank surface, so I can do my lazy blitting later

# Set up fonts
pygame.font.init()
demofont_size = 16
demofont = pygame.font.Font(None, demofont_size)

# Variables used for the demo itself
state = "main"      # Very simple state definition - main for running, quit for not
angle = 0           # The angle at which the drawn object is rotated
obj_handled = 0     # Which of the game's objects is currently being drawn
max_handled = 2     # How many objects are defined in the game
rotating = False    # Is auto-rotating enabled?
followmouse = False # Is the rotation based on where the mouse is?
mouse_angle = 0
showgrey = True     # Should the grey construction lines be shown?
size_adjust = 100   # Percentage for the size of the object, adjusted for display

# I think reading the Learning Python book is rubbing off on me... here's a
# nested list of dictionaries with nested lists, not a single array in sight!
# Also, I challenge you to say "nested list of dictionaries with nested
# lists" three times fast.

game_obj = [{'num_plots': 4,  # First object - a ship, with 4 points
             'plot_len':[40, 40, 10, 40],
             'plot_ang':[0, 130, 180, 230],
             'size':100},
            {'num_plots': 8,  # Second object - an asteroid with 8 points
             'plot_len':[38, 45, 34, 37, 42, 38, 49, 33],
             'plot_ang':[0, 45, 90, 135, 180, 225, 270, 315],
             'size':100},
            {'num_plots': 8,  # Third object - a large random asteroid with 8 points
             'plot_len':[60+random.randrange(0, 10), 60+random.randrange(0, 10), 60+random.randrange(0, 10), 60+random.randrange(0, 10), 60+random.randrange(0, 10), 60+random.randrange(0, 10), 60+random.randrange(0, 10), 60+random.randrange(0, 10)],
             'plot_ang':[0+random.randrange(-10, 11), 45+random.randrange(-10, 11), 90+random.randrange(-10, 11), 135+random.randrange(-10, 11),
                         180+random.randrange(-10, 11), 225++random.randrange(-10, 11), 270++random.randrange(-10, 11), 315++random.randrange(-10, 11)],
             'size':100}
            ]

for i in range(0, 10):  # Add 10 more objects on to the end
    rand_num_plots = random.randrange(6, 15) # Let's have between 6 and 14 points per asteroid
    rand_plot_len = []  # We're using these variables to temporarily set up random attributes to give to the asteroids
    rand_plot_ang = []  # This could, theoretically, be done in less code, but it's spaced out for readability
    angle_divisions = 360 / rand_num_plots  # Let's divide the plots equally, depending on how many there are
    asteroid_standard_size = 30  # This is the standard size of an asteroid -- put here for now, but should be elsewhere in the future
    for j in range (0, rand_num_plots):  # Generate the random goodness for each plot
        rand_plot_len.append(asteroid_standard_size + random.randrange(0, (asteroid_standard_size / 3) + 1)) # Asteroids can vary up to a third of their size
        rand_plot_ang.append((angle_divisions*j) + random.randrange(-10, 11)) # Up to 10 degrees difference either way
    game_obj.append({'num_plots': rand_num_plots, 'plot_len':rand_plot_len, 'plot_ang':rand_plot_ang, 'size':100}) # Finally, put it all in the existing data structure
    max_handled += 1  # Increment how many objects are being handled by the system

draw_obj = {'x':[], 'y':[]}   # I can't help declaring variables sometimes

# Buttons for the interface
# -- Turns out there was a much better way to do this... as seen below!  So much less repetition of code
button = []
num_buttons = 6  # This could be determined elsewhere, but is here for convenience
for i in range(0, num_buttons):
    button.append({'x': SCREEN_WIDTH - BUTTON_WIDTH - ARBITRARY_BORDER,
                   'y': ARBITRARY_BORDER + ((BUTTON_HEIGHT+ARBITRARY_BORDER) * i),
                   'width': BUTTON_WIDTH, 'height': BUTTON_HEIGHT,  # Added these two so all buttons don't HAVE to be uniform... as we see below
                   'label': 'blank'})
button[0]['label'] = 'AUTO-ROTATION'
button[1]['label'] = 'MOUSE ROTATION'
button[2]['label'] = 'GREY LINES'
button[3]['label'] = 'OBJECT'
button[4]['label'] = '- SIZE'
button[5]['label'] = '+ SIZE'
button[4]['width'] = button[5]['width'] = (BUTTON_WIDTH / 2) - 1  # A strange bit of coding, but it works
button[5]['x'] = SCREEN_WIDTH - (BUTTON_WIDTH / 2) - ARBITRARY_BORDER + 1
button[5]['y'] = ARBITRARY_BORDER + ((BUTTON_HEIGHT+ARBITRARY_BORDER) * 4)

while state == "main":

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = "quit"

    mousex, mousey = pygame.mouse.get_pos() # Gets mouse x and y
    if mousex-CENTRE_X <> 0:
        cordx = mousex - CENTRE_X
        cordy = mousey - CENTRE_Y
        mouse_angle = math.degrees(math.atan((cordy)/float(cordx)))
        # The following is to make up for a mistake in how the angle is
        # calculated -- I have no idea why it's happening, but it's
        # probably down to my faulty maths skills and I used the wrong
        # trigonometric function or something... meh, it works like this
        if cordx < 0:
            mouse_angle = mouse_angle - 90
        else:
            mouse_angle = mouse_angle + 90
    if followmouse: angle = mouse_angle

    if (event.type == pygame.MOUSEBUTTONDOWN):
        buttonpressed = -1  # The typical nothing has happened state
        j = 0
        for i in button:
            if mousex>=i['x'] and mousex<i['x']+i['width'] and mousey>=i['y'] and mousey<i['y']+i['height']:
                buttonpressed = j
            j = j + 1   # There has to be a better way of finding out how many times we've gone through a loop than this...
        if buttonpressed == 0:
            rotating = not rotating
            followmouse = False
        if buttonpressed == 1:
            followmouse = not followmouse
            rotating = False
        if buttonpressed == 2:
            showgrey = not showgrey
        if buttonpressed == 3:
            obj_handled = obj_handled + 1
            if obj_handled > max_handled:
                obj_handled = 0
        if buttonpressed == 4:
            size_adjust -= 10  # New decrement technique
            if size_adjust < 0:
                size_adjust = 0
        if buttonpressed == 5:
            size_adjust += 10  # New increment technique
        if buttonpressed > -1:
            pygame.time.delay(200)    # Delay a bit just to give the processor a chance
            buttonpressed = -1        # Return to no action state
    
    draw_position = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.blit(blank_surface, draw_position)  # Very lazy way of clearing screen

    # Time to work out what to draw
    draw_obj = {'x':[], 'y':[]}
    for i in range(0, game_obj[obj_handled]['num_plots']):  # Python almost definitely has a more elegant way of handling this, but I don't care :P~~~
        draw_obj['x'].append(int(math.sin(math.radians(game_obj[obj_handled]['plot_ang'][i]+angle))*(game_obj[obj_handled]['plot_len'][i])*size_adjust/100))
        draw_obj['y'].append(int(math.cos(math.radians(game_obj[obj_handled]['plot_ang'][i]+angle))*(game_obj[obj_handled]['plot_len'][i])*size_adjust/100))

    # Now to actually draw it!
    if showgrey: # This just draws in the grey-lined framework
        for i in range(0, game_obj[obj_handled]['num_plots']):
            pygame.draw.aaline(screen, MEDIUMGREY, (CENTRE_X, CENTRE_Y), (CENTRE_X+draw_obj['x'][i], CENTRE_Y-draw_obj['y'][i]), 1)
    for i in range(0, game_obj[obj_handled]['num_plots']): # This draws the green object itself
        j = (i + 1) % game_obj[obj_handled]['num_plots']   # j is one more than i, but loop back to 0 to close object
        pygame.draw.aaline(screen, GREEN, (CENTRE_X+draw_obj['x'][i], CENTRE_Y-draw_obj['y'][i]), (CENTRE_X+draw_obj['x'][j], CENTRE_Y-draw_obj['y'][j]), 1)
        
    # Draw buttons
    j = 0
    for i in button:
        pygame.draw.rect(screen, GREEN, (i['x'], i['y'], i['width'], i['height']), 1)
        text = demofont.render(i['label'], 1, GREEN)
        screen.blit(text,(i['x']+5, i['y']+5))
        if j == 0:
            if rotating: text = demofont.render('ON', 1, WHITE)
            else: text = demofont.render('OFF', 1, RED)
            screen.blit(text,(i['x']+5, i['y']+demofont_size+5))
        if j == 1:
            if followmouse: text = demofont.render('ON', 1, WHITE)
            else: text = demofont.render('OFF', 1, RED)
            screen.blit(text,(i['x']+5, i['y']+demofont_size+5))
        if j == 2:
            if showgrey: text = demofont.render('ON', 1, WHITE)
            else: text = demofont.render('OFF', 1, RED)
            screen.blit(text,(i['x']+5, i['y']+demofont_size+5))
        if j == 3:
            text = demofont.render(str(obj_handled), 1, WHITE)
            screen.blit(text,(i['x']+5, i['y']+demofont_size+5))
        if j == 4:
            text = demofont.render(str(size_adjust), 1, WHITE)
            screen.blit(text,(i['x']+5, i['y']+demofont_size+5))
        j = j + 1
    
    if rotating: angle = angle + 1
    
    pygame.display.update()   # Update display
    pygame.time.delay(10)     # Delay by 10/1000th just to give the processor a chance

pygame.quit()  # For clean exit
#sys.exit()     # Not really using the sys module yet, but here for later

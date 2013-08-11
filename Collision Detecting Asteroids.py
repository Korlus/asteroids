import pygame
import math

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
ARBITRARY_BORDER = 2   # How many pixels a button needs to be away from the
  		# screen

# Set up PyGame
pygame.init()

# Establish the screen variables
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Set up that all-important surface
blank_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
# A blank surface, so I can do my lazy blitting later

# Set up fonts
pygame.font.init()
demofont_size = 16
demofont = pygame.font.Font(None, demofont_size)

# Variables used for the demo itself
state = "main"      # Very simple state definition - main for running, quit
                    # for not
angle = 0           # The angle at which the drawn object is rotated
obj_handled = 0     # Which of the game's objects is currently being drawn
max_handled = 1     # How many objects are defined in the game
rotating = False    # Is auto-rotating enabled?
followmouse = False # Is the rotation based on where the mouse is?
mouse_angle = 0
showgrey = True     # Should the grey construction lines be shown?

# I think reading the Learning Python book is rubbing off on me... here's a
# nested list of dictionaries with nested lists, not a single array in
# sight!
# Also, I challenge you to say "nested list of dictionaries with nested
# lists" three times fast.

game_obj = [{'num_plots': 4,  # First object - a ship, with 4 points
             'plot_len':[40, 40, 10, 40],
             'plot_ang':[0, 130, 180, 230]},
            {'num_plots': 8,  # Second object - an asteroid with 8 points
             'plot_len':[38, 45, 34, 37, 42, 38, 49, 33],  # Later, this can
# easily be randomly generated
             'plot_ang':[0, 45, 90, 135, 180, 225, 270, 315]} # Likewise
            ]
draw_obj = {'x':[], 'y':[]}   # I can't help declaring variables sometimes

# Buttons for the interface
button = [{'x': SCREEN_WIDTH - BUTTON_WIDTH - ARBITRARY_BORDER,  # There's
# got to be some clever way of doing this with a for statement, but this will
# do for now
           'y': ARBITRARY_BORDER + ((BUTTON_HEIGHT+ARBITRARY_BORDER) * 0),
           'label': 'AUTO-ROTATION'},
          {'x': SCREEN_WIDTH - BUTTON_WIDTH - ARBITRARY_BORDER,
           'y': ARBITRARY_BORDER + ((BUTTON_HEIGHT+ARBITRARY_BORDER) * 1),
           'label': 'MOUSE ROTATION'},
          {'x': SCREEN_WIDTH - BUTTON_WIDTH - ARBITRARY_BORDER,
           'y': ARBITRARY_BORDER + ((BUTTON_HEIGHT+ARBITRARY_BORDER) * 2),
           'label': 'GREY LINES'},
          {'x': SCREEN_WIDTH - BUTTON_WIDTH - ARBITRARY_BORDER,
           'y': ARBITRARY_BORDER + ((BUTTON_HEIGHT+ARBITRARY_BORDER) * 3),
           'label': 'OBJECT'}
          ]

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
    if followmouse:
        angle = mouse_angle

    if (event.type == pygame.MOUSEBUTTONDOWN):
        buttonpressed = -1  # The typical nothing has happened state
        j = 0
        for i in button:
            if mousex>=i['x'] and mousex<i['x']+BUTTON_WIDTH and mousey>=i['y'] and mousey<i['y']+BUTTON_HEIGHT:
                buttonpressed = j
            j = j + 1   # There has to be a better way of finding out how
                        # many times we've gone through a loop than this...
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
        if buttonpressed > -1:
            pygame.time.delay(200)  # Delay a bit just to give the
                                    # processor a chance
            buttonpressed = -1      # Return to no action state


    draw_position = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.blit(blank_surface, draw_position)   # Very lazy way of clearing
                                                # screen

    # Time to work out what to draw
    draw_obj = {'x':[], 'y':[]}
    for i in range(0, game_obj[obj_handled]['num_plots']):  # Python almost
# definitely has a more elegant way of handling this, but I don't care :P~~~
        draw_obj['x'].append(int(math.sin(math.radians(game_obj[obj_handled]
['plot_ang'][i]+angle))*(game_obj[obj_handled]['plot_len'][i])))
        draw_obj['y'].append(int(math.cos(math.radians(game_obj[obj_handled]
['plot_ang'][i]+angle))*(game_obj[obj_handled]['plot_len'][i])))

    # Now to actually draw it!
    if showgrey: # This just draws in the grey-lined framework
        for i in range(0, game_obj[obj_handled]['num_plots']):
            pygame.draw.aaline(screen, MEDIUMGREY, (CENTRE_X, CENTRE_Y),
                            (CENTRE_X+draw_obj['x'][i], CENTRE_Y-draw_obj['y'][i]), 1)
    for i in range(0, game_obj[obj_handled]['num_plots']): # This draws the
                                                            # green object itself
        j = (i + 1) % game_obj[obj_handled]['num_plots']   # j is one more
                                # than i, but loop back to 0 to close object
        pygame.draw.aaline(screen, GREEN, (CENTRE_X+draw_obj['x'][i],
                            CENTRE_Y-draw_obj['y'][i]), (CENTRE_X+draw_obj['x'][j],
                            CENTRE_Y-draw_obj['y'][j]), 1)




##################################################################################################################
##################################################################################################################
##################################################################################################################
    ERROR_WIDTH = 3 # Sets basic error width for collisions to be detected. Ought to go at top when...
                    # ... Actually putting code together.

    # Trying Basic Collision Detection:
    ###################################
    # Extract points to make list of absolute coordinates by adding the central point:
    obj_points = []
    for i in range(0, len(draw_obj["x"])): # Assuming the same number of points in draw_obj["y"] and "x".
        obj_points.append((draw_obj["x"][i] + CENTRE_X, # Will need to change CENTRE_X to
                           draw_obj["y"][i] + CENTRE_Y)) # Object's central point later.


    # Test script to extract point and the next point along, for later comparison.
    for i in range(1, len(obj_points)+1):  # Ross note - I changed this from 0 to len(obj_points) to one more... must check if that's what was intended
        point1 = obj_points[i - 1]

        if i < len(obj_points):
            point2 = obj_points[i]
        elif i == len(obj_points):       # Elif statement to cause it to link first and last points together.
            point2 = obj_points[0]
        else:                           # Else statement to catch unforseen errors.
            print """
                Something went wrong in collision detection.
                I can't seem to find the right number of points for the object.
                """

        # Using y = (m*x) + c; derive object gradient and intersect (m and c):
        NON_ZERO_DIVISOR = float(point2[0]) - point1[0]
        if NON_ZERO_DIVISOR == 0:
            NON_ZERO_DIVISOR = 0.0000000000000000000000000001 # This stops dividing by zero errors.
                                 
        OBJ_GRAD = ( float(point2[1]) - point1[1] ) / NON_ZERO_DIVISOR
        OBJ_INTERSECT = point2[1] - (OBJ_GRAD * point2[0])

        
        mouse_test = 0 # Variable set up to track if it fulfils all conditions (messy and should be got rid of).


        # Then test if mouse is within 3 pixels of a line:
        if mousey + ERROR_WIDTH >= mousex * OBJ_GRAD + OBJ_INTERSECT and \
           mousey - ERROR_WIDTH <= mousex * OBJ_GRAD + OBJ_INTERSECT:
                mouse_test = mouse_test + 1
                #print "Line detected"

                # detect if within x bounds of line:
                if point1[0] >= point2[0]: # Tests to see which number is largest and then sets bounds.
                    if mousex + ERROR_WIDTH >= point2[0] and \
                       mousex - ERROR_WIDTH <= point1[0]:
                            mouse_test = mouse_test + 1
                            #print "x detected 1"
                elif point1[0] < point2[0]: # Then checks to see if mouse pointer is within them.
                    if mousex - ERROR_WIDTH <= point2[0] and \
                       mousex + ERROR_WIDTH >= point1[0]:
                            mouse_test = mouse_test + 1
                            #print "x detected 2"
                else:
                    print "Error in detecting mouse placement (x)"

                # Detect if within y bounds of line:
                if point1[1] >= point2[1]: # Tests to see which number is largest and then sets bounds.
                    if mousey + ERROR_WIDTH >= point2[1] and \
                       mousey - ERROR_WIDTH <= point1[1]:
                            mouse_test = mouse_test + 1
                            #print "y detected 1"
                elif point1[1] < point2[1]: # Then checks to see if mouse pointer is within them.
                    if mousey - ERROR_WIDTH <= point2[1] and \
                       mousey + ERROR_WIDTH >= point1[1]:
                            mouse_test = mouse_test + 1
                            #print "y detected 2"
                else:
                    print "Error in detecting mouse placement (y)"

        if mouse_test == 3:
            # print "Collision Detected"
            text = demofont.render('Collision Detected', 1, RED)
        else:
            text = demofont.render('No collision', 1, WHITE)

        screen.blit(text,(5, 16*i + 5))

##################################################################################################################
##################################################################################################################
##################################################################################################################




    # Draw buttons
    j = 0
    for i in button:
        pygame.draw.rect(screen, GREEN, (i['x'], i['y'], BUTTON_WIDTH,
BUTTON_HEIGHT), 1)
        text = demofont.render(i['label'], 1, GREEN)
        screen.blit(text,(i['x']+5, i['y']+5))
        if j == 0:   # Dirty coding, but functional
            if rotating:
                text = demofont.render('ON', 1, WHITE)
            else:
                text = demofont.render('OFF', 1, RED)
            screen.blit(text,(i['x']+5, i['y']+demofont_size+5))
        if j == 1:   # Dirty coding, but functional
            if followmouse:
                text = demofont.render('ON', 1, WHITE)
            else:
                text = demofont.render('OFF', 1, RED)
            screen.blit(text,(i['x']+5, i['y']+demofont_size+5))
        if j == 2:   # Dirty coding, but functional
            if showgrey:
                text = demofont.render('ON', 1, WHITE)
            else:
                text = demofont.render('OFF', 1, RED)
            screen.blit(text,(i['x']+5, i['y']+demofont_size+5))
        if j == 3:   # Dirty coding, but functional
            text = demofont.render(str(obj_handled), 1, WHITE)
            screen.blit(text,(i['x']+5, i['y']+demofont_size+5))
        j = j + 1

    if rotating:
        angle = angle + 1

    pygame.display.update()   # Update display
    pygame.time.delay(10)     # Delay by 10/1000th just to give the
# processor a chance

pygame.quit()  # For clean exit
#sys.exit()     # Not really using the sys module yet, but here for later

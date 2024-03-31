import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg 
from processing import *

TITLE = 'Multi-base calculator'
win_width = 700
win_height = 250
FPS = 30
font = 'cambria'

GREY = (60, 60, 60)     
WHITE = (255, 255, 255)
GREEN = (0, 255, 50)
BLUE = (0, 0, 255)
LIGHT_BLUE = (60, 220, 240)

def draw_text(text, size, x, y, colour=WHITE, draw_from='TL', fill_colour=None, outline_colour=None, thickness=0, button=True):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, colour) #True here = anti-aliasing on: blurs edges to make diag lines look normal
    #an extra arg can be used for bgd colour here^

    text_rect = text_surface.get_rect()
    if draw_from == 'TL': #topleft
        text_rect.topleft = (x+5, y-1) #adjustments for chosen font and sets which corner or centre is where
    elif draw_from == 'TR': #topright
        text_rect.topright = (x-4, y-1)
    elif draw_from == 'BL': #bottom left
        text_rect.bottomleft = (x+4, y+1)
    elif draw_from == 'BR': #bottom right
        text_rect.bottomright = (x-4, y+1)
    elif draw_from == 'CR': #centre
        text_rect.center = (x,y)

    if fill_colour: #setting and drawing rect for textbox background
        fill_rect = pg.Rect(text_rect.x -4, text_rect.y +2, text_rect.w +8, text_rect.h -1)
        pg.draw.rect(win, fill_colour, fill_rect, 0)

    if outline_colour: #for drawing an outline for textbox if u want
        outline_rect = pg.Rect(text_rect.x -4, text_rect.y +2, text_rect.w +8, text_rect.h +1)
        pg.draw.rect(win, outline_colour, outline_rect, thickness)

    win.blit(text_surface, text_rect)
    if button:
        return fill_rect
    
def check_button(rect): #function to check if button is pressed
    left, middle, right = pg.mouse.get_pressed()
    if left:
        mpos = pg.mouse.get_pos() #getting mouse position
        if rect.collidepoint(mpos[0], mpos[1]): #checking if mouse position collides with button rect
            return True #return result
        else:
            return False

def draw_main_menu():
    rect1 = draw_text('  Convert  ', 32, 0, 0, BLUE, 'TL', main_fills[0], BLUE, 3)
    rect2 = draw_text('Add', 32, rect1.right + 4, 0, BLUE, 'TL', main_fills[1], BLUE, 3)
    rect3 = draw_text('Subtract', 32, rect2.right + 4, 0, BLUE, 'TL', main_fills[2], BLUE, 3)
    return [rect1, rect2, rect3]

def draw_input_base_menu():
    rect_list = []
    y2add = 70 #this sets the distance vertical to leave between the buttons
    for i in range(5):
        rect = draw_text(conversions_display[i], 26, 0, y2add+2, BLUE, 'TL', input_base_fills[i], BLUE, 2)
        y2add = rect.bottom
        rect_list.append(rect) #adds each rect to a list to be returned
    return rect_list

def draw_output_base_menu():
    rect_list = []
    y2add = 70 #this sets the distance vertical to leave between the buttons
    for i in range(5):
        rect = draw_text(conversions_display[i], 26, button_rects2[1].right+2, y2add+2, BLUE, 'TL', output_base_fills[i], BLUE, 2)
        y2add = rect.bottom 
        rect_list.append(rect) #adds each rect to a list to be returned
    return rect_list

def draw_binary_options():
    rect_list = []
    rect = draw_text('Sign-Magnitude', 26, win_width, 10, BLUE, 'TR', binary_option_fills[0], BLUE, 2)
    rect_list.append(rect) #adds rect to a list to be returned
    rect2 = draw_text("2's Complement", 26, win_width, rect.bottom+2, BLUE, 'TR', binary_option_fills[1], BLUE, 2)
    rect_list.append(rect2)
    return rect_list


def check_change(which_menu, pressed):
    for i in range(len(all_fills[which_menu])): #for each item in a certain menu
        all_fills[which_menu][i] = LIGHT_BLUE #sets all buttons to not pressed colour
        if pressed[i]:
            choice = i
            all_fills[which_menu][i] = GREEN #sets any that are pressed to pressed colour
    return choice

#--------setting up---------
pg.init()
win = pg.display.set_mode((win_width,win_height))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

font_name = pg.font.match_font(font)

#------------------defining buttons -------------#
main_fills = [GREEN, LIGHT_BLUE, LIGHT_BLUE] #decides which options start off selected in terms of appearance
input_base_fills = [GREEN, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE]
output_base_fills = [LIGHT_BLUE, GREEN, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE]
binary_option_fills = [GREEN, LIGHT_BLUE]

all_fills = [main_fills, input_base_fills, output_base_fills, binary_option_fills]
#spacing is so it looks same size buttons in menu
conversions_display = ['  Binary   ', '  Denary  ', '     Hex     ', '    Octal    ', '    BCD     '] 

button_rects1 = draw_main_menu() #these are called once before main loop to define the button rects
button_rects2 = draw_input_base_menu()
button_rects3 = draw_output_base_menu()
button_rects4 = draw_binary_options()

choice1 = old_choice1 = choice2 = old_choice2 = choice4 = old_choice4 = 0
choice3 = old_choice3 = 1 

key_press = ''
current_data = ''
last_delete = pg.time.get_ticks()
delete_fast = False
delete_wait = 300
input_length = 22                                                                                         
valid_chars = ['a','b','c','d','e','f', 'space']

first_num = None
enter = False
previous_choice3 = 1  
previous_choice4 = 0
show_result = False
show_invalid = False
invalid_length = 2500
result_length = 26
result_x = 462

#--------------------------------- Main Program -------------------------------------#
running = True
while running:
    win.fill(GREY)
    now = pg.time.get_ticks() #get current time
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        if event.type == pg.KEYDOWN: #allows user to close window with shortcut LALT + Q
            if event.key == pg.K_q and pg.key.get_mods() & pg.KMOD_LALT:
                running = False

            key_press = pg.key.name(event.key) #get name of key input
            try:
                int(key_press)

            # if its not a number perform extra checks
            except ValueError:
                # allow minus sign if its the first character for denary to binary
                if not (key_press == '-' and len(current_data)==0  and  choice2==1 and choice3==0):
                    # set flag for submitting data if its enter
                    if key_press == 'return':
                        enter = True
                    # clear input if invalid
                    if key_press not in valid_chars:
                        key_press = ''
                # convert space to input into a actual space
                if key_press == 'space':
                    key_press = ' '

            current_data += key_press
        
        if event.type == pg.KEYUP:
            if event.key == pg.K_BACKSPACE: #so can check if backspace is held
                 delete_fast = False
    
    keys = pg.key.get_pressed()
    delete = False
    if keys[pg.K_BACKSPACE]: #check if they are pressing delete as important if its held
        delete = True
        
    if delete: #allows smooth delete
        if now - last_delete > delete_wait: #checks if enough time has passed to allow delete
            last_delete = pg.time.get_ticks()
            current_data = current_data[:-1] #removes 1 char from current data
            
            if delete_fast: #if deleting fast
                if delete_wait > 1: #,but not too fast:
                    delete_wait = int(delete_wait *0.8) #reduce min wait time to next delete     
            else: #if they lifted backspace
                    delete_wait = 140 #second delete in a row has longer wait
                    delete_fast = True #then wait gets shorter
    
    display_data = current_data   #sets limit on how much of the entered text is displayed
    if current_data == '':
        display_data = 'Enter a '+ conversions[choice2]+ ' number'
            
    if len(current_data) > input_length:
        display_data = current_data[len(current_data)-input_length:]
        
    #---------------------------primary part of main loop--------------------------#

    if enter and current_data != '': #-----if they press enter-----#
        mode_arg = None
        if choice4 != None:
            mode_arg = str(choice4+1)
            
        if choice1 == 0: #if converting
            valid, result, negative_string = convert(choice2+1, choice3+1, current_data, mode_arg)
            if not valid:
                show_result = False
                show_invalid = True
                start_invalid = pg.time.get_ticks()
            else:                                   #if the input was valid
                show_result = True
                show_invalid = False
                display_base = choice3
        else:                               #if adding/ subtracting
            if first_num:                           #if already entered the first num
                valid, result, negative_string = add(choice1+1, choice2+1, first_num, current_data, mode_arg)
                if not valid:
                    show_result = False
                    show_invalid = True
                    start_invalid = pg.time.get_ticks()
                else:
                    show_result = True
                    show_invalid = False
                    display_base = choice2
                first_num = None
            else:                                       #if this is the first num set it and wait for second
                first_num = current_data
            
        enter = False
        current_data = ''
    
    draw_text(display_data, 32, 450, 100, WHITE, 'CR', outline_colour=LIGHT_BLUE, thickness=3, button=False)
                
    draw_main_menu()
    
    draw_input_base_menu()
    if choice1 == 0:
        draw_text(' [Initial -------> Final] ', 24, 0, 40, LIGHT_BLUE, 'TL', GREY)
        draw_output_base_menu()
    else:
        draw_text('[+/-  Base]', 22, 0, 40, LIGHT_BLUE, 'TL', GREY)
    if choice1 == 0:
        if (choice2 == 0 or choice3 == 0) and (choice2 == 1 or choice3 == 1):
            draw_binary_options()
    else:
        if choice2 == 0:
            draw_binary_options()
    
    pressed1 = []
    pressed2 = []
    pressed3 = []
    pressed4 = []

    # here we call function to check which buttons are pressed for each menu
    for rect in button_rects1:
        pressed1.append(check_button(rect))

    for rect in button_rects2:
        pressed2.append(check_button(rect))

    for rect in button_rects3:
        pressed3.append(check_button(rect))

    for rect in button_rects4:
        pressed4.append(check_button(rect))
    
    # setting these to compare to new one later
    old_choice1 = choice1           
    old_choice2 = choice2
    old_choice3 = choice3
    old_choice4 = choice4

    for i, val in enumerate(pressed1): #and then loop through buttons setting value to a variable for each
        if val:  # save choice if the button was pressed
            choice1 = i
    
    for i, val in enumerate(pressed2):
        if val:  
            choice2 = i
            if choice3 == i:
                # if its the same as the other base, switch that one to this ones old value
                choice3 = old_choice2
                pressed3[old_choice2] = True

    for i, val in enumerate(pressed3):
        if val:
            if choice1 == 0:  # only if on conversion mode as otherwise 2nd convert option can be ignored
                # save 2nd conversion choice to restore when changing back to convert mode
                choice3 = previous_choice3 = i
                if choice2 == i:
                    # if its the same as the other base, switch that one to this ones old value
                    choice2 = old_choice3
                    pressed2[old_choice3] = True

    for i, val in enumerate(pressed4):
        if val:
            if choice1 == 0: #if on conversion mode needs more requirements to reassign binary -ve options
                if (choice2 == 0 or choice3 == 0) and (choice2 == 1 or choice3 == 1):
                    choice4 = i
                    previous_choice4 = i
            else:
                if choice2 == 0:
                    choice4 = i
                    previous_choice4 = i
    
    #here these sets a value to each choice if there was a change, as the values from pressed lists are volatile and change back after release
    if old_choice1 != choice1: 
        choice1 = check_change(0, pressed1)
    
    if old_choice2 != choice2:
        choice2 = check_change(1, pressed2)
    
    if old_choice3 != choice3:
        choice3 = check_change(2, pressed3)
        
    if old_choice4 != choice4:
        choice4 = check_change(3, pressed4)

    if choice1 != 0: #if on add/sub mode number of chars shown n results increases and shifts a bit left as more room
        choice3 = None
        result_length = 32 #do if display data > 20 or smth here
        result_x = 415
        if choice2 == 0:
            if choice4 == None: #if just changed back to only binary for add/sub
                choice4 = previous_choice4 #resets sm/2's to previous val
        else:
            choice4 = None #then no need for sm/ 2's option
        
    else: #if conversion mode
        if not (choice2 == 0 or choice3 == 0) or not (choice2 == 1 or choice3 == 1): #if not denary2binary or binary2denary
            choice4 = None #then no need for sm/ 2's option
        else:
            if choice4 == None: #if just changed back to one of above options
                choice4 = previous_choice4 #resets sm/2's to previous val
                
        if choice3 == None: #resets values to conversion mode ones
            result_length = 26
            result_x = 462
            if choice2 != previous_choice3:
                choice3 = previous_choice3
            else:
                #this block checks if they went on add/sub then changed input base to what output base was and resets output base colour and num to somth different to input base    
                temp_count = 0 
                while previous_choice3 == choice2: #until new choice3 is changed to smth different to choice2
                    #2 here = output_base_fills
                    all_fills[2][previous_choice3] = LIGHT_BLUE 
                    choice3 = temp_count
                    previous_choice3 = temp_count
                    old_choice3 = choice3 #so that it doesnt check change like for user click and get confused
                    temp_count += 1
                
                all_fills[2][choice3] = GREEN
    
    if show_result:
        results_msg = 'Result [' + conversions[display_base] + '] =' #forming nice string to display result, showing which base its in
        draw_text(results_msg, 32, 450, 175, WHITE, 'CR', outline_colour=LIGHT_BLUE, thickness=3, button=False) #drawing result
        
        result_str = negative_string + str(result) #displays the word negative if they subtracted a bigger num from a smaller num
        if len(result_str) > result_length: #checks if the result is longer than the limit
            result_str = result_str[:result_length-2] + '...' #shortens it if it is
        draw_text(result_str, 32, result_x, 220, WHITE, 'CR', outline_colour=LIGHT_BLUE, thickness=3, button=False) #draws result with msg

    if show_invalid:
        draw_text('Invalid Input!', 32, 450, 175, WHITE, 'CR', outline_colour=LIGHT_BLUE, thickness=3, button=False) #tells u if input was invalid
        if now - start_invalid > invalid_length:
            show_invalid = False #stops showing after set time length
        
    pg.display.flip() #updates the contents of the entire display 
    clock.tick(FPS)
    
pg.quit()
quit()
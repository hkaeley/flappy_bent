#Created with assistance from Clear Code YouTube Tutorial
#    https://www.youtube.com/watch?v=UZg49z76cLw&ab_channel=ClearCode


import pygame
import sys
import random


def draw_floor(screen,base_surface,base_x_position,base_y_position,width):
    #putting two base surfaces next to each other to make the base seem longer
    screen.blit(base_surface,(base_x_position,base_y_position)) 
    screen.blit(base_surface,(base_x_position + width,base_y_position)) 
    
def create_cap(cap_surface,poss_cap_height):
    #make new capacitors on top and bottom and place them using their  midtop as reference
    bot_new_cap = cap_surface.get_rect(midtop = (800,random.choice(poss_cap_height))) 
    top_new_cap = cap_surface.get_rect(midbottom = (800,random.choice(poss_cap_height) - 250))
    return bot_new_cap,top_new_cap

def move_caps(caps): 
    #move all the caps in the caps list over to the left
    for cap in caps:
        cap.centerx -= 5
#     return caps

def draw_caps(caps,screen,cap_surface):
    #draw the caps
    for cap in caps:
        if cap.bottom >= 1024:
            screen.blit(cap_surface,cap)
        else:
            flip_cap = pygame.transform.flip(cap_surface,False,True)
            screen.blit(flip_cap,cap)
            
def check_collision(caps,bent_rect):
    for cap in caps:
        #check if bent collides with caps
        if bent_rect.colliderect(cap):
            return False
        #check if bent is too far up or too far down
        if bent_rect.top <= -100 or bent_rect.bottom >= 900:
            return False
    return True

def rotate_bent(bent,bent_movement):
    return pygame.transform.rotozoom(bent,-bent_movement * 3,1)

def change_background(screen_num,screen_size,screens):
    #change the background
    b_surface = pygame.image.load(screens[screen_num]).convert()
    b_surface = pygame.transform.scale(b_surface,screen_size)
    return b_surface


        

def score_display(game_state,screen,game_font,score,high_score):
    if game_state == 1:
        #if its running, just put in the 
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center=(512,100))
        screen.blit(score_surface,score_rect)
    else:
        score_surface = game_font.render(f"Score:  {int(score)}",True,(255,255,255))
        score_rect = score_surface.get_rect(center=(512,100))
        screen.blit(score_surface,score_rect)
    
        high_score_surface = game_font.render(f"High Score: {int(high_score)}",True,(255,255,255))
        high_score_rect = score_surface.get_rect(center=(512,200))
        screen.blit(high_score_surface,high_score_rect)
        
        replay_surface = game_font.render("Press Space to Play Flappy Bent!",True,(255,255,255))
        replay_rect = score_surface.get_rect(center=(350,300))
        screen.blit(replay_surface,replay_rect)
        

def run_game():

    pygame.init() #init
    
    #width and height of the screen
    width = 1024
    height = 1024
    
    game_font = pygame.font.Font("images/04B_19.ttf", 40)
    
    screen_num = 1
    screens = ["images/ap_7.jpg","images/ap_8.jpg","images/ap_4.jpg","images/ap_9.jpg","images/ap_10.jpg","images/ap_11.jpg","images/mesa_court.jpg","images/ap_2.jpg"]
    obstacles = ["images/cap2.png","images/diode.png","images/resistor.png","images/transistor.png"]
    
    screen_size = (width,height) #screen size
    base_size = (width,200) #size of the base 
    bent_size = (30,30) #size of the bent
    cap_size = (80,700) #size of the capacitors
    poss_cap_height = [400,500,550]
    
    #screen object
    screen = pygame.display.set_mode(screen_size) # w x h of the screen
    
    #clock object
    clock = pygame.time.Clock()
    
    #gravity added to bent_movement in the game loop which moves the bent
    gravity = 0.18
    bent_movement = 0
    game_running = True
    score = 0
    old_score = 0
    high_score = 0
    
    
    #surface for the background - change this if you want to change the background
    background_surface = pygame.image.load("images/ap_7.jpg").convert() #2
    #resize background image to fit the game window
    background_surface = pygame.transform.scale(background_surface,screen_size)
    
    #surface for the base
    base_surface = pygame.image.load("images/base.png").convert()
    #resize the base
    base_surface = pygame.transform.scale(base_surface, base_size)
    
    base_x_position = 0 #the x position of the base image on the screen
    base_y_position = 900
    
    #surface for the bent
    bent_surface = pygame.image.load("images/tbp_bent.png").convert_alpha()
    #resize the surface for the bird
    bent_surface = pygame.transform.scale(bent_surface,bent_size) #change the size of the surface if needed
    #put rectangle around the bird surface so we can rotate it and check for collisions
    bent_rect = bent_surface.get_rect(center = (100,height/2)) #pass in where u want the center of the rect to be
    #surface for the capacitor (pipes)
    cap_surface = pygame.image.load("images/transistor.png").convert_alpha()
    #resize the capacitors
    cap_surface = pygame.transform.scale(cap_surface,cap_size)
    #create a list of capacitors to keep track of all of them
    cap_list = []
    
    #create a new capacitor every 1.2 seconds
    spawn_capacitor = pygame.USEREVENT
    pygame.time.set_timer(spawn_capacitor, 1200) #create the spawn event every 1.2 seconds
    
    started = 0
    
    #game loop containing input loop
    while True:
        #event loop
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #quit
                pygame.quit() #click x on top right to close
                sys.exit() #properly close the window
            
            if event.type == pygame.KEYDOWN: #checks if a keyboard key has been pressed down
                if event.key == pygame.K_SPACE and game_running: #if the key pressed is space, move the bent up
                    bent_movement = 0 
                    bent_movement -= 8
                elif event.key == pygame.K_SPACE and game_running == False:
                    #restart the game
                    started = 1
                    score = 0
                    game_running = True
                    cap_list.clear()
                    bent_rect.center = (100,height/2)
                    bent_movement = 0
                
            
            if event.type == spawn_capacitor:          
                #updating the score 
                if game_running:
                    if len(cap_list) == 0:
                        old_score = 0
                        score = 0
                    else:
                        old_score = score
                        score += 1
    
                cap_surface = pygame.image.load(random.choice(obstacles)).convert_alpha()
                cap_surface = pygame.transform.scale(cap_surface,cap_size)
                cap_list.extend(create_cap(cap_surface,poss_cap_height)) #add a capacitor to the capacitor list
                
        
        if score % 1 == 0 and score != 0 and score != old_score:
            if screen_num > len(screens) - 1:
                screen_num = 0
            background_surface = change_background(screen_num,screen_size,screens)
            screen_num += 1
            old_score = score
            
        
        
        
        screen.blit(background_surface,(0,0)) #put background onto the main display screen 
        game_running = check_collision(cap_list,bent_rect)
        
        if started == 0:
            game_running = False
        
        if game_running == True:
            #bent
            bent_movement += gravity #addition gravity is slowly bringing the bent down 
            rotated_bent = rotate_bent(bent_surface,bent_movement)#rotate the bent when user moves it up
            bent_rect.centery  += bent_movement #actually moving he bent down/up using its center
            screen.blit(rotated_bent ,bent_rect)#put bent onto the main display screen 
            check_collision(cap_list,bent_rect)#check to see if bird colliding wiht any of the caps
            
            #caps
            move_caps(cap_list)
            draw_caps(cap_list,screen,cap_surface)
    #         score += 0.0055
            score_display(1,screen,game_font,score,high_score)
        else:
            if score > high_score:
                high_score = score
            score_display(0,screen,game_font,score,high_score)
            
    
    
        #base    
        base_x_position -= 1 #moving the floor over to the left, change speed here
        draw_floor(screen,base_surface,base_x_position,base_y_position,width)  #put base onto the main display screen 
        
        if base_x_position <= -width: #resetting the two base images next to each other when they go too far left
            base_x_position = 0 #makes base seem like its infinite
        
        
        pygame.display.update()
        clock.tick(144) #144 frames per second

if __name__ == "__main__":
    run_game()
    
    

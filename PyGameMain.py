import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    """Class for Player Object"""
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        """Detects player input"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity -= 20
            self.jump_sound.play()

    def apply_gravity(self):
        """In-game jumping gravity"""
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: 
            self.rect.bottom = 300
            self.gravity = 0

    def player_animation(self):
        """Gives animation for the Player"""
        # Changes to jumping animation when player jumps
        if self.rect.bottom < 300:
            self.image = self.player_jump
        
        # Walking animation
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): 
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        """Updates Player object"""
        self.player_input()
        self.apply_gravity()
        self.player_animation()


class Obstacle(pygame.sprite.Sprite):
    """Class for obstacle object"""
    def __init__(self, type):
        super().__init__()
        # Initializes obstacle type
        if type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 200
        else:
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def obstacle_animation(self):
        """Gives animation for the Obstacles"""
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        global objects_speed
        """Upadates Obstacles movement"""
        self.obstacle_animation()  
        self.rect.x -= (objects_speed + 5)
        self.destroy()

    def destroy(self):
        """Destroys obstacle object when out of screen"""
        if self.rect.x <= -100:
            self.kill() 


class Coins(pygame.sprite.Sprite): 
    """Class for coin objects"""  
    def __init__(self, type = "ground"):
        super().__init__()
        # Sets coin spawn 
        if type == "ground":
            y_pos = 300
        elif type == "sky":
            y_pos = 210

        self.image = (pygame.transform.scale_by((pygame.image.load("graphics/coins.png")), 0.15)).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
        self.coin_sound = pygame.mixer.Sound("audio/coins_sound.wav")
        self.coin_sound.set_volume(0.4)
        self.current_score = 0

    def display_score(self):
        """Displays score """
        score_surf = test_font.render(f'Score : {current_score}', False, (64, 64, 64))
        score_rect = score_surf.get_rect(center = (400, 40))
        screen.blit(score_surf, score_rect)
        return current_score
        
    def destroy(self):
        """Destroys coin object when out of screen"""
        if self.rect.x <= -100:
            self.kill() 

    def update(self):
        """Updates coin movement and score"""
        global objects_speed, current_score

        self.rect.x -= (objects_speed + 3)
        self.destroy()

        if pygame.sprite.spritecollide(player.sprite, coins_group, False):
            # Increases objects speed
            if current_score % 5 == 4 and objects_speed < 25:
                objects_speed += 1

            self.kill()
            current_score += 1
            self.coin_sound.play()


def display_start():
    """Displays starting screen"""
    screen.fill((94, 129, 162))
    title_surf = test_font.render(f'Running Adventure', False, (111, 196, 169))
    title_rect = title_surf.get_rect(center = (400, 40))
    welcome_surf =  test_font.render(f"Welcome!", False, (64, 64, 64))
    welcome_rect = welcome_surf.get_rect(center = (400, 80))
    message_surf = test_font.render(f"Press space to run", False, (64, 64, 64))
    message_rect = message_surf.get_rect(center = (400, 320))
    screen.blit(player_stand, player_stand_rect)
    screen.blit(title_surf, title_rect)
    screen.blit(welcome_surf, welcome_rect)
    screen.blit(message_surf, message_rect)

def collision_obstacle():
    """Detects collision with an Obstacle 
    If detects a collision with an obstacle, will return True, else False"""
    global current_score, objects_speed
    death_sound = pygame.mixer.Sound("audio/death_sound.wav")
    death_sound.set_volume(0.3)

    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        coins_group.empty()
        current_score = 0
        objects_speed = 7
        death_sound.play()
        return False
    else:
        return True
    

# Initializes variable
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Running Adventure Beta')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# Set default conditions
game_active = False
start = False
new_high_score = False
current_score = 0
previous_score = 0 
high_score = 0
objects_speed = 7

# Set in-game backgrounds and menu objects
sky_surf = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0 ,2)
player_stand_rect = player_stand.get_rect(midbottom = (400, 270))

# Set in-game musics
background_music = pygame.mixer.Sound('audio/music.wav')
background_music.set_volume(0.3)
background_music.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
coins_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

# Timer
obstacle_timer = pygame.USEREVENT + 1
coins_timer = pygame.USEREVENT + 2

pygame.time.set_timer(obstacle_timer, 1500)
pygame.time.set_timer(coins_timer, 2000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # Starts game
                start = True

        if game_active:
            # Adds obstacle objects
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

            # Adds coin objects
            if event.type == coins_timer:
                coins_group.add(Coins(choice(["ground", "ground", "sky"])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

        if not start:
            display_start()

    # Game runs
    if game_active:
        new_high_score = False
        screen.blit(sky_surf,(0, 0))
        screen.blit(ground_surf,(0, 300))
        previous_score = Coins().display_score() 
    
        # Player
        player.draw(screen)
        player.update()

        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Coins
        coins_group.draw(screen)
        coins_group.update()

        game_active = collision_obstacle()

    # Restart display
    elif not game_active and start:
        #Checks new high score
        if previous_score > high_score:
            high_score = previous_score
            new_high_score = True
            new_high_score_surf = test_font.render('(New)', False, (45, 196, 141))
            new_high_score_rect = new_high_score_surf.get_rect(center = (560, 340)) 

        # Restart screen
        player_gravity = 0
        high_score_surf = test_font.render(f'High score : {high_score}', False, (64, 64, 64))
        high_score_rect = high_score_surf.get_rect(center = (400, 340))
        game_over_surf = test_font.render('Game Over!', False, (111, 196, 169))
        game_over_rect = game_over_surf.get_rect(center = (400, 50))
        restart_surf = test_font.render('Press space to restart', False, (209, 44, 107))
        restart_rect = restart_surf.get_rect(center = (400, 377))
        score_surf = test_font.render(f'Your Score: {previous_score}', False, (64, 64, 64))
        score_rect = score_surf.get_rect(center = (400, 300))

        screen.fill((94, 129, 162))

        # Tells Player of new highscore
        if new_high_score:  screen.blit(new_high_score_surf, new_high_score_rect)

        screen.blit(high_score_surf, high_score_rect)
        screen.blit(player_stand, player_stand_rect)
        screen.blit(score_surf, score_rect)
        screen.blit(game_over_surf, game_over_rect)
        screen.blit(restart_surf, restart_rect)

    pygame.display.update()
    clock.tick(60)

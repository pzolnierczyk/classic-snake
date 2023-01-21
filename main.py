import pygame, random

class food:
    '''
    Creating food for the snake. 
    Each coordinate is rounded to 10 px, they are recreated until there is no collision with the snake

    player_xy: player location along the X and Y axes
    width: screen width (X)
    height: screen height (Y)
    block: size of each displayed block 
    '''

    def __init__(self, player_xy, width, height, block) -> None:
        self.player_xy = player_xy
        self.width = width
        self.height = height
        self.block = block

    def food_x(self):
        return round(random.randrange(0, self.width-self.block)/10)*10
    def food_y(self):
        return round(random.randrange(0, self.height-self.block)/10)*10

    def food_creation(self):
        food_xy = [self.food_x(), self.food_y()]
        while food_xy == self.player_xy: 
            food_xy = [self.food_x(), self.food_y()]
        return food_xy


class game:
    '''
    Main class of the game
    '''
    
    def __init__(self) -> None:
        self.snake_color = (37, 66, 82)
        self.food_color = (240,67,82)
        self.background_color = (245,212,169)
        self.critical_msg_color = (234, 28, 62)
        self.ordinary_msg_color = (50, 50, 60)
        self.score_color = (0,0,0)
        self.screen_size = self.width, self.height = 800, 600
        self.block = 10

    def message(self, msg, font_size, color, y_loc = 3*600/7):
        '''
        Function for displaying messages
        msg: text of the message
        font_size: text size
        color: text color
        y_loc: text location along the Y axis (height)
        '''

        font = pygame.font.SysFont('Corbel', font_size)
        text = font.render(msg, True, color)
        text_rect = text.get_rect(center=(self.width/2, y_loc))
        self.screen.blit(text, text_rect)

    def start_menu(self, game_loop):
        '''
        Start menu of the game
        game_loop: flag for game continuation. False: game aborted, True: game continues
        '''
    
        pause = True
        # pygame.event.clear()
        while pause:
            event = pygame.event.wait()
            
            if event.type == pygame.QUIT:
                game_loop = False
                pause = False
            
            self.message('SNAKE', 50, self.critical_msg_color, self.height/4)
            self.message('Press any key to start the game', 30, self.ordinary_msg_color, self.height/3)
            pygame.display.update()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_loop = False
                    pause = False
                if event.key != pygame.K_ESCAPE:
                    pause = False
        return game_loop

    def quit_game(self):
        game_loop = False
        game_over = False
        return game_loop, game_over

    def game_pause(self, game_loop):
        '''
        Pause state
        '''

        pause = True
        pygame.event.clear()
        
        while pause:
            event = pygame.event.wait()
            
            if event.type == pygame.QUIT:
                game_loop = False
                pause = False
            
            self.message('Game Paused. Press P to continue', 30, self.critical_msg_color)
            pygame.display.update()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_loop = False
                    pause = False
                    return game_loop
                if event.key == pygame.K_p:
                    pause = False
        return game_loop
    
    def snake_move(self, snake_length, movement, new_movement):
        '''
        Snake movement

        Exception for reversed movement: if snake is longer than 1 it cannot turn around in spot 
        For example, if snake goes right, he cannot immediately go left etc
        movement: the movement performed the last time
        new_movement: new movement the player tries to do 
        '''

        if snake_length == 1: movement = new_movement
        elif new_movement != [-x for x in movement]:
                movement = new_movement
        return movement

    def player_score(self, length):
        ''' Displaying the score
        lenght: snake length'''
        score = (length-1)*10
        scoring_msg = pygame.font.SysFont(None, 25).render("Score: " +str(score), True, self.score_color)
        self.screen.blit(scoring_msg, [10,10])

    def main(self):
        '''
        Main function of the game
        '''

        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Snake!')
        clock = pygame.time.Clock()

        game_loop = True
        game_over = False

        player_xy = [self.width/2, self.height/2]
        head = player_xy.copy()
        snake_coords = []
        snake_coords.append(head)
        snake_length = 1
        movement = [0,0]

        f = food(player_xy, self.width, self.height, self.block)
        food_xy = f.food_creation()

        self.screen.fill(self.background_color)
        game_loop = self.start_menu(game_loop)

        while game_loop:
            
            while game_over:
                if event.type == pygame.QUIT: 
                    game_loop, game_over = self.quit_game()
                self.message('Game over', 50, self.critical_msg_color, self.height/4)
                self.message('Press SPACE to play again or ESC to exit', 30, self.critical_msg_color, self.height/3)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:    
                        if event.key == pygame.K_ESCAPE: 
                            game_loop, game_over = self.quit_game()
                        if event.key == pygame.K_SPACE: self.main()

            # Keyboard Control 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: game_loop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        new_movement = [-self.block, 0]
                        movement = self.snake_move(snake_length, movement, new_movement)
                    if event.key == pygame.K_RIGHT:
                        new_movement = [self.block, 0]
                        movement = self.snake_move(snake_length, movement, new_movement)
                    if event.key == pygame.K_UP:
                        new_movement = [0, -self.block]
                        movement = self.snake_move(snake_length, movement, new_movement)
                    if event.key == pygame.K_DOWN:
                        new_movement = [0, self.block]
                        movement = self.snake_move(snake_length, movement, new_movement)   
                    if event.key == pygame.K_p: 
                        game_loop = self.game_pause(game_loop)
                    if event.key == pygame.K_ESCAPE: 
                        game_loop, game_over = self.quit_game()
                            

            player_xy[0] = player_xy[0]+movement[0]
            player_xy[1] = player_xy[1]+movement[1]

            # Collision with wall 
            if player_xy[0] < 0 or player_xy[0] > self.width or player_xy[1] < 0 or player_xy[1] > self.height:
                game_over = True

            # Collision with itself
            for coordinate in snake_coords[:-1]:
                if coordinate == player_xy: game_over = True

            # Eating food
            if player_xy == food_xy:
                food_xy = f.food_creation()
                snake_length+=1

            # Snake coordinates
            if player_xy != snake_coords[-1]: #ensuring part of snake won't disappear if the loop is too fast
                head = player_xy.copy()
                snake_coords.append(head)
            if len(snake_coords) > snake_length:
                del snake_coords[0]
            print(snake_coords)
            
            # Image refresh
            self.screen.fill(self.background_color)
            pygame.draw.rect(self.screen,self.food_color,[food_xy[0], food_xy[1], self.block, self.block])
            for coordinate in snake_coords:
                pygame.draw.rect(self.screen, self.snake_color,[coordinate[0], coordinate[1], self.block, self.block])
            
            self.player_score(snake_length) #scoring
            pygame.display.update()

            clock.tick(30)
        
        pygame.quit()
        quit()  


snake = game()
snake.main()
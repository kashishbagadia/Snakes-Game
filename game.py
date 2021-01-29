"""
Snakes With Kashish
Made with PyGame
"""
import pygame, random, os

pygame.mixer.init()

pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#Background Image
bgimg = pygame.image.load("snake.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snakes With Kashish")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snake_list, snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((255,140,0))
        text_screen("Snakes Game:Let's Play!", black, 240, 250)
        text_screen("[Press Space Bar To Start]", black, 232, 292)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('playback.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snake_list = []
    snake_length = 1
    direction = 'RIGHT'
    change_to = direction

    # Check if highscore file exists, if not then creating the highscore file
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 5
    snake_size = 20
    fps = 60
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            gameWindow.fill((255,140,0))
            text_screen("Game Over:(", black, 340, 230)
            text_screen("[Press Enter To Continue!]", black, 232, 292)
            text_screen("  Score: " + str(score), (255,255,255), 10, 10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

               # Whenever a key is pressed
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        change_to = 'RIGHT'

                    if event.key == pygame.K_LEFT:
                        change_to = 'LEFT'

                    if event.key == pygame.K_UP:
                        change_to = 'UP'

                    if event.key == pygame.K_DOWN:
                        change_to = 'DOWN'

                    if event.key == pygame.K_q:
                        score +=10

            # Making sure the snake cannot move in the opposite direction instantaneously
            if change_to == 'UP' and direction!= 'DOWN':
                direction = 'UP'
            if change_to == 'DOWN' and direction!= 'UP':
                direction = 'DOWN'
            if change_to == 'LEFT' and direction!= 'RIGHT':
                direction = 'LEFT'
            if change_to == 'RIGHT' and direction!= 'LEFT':
                direction = 'RIGHT'

            # Moving the snake
            if direction == 'UP':
                velocity_y = - init_velocity
                velocity_x = 0
            if direction == 'DOWN':
                velocity_y = init_velocity
                velocity_x = 0
            if direction == 'LEFT':
                velocity_x = - init_velocity
                velocity_y = 0
            if direction == 'RIGHT':
                velocity_x = init_velocity
                velocity_y = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            # Growing the snake body as it eats the food and updating the high score if any
            if abs(snake_x - food_x)<8 and abs(snake_y - food_y)<8:
                score +=10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snake_length +=5
                if score>int(highscore):
                    highscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("  Score: " + str(score) + "  Highscore: "+str(highscore), (178,34,34), 10, 10)
            pygame.draw.rect(gameWindow, white, [food_x, food_y, snake_size, snake_size])


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list)>snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('gameover.wav')
                pygame.mixer.music.play()

            #Game over conditions
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('gameover.wav')
                pygame.mixer.music.play()
            plot_snake(gameWindow, (0,255,0), snake_list, snake_size)

        #Refresh the screen
        pygame.display.update()

        #Refresh rate
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()

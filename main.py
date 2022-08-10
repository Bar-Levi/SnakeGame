import pygame
import random


class BodyPart:  # A class which represents each body part of the snake.
    snake_size = 0

    def __init__(self, x=0, y=0, direction="Up"):
        self.x = x  # Own X coordinate.
        self.y = y  # Own Y coordinate.
        self.direction = direction  # Own direction.
        self.AddBodyPart()  # Calls AddBodyPart class' function.
        self.Head = False  # True is it's the first BodyPart of the snake.

    @classmethod
    def AddBodyPart(cls):  # Increasing the class variable "snake_size" by 1.
        cls.snake_size += 1


class Player:  # A class which represents a current or a past player of the game.
    def __init__(self, name, score=0):
        self.name = name  # Own name.
        self.score = score  # Own score.


pygame.init()  # Initializing Pygame.
# Setting some constant values:
FPS = 60
IMAGE_SIZE = 32
WIDTH, HEIGHT = 30 * IMAGE_SIZE, 20 * IMAGE_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Defining the colors as RGB tuples:
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (125, 125, 125)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
# Defining some booleans:
running = True
apple_eaten = True
Paused = False
Got_Username = False
moving_apples_on = True
# Initializing some variable which going to be used later:
movement_keys = ""
username = ""
timer = timer2 = 0
Textbox_Width = 300
Textbox_Height = 50
apple_x = apple_y = 0
moving_apples_x = random.randint(0, 29) * IMAGE_SIZE
moving_apples_y = random.randint(0, 19) * IMAGE_SIZE

# Loading the images:
RED_CARPET = pygame.image.load("red_carpet.png")
WASD_IMAGE = pygame.image.load("wasd.png")
ARROWS_IMAGE = pygame.image.load("arrows.png")
BOMB_ICON = pygame.image.load("bomb.png")
EXPLOSION_ICON = pygame.image.load("explosion.png")
pygame.display.set_caption("Bar Levi - Snake")
RED_APPLE = pygame.image.load("red_apple.png")
SNAKE_ICON = pygame.image.load("snake_icon.png")
pygame.display.set_icon(SNAKE_ICON)
SNAKE_BODY = pygame.image.load("snake_body.png")
TWO_APPLES_IMAGE = pygame.image.load("two_apples.png")

# Initializing head's image directions:
SNAKE_HEAD_DOWN = pygame.image.load("snake_head.png")
SNAKE_HEAD_RIGHT = pygame.transform.rotate(SNAKE_HEAD_DOWN, 90)
SNAKE_HEAD_UP = pygame.transform.rotate(SNAKE_HEAD_DOWN, 180)
SNAKE_HEAD_LEFT = pygame.transform.rotate(SNAKE_HEAD_DOWN, 270)


def NewGameSetup():  # Resetting all the required variables for a new game.
    global running, timer, apple_eaten, Paused, Got_Username, body_coordinates, snake_body, CURRENT_SNAKE_HEAD, Movement_Status, DIRECTION
    running = True
    apple_eaten = True
    Paused = False
    Got_Username = False
    timer = 0
    Movement_Status = DIRECTION = "Up"
    BodyPart.snake_size = 0
    snake_x, snake_y = 14 * IMAGE_SIZE, 10 * IMAGE_SIZE  # Bringing the snake's body back tho the middle of the window.
    # Creating the snake's body by initializing BodyPart() variables:
    head = BodyPart(snake_x, snake_y)
    head.Head = True  # That's the first body part -> Head = True.
    part1 = BodyPart(snake_x, snake_y + 1 * IMAGE_SIZE)
    part2 = BodyPart(snake_x, snake_y + 2 * IMAGE_SIZE)
    part3 = BodyPart(snake_x, snake_y + 3 * IMAGE_SIZE)
    part4 = BodyPart(snake_x, snake_y + 4 * IMAGE_SIZE)
    snake_body = [head, part1, part2, part3, part4]
    # Creating a list of the snake's body coordinates:
    body_coordinates = []
    for body_part in snake_body:
        body_coordinates.append((body_part.x, body_part.y))
    CURRENT_SNAKE_HEAD = SNAKE_HEAD_UP  # Updating the relevant direction for the head.


def DrawGrid():  # Drawing the grid.
    for x in range(0, WIDTH, IMAGE_SIZE):
        for y in range(0, HEIGHT, IMAGE_SIZE):
            rect = pygame.Rect(x, y, IMAGE_SIZE, IMAGE_SIZE)
            pygame.draw.rect(WIN, GRAY, rect, 1)


def CreateANewApple():  # Initializing the red apple's coordinates.
    global apple_x, apple_y, apple_eaten
    apple_eaten = False
    apple_x = random.randint(0, 29) * IMAGE_SIZE
    apple_y = random.randint(0, 19) * IMAGE_SIZE


def ShowApple(x, y):  # "Blitting" (showing) the apple on the screen.
    WIN.blit(RED_APPLE, (x, y))
    pygame.display.update()  # Updating the window.


def CreateASnake(body):  # Showing the snake's body.
    for body_part in body:
        if body_part == body[0]:
            WIN.blit(SNAKE_HEAD_UP, (body_part.x * IMAGE_SIZE, body_part.y * IMAGE_SIZE))
        else:
            WIN.blit(SNAKE_BODY, (body_part.x * IMAGE_SIZE, body_part.y * IMAGE_SIZE))


def GameOver(body_coordinates):  # Exploding the snake's body, and Adding the player's name and score to "Records.txt".
    global username
    explosion_sound = pygame.mixer.Sound("explosion_sound.wav")
    # Exploding the snake's body:
    for coordinate in body_coordinates:
        WIN.blit(BOMB_ICON, coordinate)
        pygame.display.update()
        pygame.time.wait(100)
    for coordinate in body_coordinates:
        WIN.blit(EXPLOSION_ICON, coordinate)
        explosion_sound.play()
        pygame.display.update()
        pygame.time.wait(100)
    pygame.time.wait(2000)
    Records = open("Records.txt", 'a')  # Creating/Opening a text file "Records.txt" for appending text.
    Records.write(f"{username}\n{BodyPart.snake_size}\n")  # Appending the player's name and score to "Records.txt".
    Records.close()  # Closing and saving "Records.txt".
    Menu()  # Sending the player back to the main menu.
    pygame.quit()
    exit(1)


def AddBodyPart():  # Adding a body part after the current last one by checking the coordinates it should appear in.
    global body_coordinates, snake_body
    if snake_body[len(snake_body) - 1].direction == "Up":
        new_body = BodyPart(body_coordinates[-1][0], body_coordinates[-1][1] + 1)
    if snake_body[len(snake_body) - 1].direction == "Down":
        new_body = BodyPart(snake_body[len(body_coordinates[-1][0], body_coordinates[-1][1] - 1)])
    if snake_body[len(snake_body) - 1].direction == "Right":
        new_body = BodyPart(snake_body[len(body_coordinates[-1][0] - 1, body_coordinates[-1][1])])
    if snake_body[len(snake_body) - 1].direction == "Left":
        new_body = BodyPart(body_coordinates[-1][0] + 1, body_coordinates[-1][1])
    snake_body.append(new_body)
    body_coordinates.append((new_body.x, new_body.y))


def CheckRules(body_coordinates):  # Check whether the player is breaking the rules.
    if body_coordinates[0][0] < 0 or body_coordinates[0][0] == WIDTH or body_coordinates[0][1] < 0 or \
            body_coordinates[0][1] == HEIGHT:  # Snake goes out of the screen.
        pygame.time.wait(500)
        GameOver(body_coordinates)
    for coordinate in body_coordinates:  # If the head is hitting another body part.
        if body_coordinates.count(coordinate) > 1:
            GameOver(body_coordinates)


def HandleSnakeMovement(direction):  # The function which is actually changing the snake's position.
    global body_coordinates, apple_x, apple_y, apple_eaten, Movement_Status, timer2
    timer2 += 1
    for index in range(len(body_coordinates) - 1, -1, -1):
        if index != 0:  # If the coordinates are not the head's coordinates:
            body_coordinates[index] = body_coordinates[index - 1]  # Each body part is following up the next one's spot.
        else:  # If the coordinates are the head's coordinates -> Moving the head according to the relevant direction:
            if direction == "Up":
                body_coordinates[index] = (body_coordinates[index][0], body_coordinates[index][1] - IMAGE_SIZE)
                Movement_Status = "Up"
            if direction == "Down":
                body_coordinates[index] = (body_coordinates[index][0], body_coordinates[index][1] + IMAGE_SIZE)
                Movement_Status = "Down"
            if direction == "Right":
                body_coordinates[index] = (body_coordinates[index][0] + IMAGE_SIZE, body_coordinates[index][1])
                Movement_Status = "Right"
            if direction == "Left":
                body_coordinates[index] = (body_coordinates[index][0] - IMAGE_SIZE, body_coordinates[index][1])
                Movement_Status = "Left"
    for (x, y) in body_coordinates:  # Showing the snake's body.
        if (x, y) == body_coordinates[0]:
            WIN.blit(CURRENT_SNAKE_HEAD, (x, y))
        else:
            WIN.blit(SNAKE_BODY, (x, y))
    CheckRules(body_coordinates)  # Checking whether the player is breaking the rules and should lose.
    # line 200: Determines the snake's movement speed by choosing the waiting time between moves.
    # line 200: Less time waiting = Faster.
    # line 200: "timer/100" - Making sure the speed is slowly increased while playing since "timer" is always increasing.
    pygame.time.wait(int(240 - timer / 100))
    if body_coordinates[0] == (apple_x, apple_y):  # If the snake is eating the apple:
        eating_sound = pygame.mixer.Sound("bite_sound.wav")
        eating_sound.play()  # Play a biting sound.
        AddBodyPart()  # Add a body part to the snake.
        apple_eaten = True


def CheckArrowsMovement(event):  # Checking the "Arrows" pressing what the player chose to play with the "Arrows" buttons.
    global DIRECTION, CURRENT_SNAKE_HEAD
    if event.key == pygame.K_UP and body_coordinates[0][0] != body_coordinates[1][
        0]:  # If pressed 'Up' and snake isn't going downwards.
        DIRECTION = "Up"
        CURRENT_SNAKE_HEAD = SNAKE_HEAD_UP
    if event.key == pygame.K_DOWN and body_coordinates[0][0] != body_coordinates[1][
        0]:  # If pressed 'Down' and snake isn't going upwards.
        DIRECTION = "Down"
        CURRENT_SNAKE_HEAD = SNAKE_HEAD_DOWN
    if event.key == pygame.K_LEFT and body_coordinates[0][1] != body_coordinates[1][
        1]:  # If pressed 'Left' and snake isn't going right.
        DIRECTION = "Left"
        CURRENT_SNAKE_HEAD = SNAKE_HEAD_LEFT
    if event.key == pygame.K_RIGHT and body_coordinates[0][1] != body_coordinates[1][
        1]:  # If pressed 'Right' and snake isn't going left.
        DIRECTION = "Right"
        CURRENT_SNAKE_HEAD = SNAKE_HEAD_RIGHT


def CheckWASDMovement(event):  # Checking the "WASD" pressing what the player chose to play with the "WASD" buttons.
    global DIRECTION, CURRENT_SNAKE_HEAD
    if event.key == pygame.K_w and body_coordinates[0][0] != body_coordinates[1][
        0]:  # If pressed 'w' and snake isn't going downwards.
        DIRECTION = "Up"
        CURRENT_SNAKE_HEAD = SNAKE_HEAD_UP
    elif event.key == pygame.K_s and body_coordinates[0][0] != body_coordinates[1][
        0]:  # If pressed 's' and snake isn't going upwards.
        DIRECTION = "Down"
        CURRENT_SNAKE_HEAD = SNAKE_HEAD_DOWN
    elif event.key == pygame.K_a and body_coordinates[0][1] != body_coordinates[1][
        1]:  # If pressed 'a' and snake isn't going right.
        DIRECTION = "Left"
        CURRENT_SNAKE_HEAD = SNAKE_HEAD_LEFT
    elif event.key == pygame.K_d and body_coordinates[0][1] != body_coordinates[1][
        1]:  # If pressed 'd' and snake isn't going left.
        DIRECTION = "Right"
        CURRENT_SNAKE_HEAD = SNAKE_HEAD_RIGHT


def GetSettings():  # Getting information from the player: username and playing buttons.
    global Got_Username, username, movement_keys
    # Setting a textbox for player's username input.
    textbox = pygame.Rect(WIDTH / 2 - Textbox_Width / 2, HEIGHT / 2 - Textbox_Height / 2, Textbox_Width, Textbox_Height)
    user_window = pygame.display.set_mode((WIDTH, HEIGHT))  # Creating a new window.
    while not Got_Username:
        user_window.fill(BLACK)  # Filling the window with a black color, for getting a black background.
        pygame.draw.rect(user_window, WHITE, textbox)  # Drawing the input textbox on the window.
        font = pygame.font.SysFont(None, 48)  # Changing writing font.
        text = font.render(username, True, BLACK)  # Saving the written username as "text" variable.
        #  Asking the player to type in his username:
        message = font.render("Please enter your name:", True, WHITE)
        user_window.blit(message, (textbox.x - 42, textbox.y - 60))
        user_window.blit(text, (textbox.x + 5, textbox.y + 10))  # Showing the written username on the window.
        font = pygame.font.SysFont(None, 24)
        message = font.render("(Press 'Enter' to submit)", True, WHITE)
        user_window.blit(message, (textbox.x + 55, textbox.y + 70))  # Writing "Press 'Enter' to submit" under the textbox.
        pygame.display.update()
        for event in pygame.event.get():  # Getting the events which happen on the window while typing the username.
            if event.type == pygame.KEYDOWN:  # If there is a button pressing.
                if event.key == pygame.K_BACKSPACE:  # If the player is pressing the "Backspace" button.
                    username = username[0:-1]  # Removing the username's last character.
                elif event.key == pygame.K_RETURN:  # If the player is pressing the "Enter/Return" button.
                    if username != "" and username != "\t" and username != " ":  # If username isn't empty/"Space"/"Tab".
                        Got_Username = True
                else:
                    username += event.unicode  # Adding the typed characters to the "username" variable.
            if event.type == pygame.QUIT:  # If the player is pressing the "X" button on the window's top right corner.
                pygame.quit()  # Closing the window.
                exit(1)  # Closing the program.
    # Choosing movement keys - "WASD" / Arrows:
    Got_Movement_Keys = False
    movement_keys = ""
    font = pygame.font.SysFont(None, 48)
    while not Got_Movement_Keys:  # While the player still hasn't chosen his playing buttons, keep asking him to choose:
        user_window.fill(BLACK)
        message = font.render("Please click on your playing buttons:", True, WHITE)
        user_window.blit(message, (textbox.x - 150, textbox.y - 150))
        user_window.blit(WASD_IMAGE, (textbox.x + 200, textbox.y - 50))
        wasd_rect = pygame.Rect(textbox.x + 200, textbox.y - 50, 256, 256)
        user_window.blit(ARROWS_IMAGE, (textbox.x - 175, textbox.y - 50))
        arrows_rect = pygame.Rect(textbox.x - 175, textbox.y - 50, 256, 256)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # If the player is pressing the mouse button.
                if wasd_rect.collidepoint(pygame.mouse.get_pos()):  # if the player is pressing the WASD image.
                    movement_keys = "WASD"
                    Got_Movement_Keys = True
                if arrows_rect.collidepoint(pygame.mouse.get_pos()):# if the player is pressing the Arrows image.
                    movement_keys = "Arrows"
                    Got_Movement_Keys = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)
    font = pygame.font.SysFont(None, 80)
    for sec in range(3, 0, -1):  # Printing a 3, 2, 1 countdown.
        user_window.fill(BLACK)
        message = font.render(str(sec), True, WHITE)
        user_window.blit(message, (WIDTH / 2 - 20, HEIGHT / 2 - 20))
        pygame.display.update()
        pygame.time.wait(1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)


def Menu():
    Chose = False
    menu_window = pygame.display.set_mode((WIDTH, HEIGHT))
    TOP_FIVE_IMAGE = pygame.image.load("trophy.png")
    PLAY_AGAIN_IMAGE = pygame.image.load("snake_and_apple.png")
    EXIT_IMAGE = pygame.image.load("exit.png")
    play_again_rect = pygame.Rect(150, 350, 128, 128)
    top_five_rect = pygame.Rect(400, 350, 128, 128)
    exit_rect = pygame.Rect(650, 350, 128, 128)
    while not Chose:  # Showing the player a menu with 3 options: Play / Top 5 / Quit, and waiting until he's choosing.
        menu_window.fill(BLACK)
        pygame.draw.rect(menu_window, LIGHT_GRAY, play_again_rect)  # Background for Play Again image.
        pygame.draw.rect(menu_window, LIGHT_GRAY, top_five_rect)  # Background for Top 5 Players image.
        pygame.draw.rect(menu_window, LIGHT_GRAY, exit_rect)  # Background for Quit image.
        font = pygame.font.SysFont(None, 132)
        message = font.render("Main Menu", True, WHITE)
        menu_window.blit(message, (WIDTH / 2 - 260, 100))
        font = pygame.font.SysFont(None, 48)
        menu_window.blit(PLAY_AGAIN_IMAGE, (150, 350))
        message = font.render("Play", True, WHITE)
        menu_window.blit(message, (180, 300))
        menu_window.blit(EXIT_IMAGE, (650, 350))
        message = font.render("Quit", True, WHITE)
        menu_window.blit(message, (675, 300))
        menu_window.blit(TOP_FIVE_IMAGE, (400, 350))
        message = font.render("Top 5 Players", True, WHITE)
        menu_window.blit(message, (360, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # If the player is clicking the mouse, checking which choice he took.
                if play_again_rect.collidepoint(pygame.mouse.get_pos()):
                    Chose = True
                    main()
                if top_five_rect.collidepoint(pygame.mouse.get_pos()):
                    Chose = True
                    PrintLeaderboard()
                if exit_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit(1)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)


def Pause():  # Pausing the game and freezing the screen.
    global Paused
    PAUSE_IMAGE = pygame.image.load("pause-button.png")
    WIN.blit(PAUSE_IMAGE, (WIDTH / 2 - 64, HEIGHT / 2 - 64))
    pygame.display.update()
    while Paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # If the player is pressing 'p', the game is unpausing.
                    Paused = False
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)


def PrintLeaderboard():  # Showing the top 5 players with highest records.
    file1 = open("Records.txt", 'r')  # "Records.txt" - File of names and scores -> Opening it to be readable.
    file_data = file1.read().split('\n')  # Creating a list with the whole names and scores,
    # looking like: file_data = [name1, score1, name2, score2, name3, score3, etc.]
    file1.close()  # Closing the file -> "Records.txt" isn't readable anymore.
    names_and_scores = {}
    for index in range(0, len(file_data)):  # Organizing the data in a dictionary : {name1:score1, name2:score2, etc.}:
        if index % 2 == 0:
            name = file_data[index]
        else:
            if name in names_and_scores.keys():
                if int(names_and_scores[name]) < int(file_data[index]):
                    names_and_scores[name] = int(file_data[index])
            else:
                names_and_scores[name] = int(file_data[index])
    # Sorting the dictionary in a descending order, so the highest are first, and creating 2 lists of names and scores.
    sorted_data = {k: v for k, v in sorted(names_and_scores.items(), key=lambda v: v[1], reverse=True)}
    sorted_names = list(sorted_data.keys())
    sorted_scores = list(sorted_data.values())
    try:
        first_score = sorted_scores[0]
        second_score = sorted_scores[1]
        third_score = sorted_scores[2]
        fourth_score = sorted_scores[3]
        fifth_score = sorted_scores[4]
    except:
        print("There are less than 5 scores.")
    try:
        first_name = sorted_names[0]
        second_name = sorted_names[1]
        third_name = sorted_names[2]
        fourth_name = sorted_names[3]
        fifth_name = sorted_names[4]
    except:
        print("There are less than 5 names.")
    # After we have organized the data - creating the window.
    Quit = False
    # Showing a background of a red carpet:
    leaderboards_window = pygame.display.set_mode((WIDTH, HEIGHT))
    leaderboards_window.blit(RED_CARPET, (-60, 0))
    # Showing the title - "Top 5 Players":
    font = pygame.font.SysFont("arial", 72, True, True)
    text = font.render("Top 5 Players", True, WHITE)
    leaderboards_window.blit(text, (WIDTH / 2 - 235, HEIGHT / 2 - 275))
    # Showing the top left button - "Back to Main Menu":
    font = pygame.font.SysFont("arial", 20, True, True)
    menu_rect = pygame.Rect(20, 20, 200, 40)
    pygame.draw.rect(leaderboards_window, LIGHT_GRAY, menu_rect)
    text = font.render("Back to Main Menu", True, WHITE)
    leaderboards_window.blit(text, (28, 28))
    # Showing the leaderboards' table:
    LEADERBOARDS_IMAGE = pygame.image.load("leaderboard.png")
    leaderboards_window.blit(LEADERBOARDS_IMAGE, (WIDTH / 2 - 256, HEIGHT / 2 - 220))
    # Printing the Top 5 - NOTE: might be less than 5 (depends on the amount of players who have already played):
    try:
        font = pygame.font.SysFont(None, 45)
        text = font.render(first_name, True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 - 150, HEIGHT / 2 + 6))
        text = font.render(str(first_score), True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 + 125, HEIGHT / 2 + 6))
        text = font.render("1.", True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 - 198, HEIGHT / 2 + 6))
        text = font.render(second_name, True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 - 150, HEIGHT / 2 + 54))
        text = font.render(str(second_score), True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 + 125, HEIGHT / 2 + 54))
        text = font.render("2.", True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 - 198, HEIGHT / 2 + 54))
        text = font.render(third_name, True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 - 150, HEIGHT / 2 + 102))
        text = font.render(str(third_score), True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 + 125, HEIGHT / 2 + 102))
        text = font.render("3.", True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 - 198, HEIGHT / 2 + 102))
        text = font.render(fourth_name, True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 - 150, HEIGHT / 2 + 150))
        text = font.render(str(fourth_score), True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 + 125, HEIGHT / 2 + 150))
        text = font.render("4.", True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 - 198, HEIGHT / 2 + 150))
        text = font.render(fifth_name, True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 - 150, HEIGHT / 2 + 198))
        text = font.render(str(fifth_score), True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 + 125, HEIGHT / 2 + 198))
        text = font.render("5.", True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 - 198, HEIGHT / 2 + 198))
    except:
        print("There are less than 5 scores.")
    pygame.display.update()
    while not Quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(pygame.mouse.get_pos()):  # If the player is pressing the "Back to Main Menu" button.
                    Menu()  # Sending him to the menu.


def CreateMovingApples():  # Initializing moving apples (red and green - together) - worth 2 points.
    global moving_apples_x, moving_apples_y, moving_apples_on
    moving_apples_x = random.randint(0, 29) * IMAGE_SIZE
    moving_apples_y = random.randint(0, 19) * IMAGE_SIZE
    moving_apples_on = True


def HandleMovingApples():  # The function which is actually moving the moving apples.
    global moving_apples_x, moving_apples_y, body_coordinates, moving_apples_on, timer
    WIN.blit(TWO_APPLES_IMAGE, (moving_apples_x, moving_apples_y))
    if body_coordinates[0] == (moving_apples_x, moving_apples_y):  # If the snake is eating the moving apples.
        bite_sound = pygame.mixer.Sound("bite_sound.wav")
        bite_sound.play()
        moving_apples_on = False
        # Add 2 points - 2 body parts:
        AddBodyPart()
        AddBodyPart()
        timer = 0  # Resetting the moving apples' timer.
    if timer % 5 == 0:  # Changes the moving apples' direction.
        # 1 - Up, 2 - Down, 3 - Left, 4 - Right, 5 - UpRight, 6 - UpLeft, 7 - DownRight, 8 - DownLeft:
        dir = random.randint(1, 8)
        if dir == 1 and moving_apples_y != 0:
            moving_apples_y -= IMAGE_SIZE
        if dir == 2 and moving_apples_y != HEIGHT - IMAGE_SIZE:
            moving_apples_y += IMAGE_SIZE
        if dir == 3 and moving_apples_x != 0:
            moving_apples_x -= IMAGE_SIZE
        if dir == 4 and moving_apples_x != WIDTH - IMAGE_SIZE:
            moving_apples_x += IMAGE_SIZE
        if dir == 5 and moving_apples_y != 0 and moving_apples_x != WIDTH - IMAGE_SIZE:
            moving_apples_y -= IMAGE_SIZE
            moving_apples_x += IMAGE_SIZE
        if dir == 6 and moving_apples_y != 0 and moving_apples_x != 0:
            moving_apples_x -= IMAGE_SIZE
            moving_apples_y -= IMAGE_SIZE
        if dir == 7 and moving_apples_y != HEIGHT - IMAGE_SIZE and moving_apples_x != WIDTH - IMAGE_SIZE:
            moving_apples_x += IMAGE_SIZE
            moving_apples_y += IMAGE_SIZE
        if dir == 8 and moving_apples_y != HEIGHT - IMAGE_SIZE and moving_apples_x != 0:
            moving_apples_x -= IMAGE_SIZE
            moving_apples_y += IMAGE_SIZE


def main():  # The main function which handles all the other functions.
    global running, Paused, DIRECTION, timer
    NewGameSetup()
    GetSettings()
    CreateASnake(snake_body)
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    Paused = False
            if event.type == pygame.QUIT:
                running = False

        while not Paused and running:
            clock.tick(FPS)
            if not apple_eaten:
                ShowApple(apple_x, apple_y)
            else:  # Changing the apple's spot if it's eaten.
                CreateANewApple()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if movement_keys == "WASD":
                        CheckWASDMovement(event)
                    elif movement_keys == "Arrows":
                        CheckArrowsMovement(event)
                    if event.key == pygame.K_p:  # If the player is pressing 'p' button:
                        Paused = True
                        Pause() 
            WIN.fill(BLACK)
            DrawGrid()
            HandleSnakeMovement(DIRECTION)
            if timer > 100:  # Start showing the moving apples.
                if not moving_apples_on:
                    CreateMovingApples()
                HandleMovingApples()
            timer += 1


if __name__ == "__main__":
    Menu()

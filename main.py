import pygame
import random

class BodyPart:
    snake_size = 0

    def __init__(self, x=0, y=0, direction="Up"):
        self.x = x
        self.y = y
        self.direction = direction
        self.AddBodyPart()
        self.Head = False

    @classmethod
    def AddBodyPart(cls):
        cls.snake_size += 1


class Player():
    def __init__(self, name, score=0):
        self.name = name
        self.score = score




pygame.init()
FPS = 60
IMAGE_SIZE = 32
WIDTH, HEIGHT = 30 * IMAGE_SIZE, 20 * IMAGE_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (125, 125, 125)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
running = True
apple_eaten = True
Paused = False
Got_Username = False
moving_apples_on = True
movement_keys = ""
username = ""
timer = timer2 = 0
Textbox_Width = 300
Textbox_Height = 50
apple_x = apple_y = 0
moving_apples_x = random.randint(0, 29) * IMAGE_SIZE
moving_apples_y = random.randint(0, 19) * IMAGE_SIZE
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


# Head directions.
SNAKE_HEAD_DOWN = pygame.image.load("snake_head.png")
SNAKE_HEAD_RIGHT = pygame.transform.rotate(SNAKE_HEAD_DOWN, 90)
CURRENT_SNAKE_HEAD = SNAKE_HEAD_UP = pygame.transform.rotate(SNAKE_HEAD_DOWN, 180)
SNAKE_HEAD_LEFT = pygame.transform.rotate(SNAKE_HEAD_DOWN, 270)


def NewGameSetup():
    global running, timer, apple_eaten, Paused, Got_Username, body_coordinates, snake_body, CURRENT_SNAKE_HEAD, Movement_Status, DIRECTION
    running = True
    apple_eaten = True
    Paused = False
    Got_Username = False
    timer = 0
    Movement_Status = DIRECTION = "Up"
    BodyPart.snake_size = 0
    snake_x, snake_y = 14 * IMAGE_SIZE, 10 * IMAGE_SIZE
    head = BodyPart(snake_x, snake_y)
    head.Head = True
    part1 = BodyPart(snake_x, snake_y + 1 * IMAGE_SIZE)
    part2 = BodyPart(snake_x, snake_y + 2 * IMAGE_SIZE)
    part3 = BodyPart(snake_x, snake_y + 3 * IMAGE_SIZE)
    part4 = BodyPart(snake_x, snake_y + 4 * IMAGE_SIZE)
    snake_body = [head, part1, part2, part3, part4]
    body_coordinates = []
    for body_part in snake_body:
        body_coordinates.append((body_part.x, body_part.y))
    CURRENT_SNAKE_HEAD = SNAKE_HEAD_UP


def DrawGrid():
    for x in range(0, WIDTH, IMAGE_SIZE):
        for y in range(0, HEIGHT, IMAGE_SIZE):
            rect = pygame.Rect(x, y, IMAGE_SIZE, IMAGE_SIZE)
            pygame.draw.rect(WIN, GRAY, rect, 1)


def CreateANewApple():
    global apple_x, apple_y, apple_eaten
    apple_eaten = False
    apple_x = random.randint(0, 29) * IMAGE_SIZE
    apple_y = random.randint(0, 19) * IMAGE_SIZE


def ShowApple(x, y):
    WIN.blit(RED_APPLE, (x, y))
    pygame.display.update()


def CreateASnake(body):
    for body_part in body:
        if body_part == body[0]:
            WIN.blit(SNAKE_HEAD_UP, (body_part.x * IMAGE_SIZE, body_part.y * IMAGE_SIZE))
        else:
            WIN.blit(SNAKE_BODY, (body_part.x * IMAGE_SIZE, body_part.y * IMAGE_SIZE))


def GameOver(body_coordinates):
    global username
    explosion_sound = pygame.mixer.Sound("explosion_sound.wav")
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
    Records = open("Records.txt", 'a')
    Records.write(f"{username}\n{BodyPart.snake_size}\n")
    Records.close()
    Menu()
    pygame.quit()
    exit(1)


def AddBodyPart():
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


def CheckRules(body_coordinates):
    if body_coordinates[0][0] < 0 or body_coordinates[0][0] == WIDTH or body_coordinates[0][1] < 0 or \
            body_coordinates[0][1] == HEIGHT:  # Snake goes out of the screen.
        pygame.time.wait(500)
        GameOver(body_coordinates)
    for coordinate in body_coordinates:
        if body_coordinates.count(coordinate) > 1:
            GameOver(body_coordinates)


def HandleSnakeMovement(direction):
    global body_coordinates, apple_x, apple_y, apple_eaten, Movement_Status, timer2
    timer2+=1
    for index in range(len(body_coordinates) - 1, -1, -1):
        if index != 0:
            body_coordinates[index] = body_coordinates[index - 1]
        else:
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
    for (x, y) in body_coordinates:
        if (x, y) == body_coordinates[0]:
            WIN.blit(CURRENT_SNAKE_HEAD, (x, y))
        else:
            WIN.blit(SNAKE_BODY, (x, y))
    CheckRules(body_coordinates)
    pygame.time.wait(int(240 - timer/100))  # Determines the snake's movement speed.
    if body_coordinates[0] == (apple_x, apple_y):
        eating_sound = pygame.mixer.Sound("bite_sound.wav")
        eating_sound.play()
        AddBodyPart()
        apple_eaten = True


def CheckArrowsMovement(event):
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


def CheckWASDMovement(event):
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


def GetSettings():
    global Got_Username, username, movement_keys
    textbox = pygame.Rect(WIDTH / 2 - Textbox_Width / 2, HEIGHT / 2 - Textbox_Height / 2, Textbox_Width, Textbox_Height)
    user_window = pygame.display.set_mode((WIDTH, HEIGHT))
    while not Got_Username:
        user_window.fill(BLACK)
        pygame.draw.rect(user_window, WHITE, textbox)
        font = pygame.font.SysFont(None, 48)
        text = font.render(username, True, BLACK)
        message = font.render("Please enter your name:", True, WHITE)
        user_window.blit(message, (textbox.x - 42, textbox.y - 60))
        user_window.blit(text, (textbox.x + 5, textbox.y + 10))
        font = pygame.font.SysFont(None, 24)
        message = font.render("(Press 'Enter' to submit)", True, WHITE)
        user_window.blit(message, (textbox.x + 55, textbox.y + 70))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[0:-1]
                elif event.key == pygame.K_RETURN:
                    if username != "" and username != "\t" and username != " ":
                        Got_Username = True
                else:
                    username += event.unicode
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)
    # Choosing movement keys - "WASD" / Arrows.
    Got_Movement_Keys = False
    movement_keys = ""
    font = pygame.font.SysFont(None, 48)
    while not Got_Movement_Keys:
        user_window.fill(BLACK)
        message = font.render("Please choose your playing buttons:", True, WHITE)
        user_window.blit(message, (textbox.x - 130, textbox.y - 150))
        user_window.blit(WASD_IMAGE, (textbox.x + 200, textbox.y - 50))
        wasd_rect = pygame.Rect(textbox.x + 200, textbox.y - 50, 256, 256)
        user_window.blit(ARROWS_IMAGE, (textbox.x - 200, textbox.y - 50))
        arrows_rect = pygame.Rect(textbox.x - 200, textbox.y - 50, 256, 256)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if wasd_rect.collidepoint(pygame.mouse.get_pos()):
                    movement_keys = "WASD"
                    Got_Movement_Keys = True
                if arrows_rect.collidepoint(pygame.mouse.get_pos()):
                    movement_keys = "Arrows"
                    Got_Movement_Keys = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)
    font = pygame.font.SysFont(None, 80)
    for sec in range(3, 0, -1):
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
    while not Chose:
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
            if event.type == pygame.MOUSEBUTTONDOWN:
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


def Pause():
    global Paused
    PAUSE_IMAGE = pygame.image.load("pause-button.png")
    WIN.blit(PAUSE_IMAGE, (WIDTH/2 - 64, HEIGHT/2 - 64))
    pygame.display.update()
    while Paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    Paused = False
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)


def PrintLeaderboard():
    file1 = open("Records.txt", 'r')  # File of names and scores.
    file_data = file1.read().split('\n')
    file1.close()
    names_and_scores = {}
    for index in range(0, len(file_data)):
        if index%2 == 0:
            name = file_data[index]
        else:
            if name in names_and_scores.keys():
                if int(names_and_scores[name]) < int(file_data[index]):
                    names_and_scores[name] = int(file_data[index])
            else:
                names_and_scores[name] = int(file_data[index])
    sorted_data = {k: v for k, v in sorted(names_and_scores.items(), key=lambda v: v[1], reverse=True)}  # Sorts the scores in a descending order, so the highest are first.
    sorted_names = list(sorted_data.keys())
    sorted_scores = list(sorted_data.values())
    print(sorted_names)
    print(sorted_scores)
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
    # After we got the data - creating the window.
    Quit = False
    leaderboards_window = pygame.display.set_mode((WIDTH, HEIGHT))
    leaderboards_window.blit(RED_CARPET, (-60, 0))
    font = pygame.font.SysFont("arial", 72, True, True)
    text = font.render("Top 5 Players", True, WHITE)
    leaderboards_window.blit(text, (WIDTH / 2 - 235, HEIGHT/2 - 275))
    font = pygame.font.SysFont("arial", 20, True, True)
    menu_rect = pygame.Rect(20, 20, 200, 40)
    pygame.draw.rect(leaderboards_window, LIGHT_GRAY, menu_rect)
    text = font.render("Back to Main Menu", True, WHITE)
    leaderboards_window.blit(text, (28, 28))
    LEADERBOARDS_IMAGE = pygame.image.load("leaderboard.png")
    leaderboards_window.blit(LEADERBOARDS_IMAGE, (WIDTH/2-256, HEIGHT/2-220))
    try:
        font = pygame.font.SysFont(None, 45)
        text = font.render(first_name, True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 - 150, HEIGHT / 2 + 6))
        text = font.render(str(first_score), True, BLACK)
        leaderboards_window.blit(text, (WIDTH / 2 + 125, HEIGHT / 2 + 6))
        text = font.render("1.", True, BLACK)
        leaderboards_window.blit(text, (WIDTH/2-198, HEIGHT / 2 + 6))
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Quit = True
                if event.key == pygame.K_SPACE:
                    main()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(pygame.mouse.get_pos()):
                    Menu()


def CreateMovingApples():
    global moving_apples_x, moving_apples_y, moving_apples_on
    moving_apples_x = random.randint(0, 29) * IMAGE_SIZE
    moving_apples_y = random.randint(0, 19) * IMAGE_SIZE
    moving_apples_on = True


def HandleMovingApples():
    global moving_apples_x, moving_apples_y, body_coordinates, moving_apples_on, timer
    WIN.blit(TWO_APPLES_IMAGE, (moving_apples_x, moving_apples_y))
    if body_coordinates[0] == (moving_apples_x, moving_apples_y):
        bite_sound = pygame.mixer.Sound("bite_sound.wav")
        bite_sound.play()
        moving_apples_on = False
        AddBodyPart()
        AddBodyPart()
        timer = 0
    if timer % 5 == 0:
        dir = random.randint(1,8)  # 1 - Up, 2 - Down, 3 - Left, 4 - Right, 5 - UpRight, 6 - UpLeft, 7 - DownRight, 8 - DownLeft.
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






def main():
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
                    if event.key == pygame.K_p:
                        Paused = True
                        Pause()
            WIN.fill(BLACK)
            DrawGrid()
            HandleSnakeMovement(DIRECTION)
            if timer > 100:
                if not moving_apples_on:
                    CreateMovingApples()
                HandleMovingApples()
            timer += 1


if __name__ == "__main__":
    Menu()
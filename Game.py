import math
from math import cos, sin, radians
from OpenGL.GL import *
from OpenGL.GLUT import *
import threading
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

R, G, B = 0, 0, 0
player1_y, player2_y = 0, 0
player1_up = False
player1_down = False
player2_up = False
player2_down = False
player_speed = 5

player1_health = 10
player2_health = 10

player1_score = 0
player2_score = 0

wall_height = 220
wall_decrease_rate = 0.05  # Pixels per second

game_over = False
paused = False
show_menu = True

last_shot_time = {"player1": 0, "player2": 0}
cooldown = 0.5
bullets = []
bullet_speed = 10
sunYPosition = 600

controlLight = 0  # for backgroung changing


def decrease_walls():
    global wall_height
    while True:
        if not paused and wall_height > 0:
            wall_height -= wall_decrease_rate
        time.sleep(0.01)


def shoot_bullet(player, x, y, direction):
    global last_shot_time
    current_time = time.time()
    if current_time - last_shot_time[player] >= cooldown:
        bullets.append((x, y, direction))
        last_shot_time[player] = current_time


def check_bullet_collision():
    global bullets, player1_health, player2_health, player1_score, player2_score, game_over
    new_bullets = []
    for x, y, direction in bullets:
        if direction == 1:  # Player 1's bullet
            if 740 <= x <= 770 and player2_y + 30 <= y <= player2_y + 120:  # Check collision with Player 2's body
                player2_health -= 1
                player1_score += 1
                if player2_health <= 0:
                    game_over = True
                    print("Player 1 wins!")
                continue  # Skip adding this bullet
        elif direction == -1:  # Player 2's bullet
            if 30 <= x <= 60 and player1_y + 30 <= y <= player1_y + 120:
                player1_health -= 1
                player2_score += 1
                if player1_health <= 0:
                    game_over = True
                    print("Player 2 wins!")
                continue  # Skip adding this bullet
        new_bullets.append((x, y, direction))
    bullets = new_bullets


def move_bullets():
    global bullets
    if game_over:
        bullets = []
        return
    if paused:
        return
    new_bullets = []
    for x, y, direction in bullets:
        new_x = x + (bullet_speed * direction)
        if direction == -1 and y <= wall_height and x <= 680:
            continue
        elif direction == 1 and y <= wall_height and x >= 120:
            continue
        if 0 <= new_x <= 800:
            new_bullets.append((new_x, y, direction))
    bullets = new_bullets


def manage_bullets():
    while True:
        move_bullets()
        check_bullet_collision()
        time.sleep(0.01)


def draw_bullets():
    for x, y, _ in bullets:
        draw_circle(x, y, 5, size=3)


def draw_points(x, y, size, flag):
    global R, G, B
    glPointSize(size)
    glBegin(GL_POINTS)
    glColor3f(R, G, B)
    glVertex2f(x, y)
    glEnd()


def draw_line(X1, Y1, X2, Y2, size=2):
    dx = abs(X2 - X1)
    dy = abs(Y2 - Y1)
    sx = 1 if X2 > X1 else -1  # Step for x
    sy = 1 if Y2 > Y1 else -1  # Step for y
    if dy > dx:
        dx, dy = dy, dx
        steep = True
    else:
        steep = False
    d = 2 * dy - dx
    x, y = X1, Y1
    for _ in range(int(dx + 1)):
        draw_points(x, y, size, True)
        if d > 0:
            if steep:
                x += sx
            else:
                y += sy
            d -= 2 * dx
        if steep:
            y += sy
        else:
            x += sx
        d += 2 * dy


def draw_circle(x_centre, y_centre, r, size=2):
    x = r
    y = 0
    draw_points(x + x_centre, y + y_centre, size, False)
    if (r > 0):
        draw_points(x + x_centre, -y + y_centre, size, False)
        draw_points(y + x_centre, x + y_centre, size, False)
        draw_points(-y + x_centre, x + y_centre, size, False)
    P = 1 - r
    while x > y:
        y += 1
        if P <= 0:
            P = P + 2 * y + 1
        else:
            x -= 1
            P = P + 2 * y - 2 * x + 1
        if (x < y):
            break
        draw_points(x + x_centre, y + y_centre, size, False)
        draw_points(-x + x_centre, y + y_centre, size, False)
        draw_points(x + x_centre, -y + y_centre, size, False)
        draw_points(-x + x_centre, -y + y_centre, size, False)
        if x != y:
            draw_points(y + x_centre, x + y_centre, size, False)
            draw_points(-y + x_centre, x + y_centre, size, False)
            draw_points(y + x_centre, -x + y_centre, size, False)
            draw_points(-y + x_centre, -x + y_centre, size, False)


def draw_player1():
    global player1_y

    # 1. LEG
    # Left leg (Navy Blue)
    glColor3f(0.0, 0.0, 0.5)  # Navy Blue
    for x in range(30, 41):  # Filling left leg
        for y in range(player1_y + 40, player1_y + 71):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    # Right leg (Navy Blue)
    glColor3f(0.0, 0.0, 0.5)  # Navy Blue
    for x in range(40, 51):  # Filling right leg
        for y in range(player1_y + 40, player1_y + 71):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    # 2. Shoe
    # Left Shoe (Light Blue)
    glColor3f(0.678, 0.847, 0.902)  # Light Blue
    for x in range(30, 41):  # Filling left shoe
        for y in range(player1_y + 30, player1_y + 41):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    # Right Shoe (Light Blue)
    glColor3f(0.678, 0.847, 0.902)  # Light Blue
    for x in range(40, 51):  # Filling right shoe
        for y in range(player1_y + 30, player1_y + 41):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    # 3. Body (White)
    glColor3f(1.0, 1.0, 1.0)  # White
    for x in range(30, 51):  # Filling body
        for y in range(player1_y + 70, player1_y + 101):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    # 4. Head (Black)

    # 5. Hand (White)
    glColor3f(1.0, 1.0, 1.0)  # White
    for x in range(50, 61):  # Filling hand
        for y in range(player1_y + 90, player1_y + 101):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    # 6. Gun (Brown)
    glColor3f(0.65, 0.16, 0.16)  # Brown
    for x in range(60, 91):
        for y in range(player1_y + 80, player1_y + 101):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    # 7. Drawing the outlines
    # Left leg outline
    glColor3f(0.0, 0.0, 0.5)  # Navy Blue
    draw_line(30, player1_y + 40, 40, player1_y + 40)  # Bottom edge
    draw_line(40, player1_y + 40, 40, player1_y + 70)  # Right edge
    draw_line(30, player1_y + 70, 40, player1_y + 70)  # Top edge
    draw_line(30, player1_y + 70, 30, player1_y + 40)  # Left edge

    # Right leg outline
    draw_line(40, player1_y + 40, 50, player1_y + 40)  # Bottom edge
    draw_line(50, player1_y + 40, 50, player1_y + 70)  # Right edge
    draw_line(50, player1_y + 70, 40, player1_y + 70)  # Top edge
    draw_line(40, player1_y + 70, 40, player1_y + 40)  # Left edge

    # Left shoe outline
    draw_line(30, player1_y + 40, 40, player1_y + 40)  # Bottom edge
    draw_line(40, player1_y + 40, 40, player1_y + 30)  # Right edge
    draw_line(30, player1_y + 30, 40, player1_y + 30)  # Top edge
    draw_line(30, player1_y + 30, 30, player1_y + 40)  # Left edge

    # Right shoe outline
    draw_line(40, player1_y + 40, 50, player1_y + 40)  # Bottom edge
    draw_line(50, player1_y + 40, 50, player1_y + 30)  # Right edge
    draw_line(50, player1_y + 30, 40, player1_y + 30)  # Top edge
    draw_line(40, player1_y + 30, 40, player1_y + 40)  # Left edge

    # Body outline
    draw_line(30, player1_y + 70, 50, player1_y + 70)  # Bottom edge
    draw_line(50, player1_y + 70, 50, player1_y + 100)  # Right edge
    draw_line(50, player1_y + 100, 30, player1_y + 100)  # Top edge
    draw_line(30, player1_y + 100, 30, player1_y + 70)  # Left edge

    # Head outline
    glColor3f(controlLight, controlLight, controlLight)
    draw_circle1(40, 110 + player1_y, 10)

    # Hand outline
    draw_line(50, player1_y + 90, 60, player1_y + 90)  # Bottom edge
    draw_line(60, player1_y + 90, 60, player1_y + 100)  # Right edge
    draw_line(60, player1_y + 100, 50, player1_y + 100)  # Top edge
    draw_line(50, player1_y + 100, 50, player1_y + 90)  # Left edge

    # Gun outline
    draw_line(60, player1_y + 100, 90, player1_y + 100)  # Bottom edge
    draw_line(90, player1_y + 100, 95, player1_y + 90)  # Right edge
    draw_line(95, player1_y + 90, 65, player1_y + 95)  # Top edge
    draw_line(65, player1_y + 95, 65, player1_y + 80)  # Left edge
    draw_line(65, player1_y + 80, 60, player1_y + 80)  # Bottom edge of the gun handle
    draw_line(60, player1_y + 80, 60, player1_y + 100)  # Back edge of the gun


def draw_player2():
    global player2_y
    # 1. LEG
    # Left leg (Ash Grey)
    glColor3f(0.7, 0.7, 0.7)  # Ash Grey
    for x in range(760, 771):  # Left leg
        for y in range(player2_y + 40, player2_y + 71):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    # Right leg (Ash Grey)
    glColor3f(0.7, 0.7, 0.7)  # Ash Grey
    for x in range(750, 761):  # Right leg
        for y in range(player2_y + 40, player2_y + 71):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    # 2. Shoe
    # Left Shoe (Yellow)
    glColor3f(1.0, 1.0, 0.6)  # Yellow
    for x in range(760, 771):  # Left shoe
        for y in range(player2_y + 30, player2_y + 41):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    # Right Shoe (Yellow)
    glColor3f(1.0, 1.0, 0.6)  # Yellow
    for x in range(750, 761):  # Right shoe
        for y in range(player2_y + 30, player2_y + 41):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    # 3. Body (Red)
    glColor3f(1.0, 0.0, 0.0)  # Red
    for x in range(750, 771):  # Body
        for y in range(player2_y + 70, player2_y + 101):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    # 4. Head (Black)

    # 5. Hand (Red)
    glColor3f(1.0, 0.0, 0.0)  # Red
    for x in range(740, 751):  # Hand
        for y in range(player2_y + 90, player2_y + 101):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    # 6. Gun (Dark Brown)
    glColor3f(0.36, 0.25, 0.20)  # Dark Brown
    for x in range(710, 741):  # Gun
        for y in range(player2_y + 80, player2_y + 101):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    # 7. Drawing the outlines
    # Left leg outline
    glColor3f(0.7, 0.7, 0.7)  # Ash Grey
    draw_line(760, player2_y + 40, 770, player2_y + 40)  # Bottom edge
    draw_line(770, player2_y + 40, 770, player2_y + 70)  # Right edge
    draw_line(760, player2_y + 70, 770, player2_y + 70)  # Top edge
    draw_line(760, player2_y + 70, 760, player2_y + 40)  # Left edge

    # Right leg outline
    draw_line(750, player2_y + 40, 760, player2_y + 40)  # Bottom edge
    draw_line(760, player2_y + 40, 760, player2_y + 70)  # Right edge
    draw_line(760, player2_y + 70, 750, player2_y + 70)  # Top edge
    draw_line(750, player2_y + 70, 750, player2_y + 40)  # Left edge

    # Left shoe outline
    draw_line(760, player2_y + 40, 770, player2_y + 40)  # Bottom edge
    draw_line(770, player2_y + 40, 770, player2_y + 30)  # Right edge
    draw_line(760, player2_y + 30, 770, player2_y + 30)  # Top edge
    draw_line(760, player2_y + 30, 760, player2_y + 40)  # Left edge

    # Right shoe outline
    draw_line(750, player2_y + 40, 760, player2_y + 40)  # Bottom edge
    draw_line(760, player2_y + 40, 760, player2_y + 30)  # Right edge
    draw_line(760, player2_y + 30, 750, player2_y + 30)  # Top edge
    draw_line(750, player2_y + 30, 750, player2_y + 40)  # Left edge

    # Body outline
    draw_line(750, player2_y + 70, 770, player2_y + 70)  # Bottom edge
    draw_line(770, player2_y + 70, 770, player2_y + 100)  # Right edge
    draw_line(770, player2_y + 100, 750, player2_y + 100)  # Top edge
    draw_line(750, player2_y + 100, 750, player2_y + 70)  # Left edge

    # Head outline
    glColor3f(controlLight, controlLight, controlLight)
    draw_circle1(760, 110 + player2_y, 10)

    # Hand outline
    draw_line(740, player2_y + 90, 750, player2_y + 90)  # Bottom edge
    draw_line(750, player2_y + 90, 750, player2_y + 100)  # Right edge
    draw_line(750, player2_y + 100, 740, player2_y + 100)  # Top edge
    draw_line(740, player2_y + 100, 740, player2_y + 90)  # Left edge

    # Gun outline
    draw_line(710, player2_y + 100, 740, player2_y + 100)  # Bottom edge
    draw_line(740, player2_y + 100, 740, player2_y + 80)  # Right edge
    draw_line(740, player2_y + 80, 735, player2_y + 80)  # Top edge of the gun
    draw_line(735, player2_y + 80, 735, player2_y + 95)  # Left edge of the gun
    draw_line(735, player2_y + 95, 710, player2_y + 90)  # Gun handle connection
    draw_line(710, player2_y + 90, 710, player2_y + 100)  # Back edge of the gun


def getBackgroundColor(controlLight, reverse=False):
    colors = [
        (0.9, 0.6, 0.2),  # Light Orange
        (1.0, 1.0, 0.2),  # Yellow
        (0.9, 0.9, 0.7),  # Yellowish White
        (0.6, 0.8, 1.0),  # Light Sky Blue
        (0.1, 0.1, 0.5),  # Dark Navy Blue
        (0.0, 0.0, 0.0),  # Black
    ]

    # Reverse the color list if needed
    if reverse:
        colors = colors[::-1]
    num_stages = len(colors) - 1
    stage = min(int(controlLight * num_stages), num_stages - 1)
    stage_progress = (controlLight * num_stages) - stage

    # Interpolate between the two colors for the current stage
    r = colors[stage][0] + (colors[stage + 1][0] - colors[stage][0]) * stage_progress
    g = colors[stage][1] + (colors[stage + 1][1] - colors[stage][1]) * stage_progress
    b = colors[stage][2] + (colors[stage + 1][2] - colors[stage][2]) * stage_progress

    return r, g, b


def getSunColor(control):
    # Interpolates the sun's color from yellow (day) to black (night)
    yellow = [1.0, 1.0, 0.0]  # Sun's color during the day
    black = [0.0, 0.0, 0.0]  # Sun's color during the night
    r = yellow[0] * (1 - control) + black[0] * control
    g = yellow[1] * (1 - control) + black[1] * control
    b = yellow[2] * (1 - control) + black[2] * control
    return r, g, b


def draw_river():
    # draw_line(120, 450, 120, 500)  # Left edge
    # draw_line(120, 500, 150, 500)  # Top edge
    # draw_line(150, 500, 150, 450)  # Right edge
    glColor3f(1, 1, 1)
    # draw_line(0, 430, 800, 430)  # Bottom edge
    draw_line(0, 670, 800, 670)  # top edge


# FOR SUN
def draw_line1(X1, Y1, X2, Y2, size=2):
    dx = abs(X2 - X1)
    dy = abs(Y2 - Y1)
    sx = 1 if X2 > X1 else -1  # Step for x
    sy = 1 if Y2 > Y1 else -1  # Step for y
    if dy > dx:
        dx, dy = dy, dx
        steep = True
    else:
        steep = False
    d = 2 * dy - dx
    x, y = X1, Y1
    for _ in range(int(dx + 1)):
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()
        if d > 0:
            if steep:
                x += sx
            else:
                y += sy
            d -= 2 * dx
        if steep:
            y += sy
        else:
            x += sx
        d += 2 * dy


def draw_circle1(x_centre, y_centre, r, size=2):
    x = r
    y = 0
    P = 1 - r
    draw_line1(x_centre + x, y_centre, x_centre - x, y_centre, size)  # Horizontal line for the center
    draw_line1(x_centre, y_centre + x, x_centre, y_centre - x, size)  # Vertical line for the center
    while x > y:
        y += 1
        if P <= 0:
            P = P + 2 * y + 1 #gh
        else:
            x -= 1
            P = P + 2 * y - 2 * x + 1
        if x < y:
            break
        # Drawing octants
        draw_line1(x_centre + x, y_centre + y, x_centre - x, y_centre + y, size)
        draw_line1(x_centre + x, y_centre - y, x_centre - x, y_centre - y, size)
        draw_line1(x_centre + y, y_centre + x, x_centre - y, y_centre + x, size)
        draw_line1(x_centre + y, y_centre - x, x_centre - y, y_centre - x, size)


def draw_sun():
    global sunYPosition  # Use the global sun position
    # Get sun color based on the current day-night control
    r, g, b = getSunColor(controlLight)
    glColor3f(r, g, b)  # Set the sun color
    draw_circle1(600, sunYPosition, 30)  # Draw filled circle for the sun

    # Draw sun rays using Midpoint Line Algorithm
    for angle in range(0, 360, 15):  # 15-degree step for rays
        rad = angle * math.pi / 180.0
        x1 = 600 + 30 * math.cos(rad)  # Start point of the ray
        y1 = sunYPosition + 30 * math.sin(rad)
        x2 = 600 + 60 * math.cos(rad)  # End point of the ray
        y2 = sunYPosition + 60 * math.sin(rad)
        draw_line1(x1, y1, x2, y2)  # Draw each ray


def draw_walls():
    # Player 1 wall (Brick color)
    glColor3f(179 / 255, 91 / 255, 58 / 255)  # Brick color
    for x in range(120, 151):
        for y in range(0, int(wall_height)):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    glColor3f(179 / 255, 91 / 255, 58 / 255)  # Brick color
    draw_line(120, 0, 120, wall_height)  # Left edge
    draw_line(120, wall_height, 150, wall_height)  # Top edge
    draw_line(150, wall_height, 150, 0)  # Right edge
    draw_line(150, 0, 120, 0)  # Bottom edge

    draw_line(135, 0, 135, wall_height)  # mid line y
    draw_line(120, wall_height / 2, 150, wall_height / 2)
    draw_line(120, wall_height / 4, 150, wall_height / 4)
    draw_line(120, (wall_height - wall_height / 4), 150, (wall_height - wall_height / 4))
    #
    draw_line(120, wall_height / 8, 150, wall_height / 8)
    draw_line(120, (wall_height - wall_height / 8), 150, (wall_height - wall_height / 8))
    draw_line(120, ((wall_height - wall_height / 8) - wall_height / 2), 150,
              ((wall_height - wall_height / 8) - wall_height / 2))
    draw_line(120, ((wall_height - wall_height / 8) - wall_height / 4), 150,
              ((wall_height - wall_height / 8) - wall_height / 4))

    # Player 2 wall (Brick color)
    glColor3f(179 / 255, 91 / 255, 58 / 255)  # Brick color
    for x in range(650, 681):
        for y in range(0, int(wall_height)):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    glColor3f(179 / 255, 91 / 255, 58 / 255)  # Brick color
    draw_line(650, 0, 650, wall_height)
    draw_line(650, wall_height, 680, wall_height)
    draw_line(680, wall_height, 680, 0)
    draw_line(680, 0, 650, 0)
    #
    draw_line(665, 0, 665, wall_height)
    draw_line(650, wall_height / 2, 680, wall_height / 2)
    draw_line(650, wall_height / 4, 680, wall_height / 4)
    draw_line(650, (wall_height - wall_height / 4), 680, (wall_height - wall_height / 4))  # Three-quarters height line

    draw_line(650, wall_height / 8, 680, wall_height / 8)
    draw_line(650, (wall_height - wall_height / 8), 680, (wall_height - wall_height / 8))  # Three-eighths height line
    draw_line(650, ((wall_height - wall_height / 8) - wall_height / 2), 680,
              ((wall_height - wall_height / 8) - wall_height / 2))
    draw_line(650, ((wall_height - wall_height / 8) - wall_height / 4), 680,
              ((wall_height - wall_height / 8) - wall_height / 4))


def iterate():
    glViewport(0, 0, 800, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 800, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    draw_player1()
    draw_player2()
    draw_walls()
    draw_river()
    draw_sun()
    draw_bullets()

    draw_text(10, SCREEN_HEIGHT - 80, f"Score: {player1_score}", 0.15)
    draw_text(685, SCREEN_HEIGHT - 80, f"Score: {player2_score}", 0.15)
    draw_text(10, SCREEN_HEIGHT - 110, f"Health: {player1_health}/10", 0.15)
    draw_text(645, SCREEN_HEIGHT - 110, f"Health: {player2_health}/10", 0.15)

    draw_pause_button(20, SCREEN_HEIGHT - 40)
    draw_cross_button(SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40)
    draw_restart_button(SCREEN_WIDTH / 2 - 10, SCREEN_HEIGHT - 40)

    if game_over:
        if player1_score > player2_score:
            print(f"Player 1 wins with the score: {player1_score}")
            draw_text(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 40,
                      f"Player 1 wins with the score: {player1_score}", 0.3)
        else:
            print(f"Player 2 wins with the score: {player2_score}")
            draw_text(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 40,
                      f"Player 2 wins with the score: {player2_score}", 0.3)

        draw_text(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, "GAME OVER", 0.3)

    r, g, b = getBackgroundColor(controlLight)
    glClearColor(r, g, b, 1.0)

    glutSwapBuffers()


def redraw():
    if game_over or paused:
        return
    move_bullets()
    check_bullet_collision()
    glutPostRedisplay()


def move_player1():
    global player1_y, player1_up, player1_down
    while True:
        if player1_up:
            player1_y = min(480, player1_y + player_speed)
        if player1_down:
            player1_y = max(0, player1_y - player_speed)
        time.sleep(0.01)


def move_player2():
    global player2_y, player2_up, player2_down
    while True:
        if player2_up:
            player2_y = min(480, player2_y + player_speed)
        if player2_down:
            player2_y = max(0, player2_y - player_speed)
        time.sleep(0.01)


# Update keyboard listeners
def keyboardListener(key, x, y):
    global player1_up, player1_down, controlLight, sunYPosition
    if key == b'w':
        player1_up = True
    elif key == b's':
        player1_down = True
    elif key == b'd':
        shoot_bullet("player1", 90, 100 + player1_y, 1)

    # for backgroung change
    if key == b'n':
        print("Night++")
        if controlLight >= 1:
            controlLight = 1
        else:
            controlLight += 0.06
        sunYPosition -= 3
    if key == b'm':
        print("Day++")
        if controlLight <= 0:
            controlLight = 0
        else:
            controlLight -= 0.06
        sunYPosition += 3
    glutPostRedisplay()


def keyboardUpListener(key, x, y):
    global player1_up, player1_down
    if key == b'w':
        player1_up = False
    elif key == b's':
        player1_down = False


def specialKeyListener(key, x, y):
    global player2_up, player2_down
    if key == GLUT_KEY_UP:
        player2_up = True
    elif key == GLUT_KEY_DOWN:
        player2_down = True
    elif key == GLUT_KEY_LEFT:
        shoot_bullet("player2", 710, 100 + player2_y, -1)


def specialKeyUpListener(key, x, y):
    global player2_up, player2_down
    if key == GLUT_KEY_UP:
        player2_up = False
    elif key == GLUT_KEY_DOWN:
        player2_down = False


def draw_pause_button(x, y, size=20):
    if paused:
        # Draw play triangle
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 1.0, 1.0)
        glVertex2f(x, y)
        glVertex2f(x, y + size)
        glVertex2f(x + size, y + size / 2)
        glEnd()
    else:
        # Draw pause bars
        draw_line(x, y, x, y + size)
        draw_line(x + size / 2, y, x + size / 2, y + size)


def draw_cross_button(x, y, size=20):
    draw_line(x, y, x + size, y + size)
    draw_line(x, y + size, x + size, y)


def draw_restart_button(x, y, size=20):
    draw_circle(x + size / 2, y + size / 2, size / 2)
    # Draw arrow
    draw_line(x + size / 2, y + size, x + size, y + size / 2)
    draw_line(x + size, y + size / 2, x + size / 2, y)


def draw_text(x, y, text, scale=1.0):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(scale, scale, scale)
    glColor3f(1.0, 1.0, 1.0)
    for char in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
    glPopMatrix()


def mouseListener(button, state, x, y):
    global paused, show_menu, player1_health, player2_health, player1_score, player2_score, game_over
    if state == GLUT_DOWN:
        # Convert window coordinates to OpenGL coordinates
        y = SCREEN_HEIGHT - y

        # Check pause button (top left)
        if 20 <= x <= 40 and SCREEN_HEIGHT - 40 <= y <= SCREEN_HEIGHT - 20:
            paused = not paused

        # Check cross button (top right)
        if SCREEN_WIDTH - 40 <= x <= SCREEN_WIDTH - 20 and SCREEN_HEIGHT - 40 <= y <= SCREEN_HEIGHT - 20:
            glutLeaveMainLoop()

        # Check restart button (top middle)
        if SCREEN_WIDTH / 2 - 10 <= x <= SCREEN_WIDTH / 2 + 10 and SCREEN_HEIGHT - 40 <= y <= SCREEN_HEIGHT - 20:
            # Reset game state
            player1_health = 10
            player2_health = 10
            player1_score = 0
            player2_score = 0
            paused = False
            game_over = False


# Start threads
threading.Thread(target=move_player1, daemon=True).start()
threading.Thread(target=move_player2, daemon=True).start()
threading.Thread(target=move_player2, daemon=True).start()
threading.Thread(target=move_player2, daemon=True).start()
threading.Thread(target=manage_bullets, daemon=True).start()
threading.Thread(target=decrease_walls, daemon=True).start()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)  # window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Game!")  # window name
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutKeyboardUpFunc(keyboardUpListener)
glutSpecialUpFunc(specialKeyUpListener)
glutMouseFunc(mouseListener)
glutIdleFunc(redraw)
make_game_over = False
glutKeyboardFunc(keyboardListener)
glutMainLoop()

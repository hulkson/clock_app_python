import pygame, sys

from pygame.constants import KEYDOWN, K_p

class Ball:
    def __init__(self, screen, color, posX, posY, radius):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.radius = radius
        self.dx = 0
        self.dy = 0
        self.show()

    def show(self):
        pygame.draw.circle(self.screen, self.color, (self.posX, self.posY), self.radius)

    def start_moving(self):
        self.dx = 0.15
        self.dy = 0.05

    def move(self):
        self.posX += self.dx
        self.posY += self.dy

    def paddle_collision(self):
        self.dx = -self.dx

    def wall_collision(self):
        self.dy = -self.dy

    def restart_pos(self):
        self.posX = SCREEN_WIDTH // 2
        self.posY = SCREEN_HEIGHT // 2
        self.dx = 0
        self.dy = 0
        self.show()

class Paddle:
    def __init__(self, screen, color, posX, posY, width, height):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.state = 'stopped'
        self.show()

    def show(self):
        pygame.draw.rect(self.screen, self.color, (self.posX, self.posY, self.width, self.height))

    def move(self):
        if self.state == 'up':
            self.posY -= 0.5
   
        elif self.state == 'down':
            self.posY += 0.5

    def clamp(self):
        if self.posY <= 0:
            self.posY = 0
        
        if self.posY + self.height >= SCREEN_HEIGHT:
            self.posY = SCREEN_HEIGHT - self.height

    def restart_pos(self):
        self.posY = SCREEN_HEIGHT // 2 - self.height // 2
        self.state = 'stopped'
        self.show()

class Score:
    def __init__(self, screen, points, posX, posY):
        self.screen = screen
        self.points = points
        self.posX = posX
        self.posY = posY
        self.font = pygame.font.SysFont("monospace", 80, bold=True)
        self.label = self.font.render(self.points, 0, WHITE_COLOR)
        self.show()

    def show(self):
        self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY ))

    def increase_score(self):
        points = int(self.points) + 1
        self.points = str(points)
        self.label = self.font.render(self.points, 0, WHITE_COLOR)

    def restart_score(self):
        self.points= '0'
        self.label = self.font.render(self.points, 0, WHITE_COLOR)


class CollisionManager:
    def between_ball_and_paddle_left(self, ball, paddle_left):
        if ball.posY + ball.radius > paddle_left.posY and ball.posY - ball.radius < paddle_left.posY + paddle_left.height:
            if ball.posX - ball.radius <= paddle_left.posX + paddle_left.width:
                return True
        return False

    def between_ball_and_paddle_right(self, ball, paddle_right):
        if ball.posY + ball.radius > paddle_right.posY and ball.posY - ball.radius < paddle_right.posY + paddle_right.height:
            if ball.posX + ball.radius >= paddle_right.posX:
                return True
        return False

    def between_ball_and_wall(self, ball):
        # check top
        if ball.posY - ball.radius <= 0:
            return True
        
        # check bottom
        if ball.posY + ball.radius >= SCREEN_HEIGHT:
            return True

        return False

    def check_score1(self, ball):
        return ball.posX - ball.radius >= SCREEN_WIDTH

    def check_score2(self, ball):
        return ball.posX - ball.radius <= 0

pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
SCREEN_COLOR = (0, 0, 0)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(SCREEN_COLOR)
pygame.display.set_caption('PONG_GAME')

def paint_back():
    screen.fill(SCREEN_COLOR)
    pygame.draw.line(screen, WHITE_COLOR, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)


def restart_game():
    paint_back()
    score1.restart_score()
    score2.restart_score()
    ball.restart_pos()
    paddle_left.restart_pos()
    paddle_right.restart_pos()


paint_back()

# Object
ball = Ball(screen, WHITE_COLOR, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10)
paddle_left = Paddle(screen, WHITE_COLOR, 15, SCREEN_HEIGHT // 2 - 60, 20, 120)
paddle_right = Paddle(screen, WHITE_COLOR, SCREEN_WIDTH - 20 - 15, SCREEN_HEIGHT // 2 - 60, 20, 120)
collision = CollisionManager()
score1 = Score(screen, '0', SCREEN_WIDTH // 4, 15)
score2 = Score(screen, '0', SCREEN_WIDTH - SCREEN_WIDTH // 4, 15)

# variable
playing = False

# Mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                ball.start_moving()
                playing = True

            if event.key == pygame.K_r:
                restart_game()
                playing = False

            if event.key == pygame.K_w:
                paddle_left.state = 'up'
            if event.key == pygame.K_s:
                paddle_left.state = 'down'

            if event.key == pygame.K_UP:
                paddle_right.state = 'up'
            if event.key == pygame.K_DOWN:
                paddle_right.state = 'down'

        if event.type == pygame.KEYUP:
            paddle_left.state = 'stopped'
            paddle_right.state = 'stopped'

    if playing:
        paint_back()

        ball.move()
        ball.show()

        paddle_left.move()
        paddle_left.clamp()
        paddle_left.show()

        paddle_right.move()
        paddle_right.clamp()
        paddle_right.show()

        #check collision
        if collision.between_ball_and_paddle_left(ball, paddle_left):
            ball.paddle_collision()

        if collision.between_ball_and_paddle_right(ball, paddle_right):
            ball.paddle_collision()

        if collision.between_ball_and_wall(ball):
            ball.wall_collision()

        if collision.check_score1(ball):
            paint_back()
            score1.increase_score()
            ball.restart_pos()
            paddle_left.restart_pos()
            paddle_right.restart_pos()
            playing = False

        if collision.check_score2(ball):
            paint_back()
            score2.increase_score()
            ball.restart_pos()
            paddle_left.restart_pos()
            paddle_right.restart_pos()
            playing = False

    score1.show()
    score2.show()
    pygame.display.update()
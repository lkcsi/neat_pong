import pygame
from paddle import Paddle
from ball import Ball
pygame.init()

FPS = 60
WIDTH, HEIGHT = 700, 500
PADDING, PADDLE_WIDTH, PADDLE_HEIGHT = 10, 20, 100
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
SCORE_FONT = pygame.font.SysFont('comicsans', 50)

def draw_paddles(win, *paddles: Paddle):
    for paddle in paddles:
        pygame.draw.rect(win, BLACK, (paddle.x, paddle.y, paddle.width, paddle.height))

def draw_ball(win, ball:Ball):
    pygame.draw.circle(win, BLACK, (ball.x, ball.y), ball.radius)

def draw_scores(win, left_score, right_score):
    left_text = SCORE_FONT.render(f'{left_score}', 1, BLACK)
    right_text = SCORE_FONT.render(f'{right_score}', 1, BLACK)

    win.blit(left_text, (WIDTH//4 - left_text.get_width()//2, 20))
    win.blit(right_text, (WIDTH//4*3 - right_text.get_width()//2, 20))

def draw(**drawables):
    win = drawables['win']
    win.fill(WHITE)

    draw_scores(win, drawables['left_score'], drawables['right_score'])
    draw_paddles(win, drawables['left_paddle'], drawables['right_paddle'])
    draw_ball(win, drawables['ball'])

    pygame.display.update()

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - Paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + PADDLE_HEIGHT + Paddle.VEL <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - Paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + PADDLE_HEIGHT + Paddle.VEL <= HEIGHT:
        right_paddle.move(up=False)

def range_map(x1, x2, y1, y2, num):
    range_x = x2 - x1
    range_y = y2 - y1
    num = num - x1
    num = num / range_x * range_y

    return round(num + y1)

def get_y_vel(ball: Ball, paddle: Paddle):
    delta = ball.y - (paddle.y + paddle.height // 2)
    return range_map(PADDLE_HEIGHT // -2, PADDLE_HEIGHT // 2, -5, 5, delta) 

def start_ball(ball: Ball, left_won:bool):
    if(ball.x_vel == 0 and ball.y_vel == 0):
        if left_won: 
            ball.x_vel = Ball.MAX_VEL
        else: 
            ball.x_vel = -1 * Ball.MAX_VEL

def handle_ball_movement(ball: Ball, left_paddle: Paddle, right_paddle: Paddle):
    ball.move()

    if(ball.bottom() >= HEIGHT or ball.top() <= 0):
        ball.y_vel *= -1

    if(ball.x_vel < 0):
        if( ball.left() <= left_paddle.x + PADDLE_WIDTH and 
        ball.y >= left_paddle.y and 
        ball.y <= left_paddle.y + PADDLE_HEIGHT): 
            ball.x_vel *= -1
            ball.y_vel = get_y_vel(ball, left_paddle)

    elif(ball.right() >= right_paddle.x and 
        ball.y >= right_paddle.y and 
        ball.y <= right_paddle.y + PADDLE_HEIGHT):
            ball.x_vel *= -1
            ball.y_vel = get_y_vel(ball, right_paddle)

def reset(ball:Ball, *paddles:Paddle):
    ball.reset()
    for paddle in paddles:
        paddle.reset()

def main_loop():
    left_score, right_score = 0, 0
    left_won = False
    left_paddle = Paddle(PADDING, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - PADDING - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 10)
    win = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Pong")
    run = True
    clock = pygame.time.Clock()

    while(run):
        clock.tick(FPS)
        draw(win=win, ball=ball, 
             left_paddle=left_paddle, right_paddle=right_paddle, 
             left_score=left_score, right_score=right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            start_ball(ball, left_won)

        if(ball.left() <= 0):
            left_won = False
            right_score += 1
            reset(ball, left_paddle, right_paddle)

        if(ball.right() >= WIDTH):
            left_won = True
            left_score += 1
            reset(ball, left_paddle, right_paddle)

        handle_paddle_movement(keys, left_paddle, right_paddle)
        handle_ball_movement(ball, left_paddle, right_paddle)
    
    pygame.quit()

if __name__ == '__main__':
    main_loop()
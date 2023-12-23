import pygame
from pygame import Surface
from paddle import Paddle
from ball import Ball
from random import uniform, choice
from game_stats import GameStats
pygame.init()

class Game:
    WHITE, BLACK = (255, 255, 255), (0, 0, 0)
    SCORE_FONT = pygame.font.SysFont('comicsans', 50)

    def __init__(self, win:Surface):
        self.win = win
        self.width = win.get_width()
        self.height = win.get_height()
        pygame.display.set_caption("Pong")

        self.game_stats = GameStats()

        paddle_width = self.width // 40
        paddle_height = self.height // 5
        padding = self.width // 50
        radius = self.height // 50
        self.left_paddle = Paddle(padding, self.height // 2 - paddle_height // 2, paddle_width, paddle_height)
        self.right_paddle = Paddle(self.width - padding - paddle_width, self.height // 2 - paddle_height // 2, paddle_width, paddle_height)
        self.ball = Ball(self.width // 2, self.height // 2, radius)


    def _draw_paddles(self):
        pygame.draw.rect(self.win, self.BLACK, (self.left_paddle.x, self.left_paddle.y, self.left_paddle.width, self.left_paddle.height))
        pygame.draw.rect(self.win, self.BLACK, (self.right_paddle.x, self.right_paddle.y, self.right_paddle.width, self.right_paddle.height))

    def _draw_ball(self):
        pygame.draw.circle(self.win, self.BLACK, (self.ball.x, self.ball.y), self.ball.radius)

    def _draw_scores(self):
        stats = self.game_stats
        left_text = self.SCORE_FONT.render(f'{stats.left_score}', 1, self.BLACK)
        right_text = self.SCORE_FONT.render(f'{stats.right_score}', 1, self.BLACK)

        self.win.blit(left_text, (self.width//4 - left_text.get_width()//2, 20))
        self.win.blit(right_text, (self.width//4*3 - right_text.get_width()//2, 20))

    def _draw_hits(self):
        stats = self.game_stats
        text = self.SCORE_FONT.render(f'{stats.left_hit + stats.right_hit}', 1, self.BLACK)
        self.win.blit(text, (self.width//2 - text.get_width()//2, 20))

    def draw(self, hits=False):
        self.win.fill(self.WHITE)

        if hits:
            self._draw_hits()
        self._draw_scores()
        self._draw_paddles()
        self._draw_ball()

        pygame.display.update()

    def handle_left(self, up: bool):
        self._handle_paddle(self.left_paddle, up)
        
    def handle_right(self, up: bool):
        self._handle_paddle(self.right_paddle, up)

    def _handle_paddle(self, paddle: Paddle, up:bool):
        if up and paddle.y - Paddle.VEL >= 0:
            paddle.move(True)
        if not up and paddle.y + paddle.height + Paddle.VEL <= self.height:
            paddle.move(False)

    def _range_map(self, x1, x2, y1, y2, num):
        range_x = x2 - x1
        range_y = y2 - y1
        num = num - x1
        num = num / range_x * range_y

        return num + y1

    def _get_y_vel(self, paddle: Paddle):
        delta = self.ball.y - (paddle.y + paddle.height // 2)
        return self._range_map(paddle.height // -2, paddle.height // 2, -1 * Ball.MAX_VEL, Ball.MAX_VEL, delta) 

    def start_ball(self):
        if(self.ball.x_vel == 0 and self.ball.y_vel == 0):
            result = 0
            while(result == 0):
                result = uniform(-1 * Ball.MAX_VEL, Ball.MAX_VEL)
            self.ball.y_vel = result
            self.ball.x_vel = -1 * Ball.MAX_VEL

    def _handle_paddle_collision(self, paddle:Paddle):
        ball = self.ball

        ball.y_vel = self._get_y_vel(paddle)
        ball.x_vel *= -1

    def loop(self):
        stats = self.game_stats
        self.ball.move()
        self._handle_collision()
        if(self.ball.left() <= 0):
            stats.right_score += 1
            self.reset()

        if(self.ball.right() >= self.width):
            stats.left_score += 1
            self.reset()
        
        return self.game_stats

    def _handle_collision(self):
        stats = self.game_stats
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        if(ball.bottom() >= self.height or ball.top() <= 0):
            ball.y_vel *= -1

        if(ball.x_vel < 0):
            if( ball.left() <= left_paddle.x + left_paddle.width and
            ball.y >= left_paddle.y and 
            ball.y <= left_paddle.y + left_paddle.height): 
                self._handle_paddle_collision(left_paddle)
                stats.left_hit += 1

        elif(ball.right() >= right_paddle.x and
            ball.y >= right_paddle.y and 
            ball.y <= right_paddle.y + right_paddle.height):
                self._handle_paddle_collision(right_paddle)
                stats.right_hit += 1

    def reset(self):
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
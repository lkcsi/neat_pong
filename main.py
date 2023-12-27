import pygame, neat, os
from game import Game
from paddle import Paddle
import pickle
from game_stats import GameStats

class PongGame:
    FPS = 60

    def __init__(self, window):
        self.game = Game(window)
        self.game_stats = self.game.game_stats
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball

    def handle_keys(self, keys):
        game = self.game
        if keys[pygame.K_w]:
            game.handle_left(up=True)
        if keys[pygame.K_s]:
            game.handle_left(up=False)

        if keys[pygame.K_UP]:
            game.handle_right(up=True)
        if keys[pygame.K_DOWN]:
            game.handle_right(up=False)

        if keys[pygame.K_SPACE]:
            game.start_ball()

    def handle_ai(self, paddle:Paddle, net, handle):
        output = net.activate((paddle.y, self.ball.y, abs(paddle.x - self.ball.x)))
        decision = output.index(max(output))
        if decision == 1: handle(True)
        elif decision == 2: handle(False)

    def play(self, fps=60, display=True, left_net=None, right_net=None, end_condition=lambda : False):
        game = self.game
        clock = pygame.time.Clock()
        while(not end_condition()):
            if fps > 0:
                clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            if display:
                game.draw(True)
            game.loop()

            if left_net:
                self.handle_ai(self.left_paddle, left_net, game.handle_left)
            if right_net:
                self.handle_ai(self.right_paddle, right_net, game.handle_right)

            self.handle_keys(pygame.key.get_pressed())
            

def calculate_fitenss(genome_1, genome_2, stats:GameStats):
    genome_1.fitness += stats.left_hit
    genome_2.fitness += stats.right_hit

def eval_genomes(genomes, config):
    window = pygame.display.set_mode((1000, 850))
    for i, (genome_id_1, genome_1) in enumerate(genomes[:len(genomes)-1]):
        genome_1.fitness = 0
        net1 = neat.nn.FeedForwardNetwork.create(genome_1, config)
        for (genome_id_2, genome_2) in genomes[i+1:len(genomes)]:
            if genome_2.fitness == None: genome_2.fitness = 0
            pong = PongGame(window)
            net2 = neat.nn.FeedForwardNetwork.create(genome_2, config)
            pong.play(left_net=net1, right_net=net2, display=False, fps=0)
            calculate_fitenss(genome_1, genome_2, pong.game_stats, 
                              lambda : pong.game_stats.left_score == 1 or 
                              pong.game_stats.right_score == 1 or 
                              pong.game_stats.left_hit == 50)
    pygame.quit()

def test_best_network(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    win = pygame.display.set_mode((1000, 850))

    pong = PongGame(win)
    pong.play(right_net=winner_net)
    pygame.quit()

def run_neat(config):
    #load checkpoint
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-22')
    #new run
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))

    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    #checkpoint every 1 generation 
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_dir = os.path.join(local_dir, 'config.txt')

    print(config_dir)
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_dir)

    #run_neat(config)
    test_best_network(config)
    
    #window = pygame.display.set_mode((1000, 850))
    #pong = PongGame(window)
    #pong.play()
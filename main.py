import pygame, neat, os
from game import Game
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

    def play(self):
        game = self.game
        clock = pygame.time.Clock()
        run = True
        while(run):
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            game.draw(True)
            game.loop()
            self.handle_keys(pygame.key.get_pressed())
        
        pygame.quit()

    def test_ai(self, net):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            output = net.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            decision = output.index(max(output))
            if decision == 1: self.game.handle_right(True)
            elif decision == 2: self.game.handle_right(False)

            game_info = self.game.loop()
            self.handle_keys(pygame.key.get_pressed())
            self.game.draw()

    def train_ai(self, genome_1, genome_2, config):
        run = True
        net1 = neat.nn.FeedForwardNetwork.create(genome_1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome_2, config)

        self.game.start_ball()
        while(run):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            output_1 = net1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            decision_1 = output_1.index(max(output_1))
            if decision_1 == 1: self.game.handle_left(True)
            elif decision_1 == 2: self.game.handle_left(False)

            output_2 = net2.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            decision_2 = output_2.index(max(output_2))
            if decision_2 == 1: self.game.handle_right(True)
            elif decision_2 == 2: self.game.handle_right(False)

            #self.game.draw(True)
            stats = self.game.loop()

            if(stats.left_score >= 1 or stats.right_score >= 1 or stats.left_hit >= 50):
                self.calculate_fitenss(genome_1, genome_2, stats)
                break
            
    def calculate_fitenss(self, genome_1, genome_2, stats:GameStats):
        genome_1.fitness += stats.left_hit
        genome_2.fitness += stats.right_hit


def eval_genomes(genomes, config):
    window = pygame.display.set_mode((1000, 850))
    for i, (genome_id_1, genome_1) in enumerate(genomes[:len(genomes)-1]):
        genome_1.fitness = 0
        for (genome_id_2, genome_2) in genomes[i+1:len(genomes)]:
            if genome_2.fitness == None: genome_2.fitness = 0
            pong = PongGame(window)
            pong.train_ai(genome_1, genome_2, config)

def test_best_network(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    win = pygame.display.set_mode((1000, 850))

    pong = PongGame(win)
    pong.test_ai(winner_net)

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
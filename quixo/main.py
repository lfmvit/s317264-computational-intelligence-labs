from enhanced_game import EnhancedGame
from game import Game
from players import RandomPlayer, NoobPlayer, MinMaxFragger
from tqdm.auto import tqdm


n_wins = 0
for i in tqdm(range(100)):
    g = Game()
    player1 = MinMaxFragger(0,2)
    player2 = NoobPlayer(1)
    winner = g.play(player1, player2)
    if winner == 0:
        n_wins += 1
print(f"player 0 wins {n_wins} games out of 100")
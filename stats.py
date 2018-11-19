from farmer import *
import matplotlib.pyplot as plt

red_dice = Dice({"rabbit": 6, "sheep": 2, "pig": 2, "horse": 1, "fox": 1})
yellow_dice = Dice({"rabbit": 6, "sheep": 3, "pig": 1, "cow": 1, "wolf": 1})


def simulate_games(n, players, red_dice, yellow_dice, game):
    win_stats = [0 for i in range(len(players))]
    turns = []
    for i in range(n):
        num_of_turns = 0
        br = False
        while True:
            num_of_turns += 1
            for i in range(len(players)):
                if players[i].make_turn(red_dice, yellow_dice):
                    win_stats[i] += 1
                    br = True
                    break
            if br:
                break
        for player in players:
            player.reset()
        game.reset()
        turns.append(num_of_turns)
    avg_len = round(sum(turns) / n, 2)
    return win_stats, avg_len


def pie_chart(players, name, game, n):
    labels = ["Player" + str(i + 1) for i in range(len(players))]
    sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
    fig1, ax1 = plt.subplots()
    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    ax1.set_title(name + "\n\n Average length of game: " + str(avg_len))
    fig1.savefig(name + ".png")
    animals = []
    names = name.split("_")
    for name in names:
        animals.append(name)
    ax1.legend(wedges, animals,
               title="Players",
               loc="lower right")
    plt.show()


def error_chart_rabbit_horse(n):
    available = {"rabbit": 60, "sheep": 24, "pig": 20, "cow": 12, "horse": 6}
    game = Game(available)
    players = []
    players.extend([StrategyFavouriteAnimal("rabbit", game), StrategyFavouriteAnimal("horse", game)])

    x = []
    s1 = []
    s2 = []
    s3 = []
    for i in range(15):
        x.append(i * 10)
        game.default = {"rabbit": i * 10, "sheep": 24, "pig": 20, "cow": 12, "horse": 6}
        game.reset()
        sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
        s1.append(sizes[0])
        print(s1)
        sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
        s2.append(sizes[0])
        print(s2)
        sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
        s3.append(sizes[0])
        print(s3)
    bottom, middle, top = [], [], []
    for i in range(15):
        triple = list(map(lambda x: x / n * 100, sorted([s1[i], s2[i], s3[i]])))
        bottom.append(triple[0])
        middle.append(triple[1])
        top.append(triple[2])

    fig, ax = plt.subplots()
    ax.set_title("Rabbit vs horse  - " + str(n) + " games")
    ax.set_xlabel("Rabbits available")
    ax.set_ylabel("% of won games for rabbit player")
    plt.plot(x, bottom, 'k-', x, middle, 'k-', x, top, 'k-')
    plt.fill_between(x, bottom, top)
    plt.savefig("Rabbit vs horse - " + str(n) + ".png")
    plt.show()


def error_chart_rabbit_biggest(n):
    available = {"rabbit": 60, "sheep": 24, "pig": 20, "cow": 12, "horse": 6}
    game = Game(available)
    players = []
    players.extend([StrategyFavouriteAnimal("rabbit", game), StrategyBiggestAnimal(game)])

    x = []
    s1 = []
    s2 = []
    s3 = []
    for i in range(15):
        x.append(i * 10)
        game.default = {"rabbit": i * 10, "sheep": 24, "pig": 20, "cow": 12, "horse": 6}
        game.reset()
        sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
        s1.append(sizes[0])
        print(s1)
        sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
        s2.append(sizes[0])
        print(s2)
        sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
        s3.append(sizes[0])
        print(s3)
    bottom, middle, top = [], [], []
    for i in range(15):
        triple = list(map(lambda x: x / n * 100, sorted([s1[i], s2[i], s3[i]])))
        bottom.append(triple[0])
        middle.append(triple[1])
        top.append(triple[2])

    fig, ax = plt.subplots()
    ax.set_title("Rabbit vs biggest  - " + str(n) + " games")
    ax.set_xlabel("Rabbits available")
    ax.set_ylabel("% of won games for rabbit player")
    plt.plot(x, bottom, 'k-', x, middle, 'k-', x, top, 'k-')
    plt.fill_between(x, bottom, top)
    plt.savefig("Rabbit vs biggest - " + str(n) + ".png")
    plt.show()


def error_chart_simple(n):
    available = {"rabbit": 60, "sheep": 24, "pig": 20, "cow": 12, "horse": 6}
    game = Game(available)
    players = []
    players.extend([StrategyFavouriteAnimal("rabbit", game), StrategyFavouriteAnimal("sheep", game)])

    x = []
    s1 = []
    s2 = []
    s3 = []
    for i in range(15):
        x.append(i + 1)
        sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
        s1.append(sizes[0])
        print(s1)
        sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
        s2.append(sizes[0])
        print(s2)
        sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
        s3.append(sizes[0])
        print(s3)
    bottom, middle, top = [], [], []
    for i in range(15):
        triple = list(map(lambda x: x / n * 100, sorted([s1[i], s2[i], s3[i]])))
        bottom.append(triple[0])
        middle.append(triple[1])
        top.append(triple[2])

    fig, ax = plt.subplots()
    ax.set_title("Rabbit vs sheep - " + str(n) + " games")
    ax.set_xlabel("Nth series")
    ax.set_ylabel("% of won games for sheep rabbit")
    plt.plot(x, bottom, 'k-', x, middle, 'k-', x, top, 'k-')
    plt.fill_between(x, bottom, top)
    plt.savefig("Rabbit vs sheep  - " + str(n) + ".png")
    plt.show()


def line_chart_three_players(n):
    available = {"rabbit": 60, "sheep": 24, "pig": 20, "cow": 12, "horse": 6}
    game = Game(available)
    players = []
    players.extend([StrategyFavouriteAnimal("rabbit", game), StrategyFavouriteAnimal("sheep", game),
                    StrategyFavouriteAnimal("pig", game)])
    x = []
    y1 = []
    y2 = []
    y3 = []
    for i in range(30):
        x.append(i * 10)
        game.default = {"rabbit": i * 10, "sheep": 24, "pig": 20, "cow": 12, "horse": 6}
        game.reset()
        sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
        sizes = list(map(lambda x: x / n * 100, sizes))
        y1.append(sizes[0])
        y2.append(sizes[1])
        y3.append(sizes[2])
    fig, ax = plt.subplots()
    ax.set_title("Rabbit vs sheep vs pig  - " + str(n) + " games")
    ax.set_xlabel("Rabbits available")
    ax.set_ylabel("% of games won")
    plt.plot(x, y1, label="rabbit")
    plt.plot(x, y2, label="sheep")
    plt.plot(x, y3, label="pig")
    ax.legend()
    plt.savefig("Rabbit vs sheep vs pig - " + str(n) + ".png")
    plt.show()


def error_chart_advantage(n):
    available = {"rabbit": 60, "sheep": 24, "pig": 20, "cow": 12, "horse": 6}
    game = Game(available)
    players = []
    players.extend([StrategyAdvantage("rabbit", game),StrategyFavouriteAnimal("rabbit", game)])
    x = []
    s1 = []
    s2 = []
    s3 = []
    for i in range(10):
        x.append(i * 10)
        players[0].default = {"rabbit": i * 10, "sheep": 0, "pig": 0, "cow": 0, "horse": 0}
        players[0].reset()
        sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
        s1.append(sizes[0])
        print(s1)
        sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
        s2.append(sizes[0])
        print(s2)
        sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
        s3.append(sizes[0])
        print(s3)
    bottom, middle, top = [], [], []
    for i in range(10):
        triple = list(map(lambda x: x / n * 100, sorted([s1[i], s2[i], s3[i]])))
        bottom.append(triple[0])
        middle.append(triple[1])
        top.append(triple[2])

    fig, ax = plt.subplots()
    ax.set_title("Advantage vs normal  - " + str(n) + " games")
    ax.set_xlabel("Rabbits at the start of game")
    ax.set_ylabel("% of won games for advantaged player")
    plt.plot(x, bottom, 'k-', x, middle, 'k-', x, top, 'k-')
    plt.fill_between(x, bottom, top)
    plt.savefig("Advantage vs normal - " + str(n) + ".png")
    plt.show()


def pie_chart_three_players():
    available = {"rabbit": 60, "sheep": 24, "pig": 20, "cow": 12, "horse": 6}
    game = Game(available)
    players = []
    players.extend([StrategyFavouriteAnimal("rabbit", game), StrategyFavouriteAnimal("sheep", game),
                    StrategyFavouriteAnimal("pig", game)])
    name = "Rabbit_sheep_pig"
    pie_chart(players, name, game, 1000)


def generate_all_charts():
    # error_chart_rabbit_horse(1000)
    # error_chart_rabbit_biggest(1000)
    error_chart_advantage(1000)
    # pie_chart_three_players()
    # line_chart_three_players(1000)


generate_all_charts()

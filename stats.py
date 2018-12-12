from farmer import *
import matplotlib.pyplot as plt

red_dice = Dice({"rabbit": 6, "sheep": 2, "pig": 2, "horse": 1, "fox": 1})
yellow_dice = Dice({"rabbit": 6, "sheep": 3, "pig": 1, "cow": 1, "wolf": 1})


def simulate_games(n, players, dice_red, dice_yellow, game):
    win_stats = [0 for _ in range(len(players))]
    turns = []
    for i in range(n):
        num_of_turns = 0
        br = False
        while True:
            num_of_turns += 1
            for j in range(len(players)):
                if players[j].make_turn(dice_red, dice_yellow):
                    win_stats[j] += 1
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
    wedges, texts, auto_texts = ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
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


def triple_simulation(n, game, players):
    values = []
    for i in range(3):
        sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
        values.append(sizes[0])
    return values


def error_chart(n, game, players):
    x = []
    sizes = [[], [], []]
    for i in range(15):
        x.append(i * 10)
        game.default = {"rabbit": i * 10, "sheep": 24, "pig": 20, "cow": 12, "horse": 6}
        game.reset()
        values = triple_simulation(n, game, players)
        for j in range(3):
            sizes[j].append(values[j])
    bottom, middle, top = convert_to_percent(n, 15, sizes)
    return bottom, middle, top, x


def convert_to_percent(n, y_labels_count, sizes):
    bottom, middle, top = [], [], []
    for i in range(y_labels_count):
        triple = list(map(lambda x: x / n * 100, sorted([sizes[0][i], sizes[1][i], sizes[2][i]])))
        bottom.append(triple[0])
        middle.append(triple[1])
        top.append(triple[2])
    return bottom, middle, top


def error_chart_rabbit_horse(n):
    game = Game()
    players = [StrategyFavouriteAnimal("rabbit", game), StrategyFavouriteAnimal("horse", game)]

    bottom, middle, top, x = error_chart(n, game, players)

    fig, ax = plt.subplots()
    ax.set_title("Rabbit vs horse  - " + str(n) + " games")
    ax.set_xlabel("Rabbits available")
    ax.set_ylabel("% of won games for rabbit player")
    plt.plot(x, bottom, 'k-', x, middle, 'k-', x, top, 'k-')
    plt.fill_between(x, bottom, top)
    plt.savefig("Rabbit vs horse - " + str(n) + ".png")
    plt.show()


def error_chart_rabbit_biggest(n):
    game = Game()
    players = [StrategyFavouriteAnimal("rabbit", game), StrategyBiggestAnimal(game)]

    bottom, middle, top, x = error_chart(n, game, players)

    fig, ax = plt.subplots()
    ax.set_title("Rabbit vs biggest  - " + str(n) + " games")
    ax.set_xlabel("Rabbits available")
    ax.set_ylabel("% of won games for rabbit player")
    plt.plot(x, bottom, 'k-', x, middle, 'k-', x, top, 'k-')
    plt.fill_between(x, bottom, top)
    plt.savefig("Rabbit vs biggest - " + str(n) + ".png")
    plt.show()


def error_chart_simple(n):
    game = Game()
    players = [StrategyFavouriteAnimal("rabbit", game), StrategyFavouriteAnimal("sheep", game)]

    x = []
    sizes = [[], [], []]
    for i in range(15):
        x.append(i + 1)
        values = triple_simulation(n, game, players)
        for j in range(3):
            sizes[j].append(values[j])
    bottom, middle, top = convert_to_percent(n, 15, sizes)
    fig, ax = plt.subplots()
    ax.set_title("Rabbit vs sheep - " + str(n) + " games")
    ax.set_xlabel("Nth series")
    ax.set_ylabel("% of won games by rabbit")
    plt.plot(x, bottom, 'k-', x, middle, 'k-', x, top, 'k-')
    plt.fill_between(x, bottom, top)
    plt.savefig("Rabbit vs sheep  - " + str(n) + ".png")
    plt.show()


def line_chart_three_players(n):
    game = Game()
    players = [StrategyFavouriteAnimal("rabbit", game), StrategyFavouriteAnimal("sheep", game),
               StrategyFavouriteAnimal("pig", game)]
    x = []
    y_axes = [[], [], []]
    for i in range(30):
        x.append(i * 10)
        game.default = {"rabbit": i * 10, "sheep": 24, "pig": 20, "cow": 12, "horse": 6}
        game.reset()
        sizes, avg_len = simulate_games(n, players, red_dice, yellow_dice, game)
        sizes = list(map(lambda x: x / n * 100, sizes))
        for j in range(3):
            y_axes[j].append(sizes[j])
    fig, ax = plt.subplots()
    ax.set_title("Rabbit vs sheep vs pig  - " + str(n) + " games")
    ax.set_xlabel("Rabbits available")
    ax.set_ylabel("% of games won")
    plt.plot(x, y_axes[0], label="rabbit")
    plt.plot(x, y_axes[1], label="sheep")
    plt.plot(x, y_axes[2], label="pig")
    ax.legend()
    plt.savefig("Rabbit vs sheep vs pig - " + str(n) + ".png")
    plt.show()


def error_chart_advantage(n):
    game = Game()
    players = [StrategyAdvantage("rabbit", game), StrategyFavouriteAnimal("rabbit", game)]
    x = []
    sizes = [[], [], []]
    for i in range(10):
        x.append(i * 10)
        players[0].default = {"rabbit": i * 10, "sheep": 0, "pig": 0, "cow": 0, "horse": 0}
        players[0].reset()
        values = triple_simulation(n, game, players)
        for j in range(3):
            sizes[j].append(values[j])
    bottom, middle, top = convert_to_percent(n, 10, sizes)
    fig, ax = plt.subplots()
    ax.set_title("Advantage vs normal  - " + str(n) + " games")
    ax.set_xlabel("Rabbits at the start of game")
    ax.set_ylabel("% of won games for advantaged player")
    plt.plot(x, bottom, 'k-', x, middle, 'k-', x, top, 'k-')
    plt.fill_between(x, bottom, top)
    plt.savefig("Advantage vs normal - " + str(n) + ".png")
    plt.show()


def pie_chart_three_players(n):
    game = Game()
    players = []
    players.extend([StrategyFavouriteAnimal("rabbit", game), StrategyFavouriteAnimal("sheep", game),
                    StrategyFavouriteAnimal("pig", game)])
    name = "Rabbit_sheep_pig"
    pie_chart(players, name, game, n)


line_chart_three_players(100)

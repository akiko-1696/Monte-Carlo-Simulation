import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


STARTING_BANKROLL = 1000
N_FLIPS = 100
N_UNIVERSES = 10000

CONSERVATIVE = 0.10
KELLY = 0.20
AGGRESSIVE = 0.50
RANDOM_SEED = 42

def single_bet(bankroll, fraction, p_win=0.6):
    bet_size = bankroll * fraction

    if random.random() < p_win:
        bankroll = bankroll + bet_size
    else:
        bankroll = bankroll - bet_size

    return bankroll



def simulate_path(bankroll,fraction,n_flips):
    history = [bankroll]
    for _ in range(n_flips):

        bankroll = single_bet(bankroll, fraction)
        history.append(bankroll)

    return history

def monte_carlo(starting_bankroll,fraction,n_flips,n_universes):
    bankrolls = []
    for _ in range(n_universes):
        path = simulate_path(starting_bankroll,fraction,n_flips)
        bankrolls.append(path[-1])
    
    return bankrolls



def probability_of_profit(results):
    return sum(x > STARTING_BANKROLL for x in results) / len(results)


def main():

    random.seed(RANDOM_SEED)
    path_10 = simulate_path(STARTING_BANKROLL, CONSERVATIVE, N_FLIPS)
    random.seed(RANDOM_SEED)
    path_20 = simulate_path(STARTING_BANKROLL, KELLY, N_FLIPS)
    random.seed(RANDOM_SEED)
    path_50 = simulate_path(STARTING_BANKROLL, AGGRESSIVE, N_FLIPS)

    results_10 = monte_carlo(STARTING_BANKROLL, CONSERVATIVE, N_FLIPS, N_UNIVERSES)
    results_20 = monte_carlo(STARTING_BANKROLL, KELLY, N_FLIPS, N_UNIVERSES)
    results_50 = monte_carlo(STARTING_BANKROLL, AGGRESSIVE, N_FLIPS, N_UNIVERSES)


    data = {
        "Strategy": ["10%", "Kelly", "50%"],
        "Mean": [
            np.mean(results_10),
            np.mean(results_20),
            np.mean(results_50)
        ],
        "Median": [
            np.median(results_10),
            np.median(results_20),
            np.median(results_50)
        ],
        "Profit Probability": [
            probability_of_profit(results_10),
            probability_of_profit(results_20),
            probability_of_profit(results_50)
        ]
    }

    df = pd.DataFrame(data)

    print(df)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].hist(results_10, bins=50)
    axes[0].set_title("10%")

    axes[1].hist(results_20, bins=50)
    axes[1].set_title("Kelly")

    axes[2].hist(results_50, bins=50)
    axes[2].set_title("50%")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
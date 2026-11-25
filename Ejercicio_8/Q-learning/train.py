from environement import *
import random
#Parameters
ALPHA = 0.5
GAMMA = 1.0
EPSILON = 0.1
N_EPISODES = 500
MAX_PASSO = 200
SEED = 42

N_ROW = 4
N_COLUMN = 12

MOVES = list(ACTION.keys())

def empty_q (): 
    q= {}
    for row in range(N_ROW) : 
        for column in range(N_COLUMN) : 
            case = (row, column)
            if is_cliff(case) or case == FINISH : 
                continue
            q[case] = [0.0] * len(ACTION)
    return q

def best_move(q , case) : 
    moves = q[case]
    best = moves[0]
    idx = 0
    for i in range(1, len(moves)) : 
        if moves[i] > best : 
            best = moves[i]
            idx = i
    return idx

def epsilon_greedy(q, case, epsilon):
    if random.random() < epsilon:
        return random.randrange(len(ACTION))
    return best_move(q, case)

def train(n_seed = SEED) : 
    random.seed(n_seed)
    q = empty_q()
    award = []

    for _ in range(N_EPISODES) : 
        case = START
        total = 0 
        for _ in range(MAX_PASSO) : 
            a = epsilon_greedy(q, case, EPSILON)
            new_case, r, state = step(case, MOVES[a])
 
            # Cible Q-learning : r + gamma * max Q(s', .), et 0 si s' est G
            if state:
                futur = 0.0
            else:
                futur = max(q[new_case])
            cible = r + GAMMA * futur
            q[case][a] += ALPHA * (cible - q[case][a])
 
            total += r
            case = new_case
            if state:
                break
        award.append(total)
 
    return q, award


def evaluate(q):
    """Greedy run from START (epsilon = 0). Returns (path, steps, return)."""
    case = START
    path = []
    total = 0
    for _ in range(MAX_PASSO):
        a = best_move(q, case)
        path.append(MOVES[a])
        case, r, state = step(case, MOVES[a])
        total += r
        if state:
            break
    return path, len(path), total
 
 
def print_policy(q):
    arrows = {"N": "↑", "E": "→", "S": "↓", "W": "←"}
    for row in range(N_ROW):
        line = []
        for column in range(N_COLUMN):
            case = (row, column)
            if case == FINISH:
                line.append("G")
            elif is_cliff(case):
                line.append("C")
            else:
                line.append(arrows[MOVES[best_move(q, case)]])
        print(" ".join(line))
 
 
def moving_average(series, k=10):
    result = []
    for i in range(len(series)):
        window = series[max(0, i - k + 1): i + 1]
        result.append(sum(window) / len(window))
    return result
 
 
if __name__ == "__main__":
    q, award = train()
 
    print(f"Seed: {SEED}")
    print(f"Parameters: alpha={ALPHA}, gamma={GAMMA}, epsilon={EPSILON}, "
          f"episodes={N_EPISODES}, max steps={MAX_PASSO}")
    print("Tie-breaking: first of N, E, S, W")
    print()
 
    path, steps, total = evaluate(q)
    print("Greedy policy:")
    print_policy(q)
    print()
    print("Path from START:", ", ".join(path))
    print("Steps:", steps)
    print("Greedy return:", total)
    print()
 
    avg = moving_average(award, 10)
    print("Reward per training episode:")
    print("  first 5:", award[:5])
    print("  last 5:", award[-5:])
    print(f"  final moving average (10 episodes): {avg[-1]:.1f}")
 
    import matplotlib.pyplot as plt
 
    plt.figure(figsize=(9, 5))
    plt.plot(award, alpha=0.35, label="reward per episode")
    plt.plot(avg, label="moving average (10 episodes)")
    plt.axhline(-13, color="gray", linestyle="--", label="optimal policy (-13)")
    plt.ylim(-200, 0)
    plt.xlabel("Episode")
    plt.ylabel("Cumulative reward")
    plt.title(f"Q-learning on Cliff Walking (seed {SEED})")
    plt.legend()
    plt.tight_layout()
    plt.savefig("q_learning_curve.png", dpi=150)
    print("\nPlot saved: q_learning_curve.png")
 



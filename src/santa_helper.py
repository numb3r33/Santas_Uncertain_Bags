import numpy as np

def horse_weight_distribution(sample_size):
    horse_draws = np.random.normal(loc=5.0, scale=2.0, size=sample_size)
    return np.array([max(0, val) for val in horse_draws])

def ball_weight_distribution(sample_size):
    ball_draws = 1 + np.random.normal(1, 0.3, sample_size)
    return np.array([max(0, val) for val in ball_draws])

def bike_weight_distribution(sample_size):
    bike_draws =  np.random.normal(20, 10, sample_size)
    return np.array([max(0, val) for val in bike_draws])

def train_weight_distribution(sample_size):
    train_draws = np.random.normal(10, 5, sample_size)
    return np.array([max(0, val) for val in train_draws])

def coal_weight_distribution(sample_size):
    return 47 * np.random.beta(0.5, 0.5, sample_size)

def book_weight_distribution(sample_size):
    return np.random.chisquare(2,sample_size)

def doll_weight_distribution(sample_size):
    return np.random.gamma(5,1, sample_size)

def block_weight_distribution(sample_size):
    return np.random.triangular(5,10,20,sample_size)

def gloves_weight_distribution(sample_size):
    return np.array([3.0 + np.random.rand(1)[0] if np.random.rand(1) < 0.3 else np.random.rand(1)[0] for i in range(sample_size)])

def draw_distributions(gift_type, sample_size=1000):
    if gift_type == 'horse':
        return horse_weight_distribution(sample_size)
    elif gift_type == 'ball':
        return ball_weight_distribution(sample_size)
    elif gift_type == 'bike':
        return bike_weight_distribution(sample_size)
    elif gift_type == 'train':
        return train_weight_distribution(sample_size)
    elif gift_type == 'coal':
        return coal_weight_distribution(sample_size)
    elif gift_type == 'book':
        return book_weight_distribution(sample_size)
    elif gift_type == 'doll':
        return doll_weight_distribution(sample_size)
    elif gift_type == 'blocks':
        return block_weight_distribution(sample_size)
    else:
        return gloves_weight_distribution(sample_size)

def parse_gift_type(gifts):
    """
    Name of the gift is made up of giftType_counter, so if we split
    by the `underscore` then first part would give us the type of the gift
    and second part would give us the counter.
    """
    return gifts.GiftId.map(lambda x: x.split('_')[0])

def generate_weights(gifts, gift_types=None):
    """
    Given dataframe gifts generate weights of the individual gifts based on the
    gift type.
    """

    def calculate_std(gift_types):
        return {gift_type:np.std(draw_distributions(gift_type)) for gift_type in gift_types}

    gifts['gift_type'] = parse_gift_type(gifts)

    if gift_types is not None:
        mask = gifts.gift_type.isin(gift_types)
        gifts = gifts.loc[mask]

    weights         = []
    std_by_type     = calculate_std(gifts.gift_type.unique())

    for gift_type in gifts['gift_type'].values:
        samples = draw_distributions(gift_type, sample_size=1)
        weights.append(samples[0])

    gifts['weights'] = np.array(weights)
    gifts['std']     = list(map(lambda x: std_by_type[x], gifts['gift_type']))

    return gifts


def prepare_solution(filename, solution):
    solution_file_path = '../submissions/%s.csv'%(filename)

    with open(solution_file_path, 'w') as outfile:
        outfile.write('Gifts\n')

        for sol in solution:
            if len(sol) >= 3:
                outfile.write(' '.join(sol))
                outfile.write('\n')

        outfile.close()

import numpy as np


def sample_horse(size=1):
	return np.maximum(0, np.random.normal(5,2,size))

def sample_ball(size=1):
	return np.maximum(0, 1 + np.random.normal(1,0.3,size))

def sample_bike(size=1):
	return np.maximum(0, np.random.normal(20,10,size))

def sample_train(size=1):
	return np.maximum(0, np.random.normal(10,5,size))

def sample_coal(size=1):
	return 47 * np.random.beta(0.5,0.5,size)

def sample_book(size=1):
	return np.random.chisquare(2,size)

def sample_doll(size=1):
	return np.random.gamma(5,1,size)

def sample_block(size=1):
	return np.random.triangular(5,10,20,size)

def sample_gloves(size=1):
	dist1 = 3.0 + np.random.rand(size)
	dist2 = np.random.rand(size)
	toggle = np.random.rand(size) < 0.3
	dist2[toggle] = dist1[toggle]
	return dist2

samplers = {
	"horse": sample_horse,
	"ball": sample_ball,
	"bike": sample_bike,
	"train": sample_train,
	"coal": sample_coal,
	"book": sample_book,
	"doll": sample_doll,
	"blocks": sample_block,
	"gloves": sample_gloves
}


gift_types = ['ball', 'bike', 'blocks', 'book',\
			  'coal', 'doll', 'gloves', 'horse',\
			  'train']

def sample(index, quantity=1, size=1):
	"""
	Use the sampling method for a gift type to generate samples
	from the underlying distribution.

	Also takes quantity and size as the parameters which represent
	how many iterations should we consider and what should be the sample size for each of
	the iteration.
	"""
	return np.sum(samplers[gift_types[index]](quantity * size).reshape(quantity, size), axis=0)

def create_bag_weight_sampler(bag):
	"""
	Takes in a configuration for a bag and returns a sampler
	and the string representation of the bag.
	"""
	def bag_weight_sampler(size=1):
		"""
		Takes in the number of samples to consider and returns
		estimated weight based on the configuration and number of
		samples considered.
		"""
		weight = np.array([0.0]*size)

		for i in range(len(bag)):
			weight += sample(i, bag[i], size)

		return weight

	return bag_weight_sampler


def custom_sample(gift_type, quantity=1, size=1):
	"""
	Use the sampling method for a gift type to generate samples
	from the underlying distribution.

	Also takes quantity and size as the parameters which represent
	how many iterations should we consider and what should be the sample size for each of
	the iteration.
	"""
	return np.sum(samplers[gift_type](quantity * size).reshape(quantity, size), axis=0)


def bag_name(bag):
	return str(list(map(lambda gift: "{}({})".format(gift, bag[gift]), sorted(bag.keys()))))

def create_bag_weight_custom_sampler(bag):
	def bag_weight_sampler(size=1):
		weight = np.array([0.0]*size)
		for gift in sorted(bag.keys()):
			weight += custom_sample(gift, bag[gift], size)
		return weight
	return bag_weight_sampler, bag_name(bag)



def create_bag_utility_sampler(bag):
	bag_weight_sampler, bag_name = create_bag_weight_custom_sampler(bag)
	def bag_utility_sampler(size=1):
		samples = bag_weight_sampler(size)
		samples[samples > 50] = 0 # clip all those samples where weight > 50 ( dangerous )
		return samples
	return bag_utility_sampler, bag_name


def get_bag_utility_distributions(candidate_bags):
	distributions = []
	size = len(candidate_bags)
	for i, candidate_bag in enumerate(candidate_bags):
		if i % 7000 == 0:
			print("{:.4f}\r".format(float(i) / float(size)))
		distributions.append(get_bag_utility_distribution(candidate_bag))
	print("")
	return np.vstack(distributions)



def get_bag_utility_distribution(candidate_bag):
	bag = { gift_types[i]: int(candidate_bag[i]) for i in range(len(gift_types)) if candidate_bag[i] > 0 }
	sampler, name = create_bag_utility_sampler(bag)
	sample = sampler(1000)
	return np.mean(sample), np.var(sample)






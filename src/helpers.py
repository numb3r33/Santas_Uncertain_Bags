import numpy as np

def sort_std_weights(gifts_with_weights):
	"""
	Sort the gifts in ascending order of the sample std and descending order of the sample value
	of the distribution they came from.
	"""
	return gifts_with_weights.sort_values(by=['std', 'weights'], ascending=[True, False])

def sort_weights_std(gifts_with_weights):
	return gifts_with_weights.sort_values(by=['weights', 'std'], ascending=[False, True])


def index_to_name(solution, names):
	solution_with_names = []

	for sol in solution:
		solution_with_names.append(list(map(lambda x: names[x], sol)))

	return solution_with_names


def num_not_filled(solution):
	return len([sol for sol in solution if len(sol) == 0])



def solution_weight(solution, weight_mapping):
	total_weight = 0

	for sol in solution:
		total_weight += np.sum(list(map(lambda x: weight_mapping.iloc[x], sol)))
	return total_weight

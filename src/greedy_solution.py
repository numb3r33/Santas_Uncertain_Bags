def bag_solution(gifts, is_available):

	for i in range(len(gifts)):
		if not is_available[i]:
			continue

		possible_solution = [i]
		current_weight    = gifts[i]

		for j in range(i + 1, len(gifts)):
			if (is_available[j]) and (current_weight + gifts[j] <= 50):
				possible_solution.append(j)
				current_weight += gifts[j]

		if len(possible_solution) >= 3:
			return possible_solution

	return [] # no solution could be found

def multi_bag_solution(gifts, n_bags, verbose=False):
	"""
	Notes:
	Items should be a copy of the original items as this we would get modified.

	Parameters:
	-----------

	gifts: array of weights for each of the items
	n_bags: number of bags to fill.
	"""

	def mark_unavailable(is_available, solution_indices):
		for idx in solution_indices:
			is_available[idx] = False

		return is_available

	def print_solution(weights, indices):
		if len(indices) == 0:
			print('No solution')
		else:
			print(', '.join([str(weights[idx]) for idx in indices]))

	configuration = []
	is_available  = [True] * len(gifts)

	for bag_index in range(n_bags):
		solution_indices = bag_solution(gifts, is_available) # this can return an empty list.

		if verbose:
			print_solution(gifts, solution_indices)

		configuration.append(solution_indices)
		is_available    = mark_unavailable(is_available, solution_indices)

	return configuration


def can_accept(configuration):
	"""
	Checks whether all of the bags were filled or not.
	"""
	for config in configuration:
		if len(config) == 0:
			return False
	return True

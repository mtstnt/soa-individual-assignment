from nameko.rpc import rpc
import itertools as it

class CalculationService:
	name = "calculation_service"

	@rpc
	def permutation(self, value: list[any]) -> dict:
		if type(value) != list:
			return { "error": 1, "message": "Permutation parameter must be a list!" }
		results = []
		for i in range(1, len(value) + 1):
			comb = list(it.permutations(value, i))
			for j in comb:
				results.append(j)
		return { 
			"error": 0,
			"permutations": results
		}

	@rpc
	def combination(self, value: list[any]) -> dict:
		if type(value) != list:
			return { "error": 1, "message": "Combination parameter must be a list!" }

		results = []
		for i in range(1, len(value) + 1):
			comb = list(it.combinations(value, i))
			for j in comb:
				results.append(j)
		return { 
			"error": 0,
			"combinations": results
		}
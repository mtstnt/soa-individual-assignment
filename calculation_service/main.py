from nameko.rpc import rpc
import itertools as it

class CalculationService:
	name = "calculation_service"

	@rpc
	def permutation(value: list[any]) -> dict:
		if value is not list:
			return { "error": 1, "message": "Permutation parameter must be a list!" }
		return it.permutations(value)

	@rpc
	def combination(value: list[any]) -> dict:
		if value is not list:
			return { "error": 1, "message": "Combination parameter must be a list!" }
		return it.combinations(value)
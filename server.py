import pandas as pd
import solver_code

from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/solve', methods = ['POST'])
def handle_solve():
	# deserialize input board

	board_json = request.json
	print(board_json)
	board_numpy = pd.DataFrame(board_json).to_numpy()

	print(f'input board: {board_numpy}')
	# solve board
	solution = solver_code.BoardSolver(board_numpy).solve()
	
	print(f'output board: {solution}')
	# in case of no solution:
	if type(solution) == str:
		return jsonify(isError=True, statusCode=400, message=solution)
	
	# in case of solution:
	else:
		solution_json = pd.DataFrame(solution).to_json()
		print('solution:', solution_json)
		return jsonify(isError=False, statusCode=200, message='Success', data=solution_json)	


if __name__ == '__main__':
    app.run()



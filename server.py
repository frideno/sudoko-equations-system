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


"""

run with:

curl --header "Content-Type: application/json" --request POST --data '{"0":{"0":0,"1":0,"2":7,"3":0,"4":0,"5":0,"6":0,"7":1,"8":0},"1":{"0":4,"1":0,"2":2,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0},"2":{"0":0,"1":0,"2":3,"3":6,"4":2,"5":0,"6":0,"7":0,"8":4},"3":{"0":3,"1":0,"2":0,"3":9,"4":0,"5":0,"6":0,"7":0,"8":5},"4":{"0":0,"1":0,"2":0,"3":0,"4":4,"5":0,"6":6,"7":0,"8":1},"5":{"0":7,"1":0,"2":0,"3":0,"4":1,"5":0,"6":0,"7":0,"8":8},"6":{"0":0,"1":0,"2":0,"3":0,"4":3,"5":0,"6":0,"7":0,"8":0},"7":{"0":0,"1":8,"2":6,"3":4,"4":0,"5":0,"6":0,"7":0,"8":0},"8":{"0":0,"1":0,"2":0,"3":5,"4":6,"5":7,"6":9,"7":0,"8":0}}' http://127.0.0.1:5000/solve


"""

#!/usr/bin/python
import time

def read_cost_file():
	cost_file = open("imp2cost.txt", "r")
	input_lines = cost_file.read().split("\n")

	cost_dictionary = {}

	header = input_lines[0].split(",")
	for i in xrange(1, len(header)):
		cost_dictionary[header[i]] = {}
	
	for i in xrange(1, len(input_lines)):
		line = input_lines[i].split(",")
		for j in xrange(1, len(line)):
			cost_dictionary[header[j]][line[0]] = line[j]

	cost_file.close()
	return cost_dictionary


def diff(costs, x, y):
	return int(costs[x][y])


def insert(costs, row, index, sequence):
	return row[index-1] + diff(costs, sequence[index-1], "-")

def delete(costs, D, index1, index2, sequence):
	return D[index1-1][index2] + diff(costs, sequence[index1-1], "-")


def align(costs, D, index1, index2, sequence1, sequence2):
	return D[index1-1][index2-1] + diff(costs, sequence1[index1-1], sequence2[index2-1])


def calc_edit_distance(costs, sequence1, sequence2):
	D = [];
	m = len(sequence1) + 1
	n = len(sequence2) + 1
	result1 = []
	result2 = []
	directions = []

	for i in xrange(m):
		row = []
		row_directions = []
		for j in xrange(n):
			if i == 0 and j == 0:
				minimum = 0
				row_directions.append(' ')
			elif i == 0:
				minimum = insert(costs, row, j, sequence2)
				row_directions.append('d')
			elif j == 0:
				minimum = delete(costs, D, i, j, sequence1)
				row_directions.append('l')
			else:
				insert_cost = insert(costs, row, j, sequence2)
				delete_cost = delete(costs, D, i, j, sequence1)
				align_cost = align(costs, D, i, j, sequence1, sequence2)
				minimum = min(insert_cost, delete_cost, align_cost)

				if minimum == insert_cost:
					row_directions.append('d')
				elif minimum == delete_cost:
					row_directions.append('l')
				else:
					row_directions.append(' ')
					
			row.append(minimum)
			
		D.append(row)
		directions.append(row_directions)

	while i !=0 or j != 0:
		if directions[i][j] == 'l':
			i -= 1
			result1.insert(0, "-")
			result2.insert(0, sequence1[i])
		elif directions[i][j] == 'd':
			j -= 1
			result1.insert(0, sequence2[j])
			result2.insert(0, "-")
		else:
			i -= 1
			j -= 1
			result1.insert(0, sequence2[j])
			result2.insert(0, sequence1[i])
	
	return (result1, result2, D[m-1][n-1])


def main():
	costs = read_cost_file()

	input_file = open("imp2input5000.txt", "r")
	output_file = open("imp2output.txt", "w")

	times = []
	
	for line in input_file:
		line = line.split(",");
		sequence1 = line[0].strip("\n")
		sequence2 = line[1].strip("\n")

		start_time = time.time()

		(result1, result2, alignment_cost) = calc_edit_distance(costs, sequence2, sequence1)

		times.append(time.time() - start_time)
		
		output_file.write("".join(result1) + "," + "".join(result2) + ":" + str(alignment_cost) + "\n")

	print times

	input_file.close()
	output_file.close()


if __name__ == "__main__":
	main()


import matplotlib.pyplot as plt
from team import Team
from random import random
import numpy as np

num_teams = 30
num_years = 100

pos_util = [10, 8, 5, 3]

def main():
	# Initialize Teams
	teams = []
	for i in range(num_teams):
		teams.append(Team(i, 100, 0))
	history = []
	utilities = [0] * num_teams

	# Create list of team histories
	for i in range(num_teams):
		history.append(list())

	# Run Simulation Loop
	for year in range(num_years):
		# Run mechanism
		true_powers = [x.getPower() for x in teams]
		powers = [x.reportPower() for x in teams]
		new_power = mech(powers)

		for i in range(num_teams):
			new_power[i] = true_powers[i] + new_power[i] - powers[]

		for i in range(num_teams):
			teams[i].setPower(new_power[i])

		# Update histories
		for i in range(num_teams):
			history[i].append(true_powers[i])

		# Update utilities
		rankings = sorted(powers)
		rankings = [rankings.index(x) for x in powers]
		for i in range(num_teams):
			if rankings[i] == 0:
				utilities[i] += pos_util[0]
			elif rankings[i] == 1:
				utilities[i] += pos_util[1]
			elif rankings[i] < 4:
				utilities[i] += pos_util[2]
			elif rankings[i] < 16:
				utilities[i] += pos_util[3]

	for i in range(num_teams):
		print("Team %d:" % (i))
		print("\tAverage Power: %f" % (sum(history[i])/float(num_years)))
		print("\tAverage Utility: %f" % (utilities[i]/float(num_years)))
		print("----------------------------------------")

	print("Overall:")
	print("\tAverage Power Variance: %f" % (sum([np.var(np.asarray(x)) for x in history])/float(num_years)))
	print("----------------------------------------")


	# Visualize Result
	for i in range(num_teams):
		plt.plot(range(num_years), history[i])
	plt.show()



if __name__ == '__main__':
	main()
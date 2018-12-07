
import matplotlib.pyplot as plt
from team import Team
from random import random
import numpy as np
from nbamech import runmech

num_teams = 30
num_years = 100

pos_util = [10, 8, 5, 3]

def dummy_mech(x):
	ans = []
	for i in range(len(x)):
		ans.append((i, x[i][1] + 5 * (random() - 0.5)))
	return ans 

def main():
	# Initialize Teams
	teams = []
	for i in range(num_teams-5):
		teams.append(Team(i, 100, 0))
	for i in range(5):
		teams.append(Team(25+i, 100, True))
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
		print(powers)
		ind_power = []
		for i in range(num_teams):
			ind_power.append((i, powers[i]))
		new_power = sorted(runmech(ind_power), key=lambda x: x[0])
		new_power = [x[1] for x in new_power]

		for i in range(num_teams):
			new_power[i] = true_powers[i] + new_power[i] - powers[i]

		for i in range(num_teams):
			teams[i].setPower(new_power[i])

		# Update histories
		for i in range(num_teams):
			history[i].append(true_powers[i])

		# Update utilities
		rankings = sorted(powers, reverse=True)
		rankings = [rankings.index(x) for x in powers]
		print(rankings)
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
		plt.title("NBA Team Power Ratings over %d Years" % (num_years))
		plt.ylabel("Power Rating")
		plt.xlabel("Year")
	plt.show()



if __name__ == '__main__':
	main()

import matplotlib.pyplot as plt

num_teams = 30
num_years = 100

def main():
	teams = [Team()] * num_teams
	history = []
	for i in range(num_teams):
		history.append(list())
	for year in range(num_years):
		powers = [x.reportPower()[1] for x in teams]
		new_power = mech(powers)
		for i in range(num_teams):
			teams[i].setPower(new_power[i])
		for i in range(num_teams):
			history[i].append(power[i])
	for i in range(num_teams):
		plt.plot(range(num_years), history[i])



if __name__ == '__main__':
	main()
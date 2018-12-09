
import matplotlib.pyplot as plt
from team import Team
from random import random
import numpy as np
import pandas as pd
from nbamech import runmech

num_teams = 30
num_years = 100

pos_util = [10, 8, 5, 3]
init_powers = []
df = pd.DataFrame(index=range(1,num_teams+1), columns=range(num_years))

def dummy_mech(x):
  ans = []
  for i in range(len(x)):
    ans.append((i, x[i][1] + 5 * (random() - 0.5)))
  return ans

def main():
  # Initialize Teams
  teams = []
  for i in range(num_teams-5):
    teams.append(Team(i, 85 + 3 * i, 0))
  for i in range(5):
    teams.append(Team(25+i, 97 + i, 1))
  history = []
  history_report = []
  stdevs = []
  utilities = [0] * num_teams

  # Create list of team histories
  for i in range(num_teams):
    history.append(list())
    history_report.append(list())

  # Run Simulation Loop
  for year in range(num_years):
    # Run mechanism
    true_powers = [x.getPower() for x in teams]
    powers = [x.reportPower() * (1 + 0.1 * (random() - 0.5)) for x in teams]
    print(powers)
    ind_power = []
    for i in range(num_teams):
      ind_power.append((i, powers[i]))
    new_power = sorted(runmech(ind_power), key=lambda x: x[0])
    new_power = [x[1] for x in new_power]
    for i in range(num_teams):
      new_power[i] = true_powers[i] + new_power[i] - powers[i]
    # total = sum(new_power)
    # new_power = [x * (num_teams * 100.) / total for x in new_power]

    for i in range(num_teams):
      teams[i].setPower(new_power[i])

    # Update histories
    for i in range(num_teams):
      history[i].append(true_powers[i])
      history_report[i].append(powers[i])

    # Update standard deviations
    stdevs.append(np.std(np.asarray(true_powers)))

    # Update utilities
    rankings = sorted(powers, reverse=True)
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

    # Create dataframe
    df[year] = rankings

  for i in range(num_teams):
    print("Team %d:" % (i))
    print("\tAverage Power: %f" % (sum(history[i])/float(num_years)))
    print("\tAverage Utility: %f" % (utilities[i]/float(num_years)))
    print("----------------------------------------")

  print("Overall:")
  print("\tAverage Power Variance: %f" % (sum(stdevs)/float(num_years)))
  print("----------------------------------------")


  # Visualize Result
  f, ax = plt.subplots(1,2, figsize=(15,8))
  for i in range(num_teams):
    ax[0].plot(range(num_years), history[i])
    ax[0].set_title("NBA Team Power Ratings over %d Years" % (num_years))
    ax[0].set_ylabel("Power Rating")
    ax[0].set_xlabel("Year")

  for i in range(num_teams):
    ax[1].plot(range(num_years), history_report[i])
    ax[1].set_title("NBA Team Reported Power Ratings over %d Years" % (num_years))
    ax[1].set_ylabel("Power Rating")
    ax[1].set_xlabel("Year")
  plt.show()

  with open('team_rankings.csv', 'w') as out:
    out.write(df.to_csv())



if __name__ == '__main__':
  main()


import matplotlib.pyplot as plt
from team import Team
from random import random
import numpy as np
import pandas as pd
from nbamech_2019 import runmech

num_teams = 30
num_years = 100

pos_util = [10, 8, 5, 3, -2]
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
    teams.append(Team(i, 100, 0))
  for i in range(5):
    teams.append(Team(25+i, 100, 1))
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
    ave_powers = []
    for i in range(num_teams):
      try:
        ave_powers.append((powers[i] + history[i][-1] + history[i][-2]) / 3.0)
      except:
        ave_powers.append(powers[i])
    for i in range(num_teams):
      ind_power.append((i, ave_powers[i]))
    new_power = sorted(runmech(ind_power), key=lambda x: x[0])
    new_power = [x[1] for x in new_power]

    for i in range(num_teams):
      new_power[i] = true_powers[i] + new_power[i] - ave_powers[i]

    total = sum(new_power)
    new_power = [x * (num_teams * 100.) / total for x in new_power]

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
      elif rankings[i] > 24:
        utilities[i] += pos_util[4]

    # Create dataframe
    df[year] = rankings

  indices = [0, 5, 10, 15, 20, 26, 27, 28, 29]
  for i in range(num_teams):
    print("Team %d:" % (i))
    print("\tAverage Power: %f" % (sum(history[i])/float(num_years)))
    print("\tAverage Reported Power: %f" % (sum(history_report[i])/float(num_years)))
    print("\tAverage Utility: %f" % (utilities[i]/float(num_years)))
    print("----------------------------------------")

  print("Non-Tanking Teams:")
  print("\tAverage Power: %f" % (sum([sum(history[i])/float(num_years) for i in range(25)])/25.0))
  print("\tAverage Reported Power: %f" % (sum([sum(history_report[i])/float(num_years) for i in range(25)])/25.0))
  print("\tAverage Utility: %f" % (sum(utilities[:25])/float(num_years * 25)))
  print("----------------------------------------")

  print("Tanking Teams:")
  print("\tAverage Power: %f" % (sum([sum(history[i])/float(num_years) for i in range(25,30)])/5.0))
  print("\tAverage Reported Power: %f" % (sum([sum(history_report[i])/float(num_years) for i in range(25,30)])/5.0))
  print("\tAverage Utility: %f" % (sum(utilities[25:])/float(num_years * 5)))
  print("----------------------------------------")

  print("Overall:")
  print("\tAverage Power Variance: %f" % (sum(stdevs)/float(num_years)))
  print("----------------------------------------")


  # Visualize Result
  f, ax = plt.subplots(1,2, figsize=(15,8), sharey=True)
  for i in indices:
    ax[0].plot(range(num_years), history[i])
    ax[0].set_title("NBA Team Power Ratings over %d Years" % (num_years))
    ax[0].set_ylabel("Power Rating")
    ax[0].set_xlabel("Year")

  for i in indices:
    ax[1].plot(range(num_years), history_report[i])
    ax[1].set_title("NBA Team Reported Power Ratings over %d Years" % (num_years))
    ax[1].set_ylabel("Power Rating")
    ax[1].set_xlabel("Year")
  plt.show()

  with open('team_rankings_custom.csv', 'w') as out:
    out.write(df.to_csv())



if __name__ == '__main__':
  main()

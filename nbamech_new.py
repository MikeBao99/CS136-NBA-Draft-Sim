from random import randint
import numpy

# prob_dist = [250, 199, 156, 119,  88, 63, 43, 28, 17, 11, 8, 7, 6, 5]
# prob_dist = [140, 140, 140, 125, 105, 90, 75, 60, 45, 30, 20, 15, 10, 5] # 2019
prob_dist = [120, 120, 120, 120, 100, 100, 100, 100, 3, 3, 3, 3, 0, 0]

# on input 30 team's power levels as (team_id, power)
def runmech(powers):
  # initalizes scores 1 through 30 for the draftees
  # draftee_score = list(range(1, 31))
  # draftee_score.reverse()

  draftee_score = []
  for i in numpy.random.uniform(26, 30, size=(1, 5)).tolist()[0]:
    draftee_score.append(round(i, 2))
  for i in numpy.random.uniform(21, 24, size=(1, 5)).tolist()[0]:
    draftee_score.append(round(i, 2))
  for i in numpy.random.uniform(10, 17, size=(1, 20)).tolist()[0]:
    draftee_score.append(round(i, 2))

  draftee_score.sort(reverse=True)
  # print(draftee_score)

  # sorts from worst to best
  powers = sorted(powers, key=lambda x: x[1])
  print(powers)
  # picks worst 14 teams
  lottery_entrees = powers[:14]

  # makes sure that no teams have same score
  distinct = -1

  # checks whether they have the same score
  for x in range(len(lottery_entrees) - 1):
    if lottery_entrees[x][1] == lottery_entrees[x+1][1]:
      distinct = x
      break

  # if they have same score, averages their prob chances together
  if distinct != -1:
    prob_dist[x], prob_dist[x+1] = (((prob_dist[x] + prob_dist[x+1])/2),)*2

  # creates the method of lottery
  boundary = numpy.cumsum(prob_dist)

  # top n teams
  decided_lottery = []

  # number of teams that can win the lottery
  num_chosen = 8

  # runs the lottery and appends winner indices to list
  while len(decided_lottery) < num_chosen:
    lottery_draw = randint(1, 1001)
    for i in range(len(boundary)):
      if lottery_draw < boundary[i]:
        if i in decided_lottery:
          break
        else:
          decided_lottery.append(i)
          break

  # lottery winners' ids and powers
  first_n = []
  for index in decided_lottery:
    first_n.append(lottery_entrees[index])

  # the 14 - n worst teams that didn't win the lottery
  lottery_losers = []
  # basically just set division lol
  for i in range(len(lottery_entrees)):
    if lottery_entrees[i] not in first_n:
      lottery_losers.append(lottery_entrees[i])

  # combines everything together
  worst_fourteen = first_n + lottery_losers
  draft_order = worst_fourteen + powers[14:]

  # adds the new draftee scores to the teams
  for i in range(len(draft_order)):
    powers[i] = (draft_order[i][0], round(draft_order[i][1] + draftee_score[i],1))

  return powers

ids = list(range(1,31))
skill = list(range(85,115))
final_output = sorted(runmech(zip(ids,skill)), key=lambda x: x[1])
# print(final_output)
# print("~~~~~~~~~~~~~~~~~~")
# counter = 0
# for i in range(len(final_output)):
#   counter += abs(final_output[i][0] - (i+1))
# print(counter)





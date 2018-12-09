from random import randint
import numpy

prob_dist = [250, 199, 156, 119,  88, 63, 43, 28, 17, 11, 8, 7, 6, 5]
# prob_dist = [140, 140, 140, 125, 105, 90, 75, 60, 45, 30, 20, 15, 10, 5]

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

  # sorts from worst to best
  powers = sorted(powers, key=lambda x: x[1])
  # picks worst 14 teams
  lottery = powers[:14]

  distinct = -1

  for x in range(len(lottery) - 1):
    if lottery[x][1] == lottery[x+1][1]:
      distinct = x
      break

  if distinct != -1:
    prob_dist[x], prob_dist[x+1] = (((prob_dist[x] + prob_dist[x+1])/2),)*2

  boundary = numpy.cumsum(prob_dist)

  final_order = []

  while len(final_order) < 3:
    lottery_draw = randint(1, 1001)
    for i in range(len(boundary)):
      if lottery_draw < boundary[i]:
        if i in final_order:
          break
        else:
          final_order.append(i)
          break

  print(final_order)

  first_three = []
  for index in final_order:
    first_three.append(lottery[index])

  final_eleven = lottery
  real_final_eleven = []

  for i in range(len(final_eleven)):
    if final_eleven[i] not in first_three:
      real_final_eleven.append(final_eleven[i])

  worst_fourteen = first_three + real_final_eleven

  final_draft_order = worst_fourteen + powers[14:]
  print(final_draft_order)

  for i in range(len(final_draft_order)):
    powers[i] = (final_draft_order[i][0], round(final_draft_order[i][1] * 0.9 + draftee_score[i],1))

  return powers

ids = list(range(1,31))
skill = list(range(85,115))
print(sorted(runmech(zip(ids,skill)), key=lambda x: x[1]))





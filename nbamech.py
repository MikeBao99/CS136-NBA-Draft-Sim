from random import randint
import numpy

prob_dist = [250, 199, 156, 119,  88, 63, 43, 28, 17, 11, 8, 7, 6, 5]

# on input 30 team's power levels as (team_id, power)
def runmech(powers):
  # initalizes scores 1 through 30 for the draftees
  draftee_score = list(range(1, 31))
  draftee_score.reverse()

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
          continue
        else:
          final_order.append(i)
          break

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
    print(powers[i])
    print(powers[i][1])
    print(draftee_score[i])
    print(powers[i][1] + draftee_score[i])
    powers[i] = (final_draft_order[i][0], final_draft_order[i][1] + draftee_score[i])

  return powers


ids = list(range(1, 31))
powers = list(range(85, 115))

print(runmech(zip(ids, powers)))






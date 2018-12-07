class Team:
  def __init__(self, id, power, tank):
    self.id = id
    self.power = power
    self.tank = tank

  def getPower(self):
    return self.power

  def setPower(self, newPower):
    self.power = newPower

  def reportPower(self):
    if self.tank == True:
      return 0
    else:
      return self.power

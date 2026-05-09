import rolandoGarrafasMain as rg


def CreateGroup(groupName:str, initialPlayerNumber:int) -> rg.Group:
  players = []
  for i in range(initialPlayerNumber, initialPlayerNumber + 8):
    isSeed = i < initialPlayerNumber + 4
    name = 'Player' + str(i)
    players.append(rg.Player(name, isSeed))

  return rg.Group(groupName, players)


def CreateGroups(groupsLength:int) -> rg.Groups:
  groups = {}
  for i in range(groupsLength):
    groupName = 'Linha ' + str(i+1)
    initialPlayerNumber = 8*i + 1
    groups[groupName] = CreateGroup(groupName, initialPlayerNumber)

  return groups


def TestFromScratch() -> None:
  groupsLength = 3
  groups = CreateGroups(groupsLength)
  tournament = rg.Tournament('Test', groups)
  tournament.DrawGroups()
  print(tournament.GetTeamsStr())
  print(tournament.GetMatchesStr())


if __name__ == '__main__':
  TestFromScratch()
from playersImport import GetGroups
import rolandoGarrafasMain as rg


# PT-BR
kGroupPrefix = "Linha"


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
    groupName = kGroupPrefix + " " + str(i+1)
    initialPlayerNumber = 8*i + 1
    groups[groupName] = CreateGroup(groupName, initialPlayerNumber)

  return groups


def TestFromGroups(groups:rg.Groups) -> None:
  tournament = rg.Tournament('Test', groups)
  tournament.DrawGroups()
  print(tournament.GetTeamsStr())
  print(tournament.GetMatchesStr())


def TestFromScratch() -> None:
  groupsLength = 3
  groups = CreateGroups(groupsLength)
  TestFromGroups(groups)


def TestFromCsv(filePath:str) -> None:
  groups = GetGroups(filePath, kGroupPrefix)
  TestFromGroups(groups)


if __name__ == '__main__':
  TestFromScratch()
  TestFromCsv("TestData\\PlayersTest1.csv")
from enum import Enum
import pandas as pd
import rolandoGarrafasMain as rg


class Column(Enum):
  Group = 1
  Player = 2
  IsSeed = 3


def GetGroups(filePath:str, groupPrefix:str="Group") -> rg.Groups:
  df = pd.read_csv(filePath, encoding="utf-8")
  players: dict[int, list[rg.Player]] = {}
  for _, row in df.iterrows():
    group = row[Column.Group.name]
    playerName = row[Column.Player.name]
    isSeed = bool(row[Column.IsSeed.name])

    player = rg.Player(playerName, isSeed)
    players.setdefault(group, []).append(player)

  groups = {}
  for group, groupPlayers in players.items():
    groupName = groupPrefix + " " + str(group)
    groups[groupName] = rg.Group(groupName, groupPlayers)

  return groups

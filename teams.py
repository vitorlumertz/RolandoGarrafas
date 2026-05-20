
from enum import Enum


class TeamColor(Enum):
  Yellow = 1
  Blue = 2
  Green = 3
  Red = 4


# PT-BR
kTeamNames = {
  TeamColor.Yellow: 'Equipe Amarela',
  TeamColor.Blue:   'Equipe Azul',
  TeamColor.Green:  'Equipe Verde',
  TeamColor.Red:    'Equipe Vermelha',
}


kTeamsIcons = {
  TeamColor.Yellow: '🟡',
  TeamColor.Blue:   '🔵',
  TeamColor.Green:  '🟢',
  TeamColor.Red:    '🔴',
}


def GetTeamIcon(team:TeamColor) -> str:
  icon = kTeamsIcons.get(team)
  if icon is None:
    raise Exception("Could not get team icon.")
  return icon
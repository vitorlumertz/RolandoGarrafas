from dataclasses import dataclass
from enum import Enum
from typing import Literal
import random


type GroupName = str

type Team         = dict[GroupName, Double]
type Teams        = dict[TeamColor, Team]
type GroupDoubles = dict[TeamColor, Double]
type Groups       = dict[GroupName, Group]


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


@dataclass
class MatchPattern:
  team1: TeamColor
  team2: TeamColor


@dataclass
class RoundPattern:
  pattern1: MatchPattern
  pattern2: MatchPattern


@dataclass
class Player:
  name: str
  isSeed: bool

  def __str__(self):
    return self.name


@dataclass
class Double:
  player1: Player
  player2: Player
  team: TeamColor

  def __str__(self) -> str:
    return f'{self.player1}/{self.player2}'


@dataclass
class Match:
  double1: Double
  double2: Double
  groupName: str

  def __str__(self) -> str:
    d1 = self.double1
    d2 = self.double2
    return f'{self.groupName}: {kTeamsIcons[d1.team]} {d1} x {d2} {kTeamsIcons[d2.team]}'


@dataclass
class Round:
  roundNumber: Literal[1, 2, 3]
  matches: list[Match]

  def __str__(self) -> str:
    result = f'{self.roundNumber}ª Rodada:\n\n'
    for match in self.matches:
      result += f'{match}\n'
    return result


class Group:
  def __init__(self, name:str, players:list[Player]):
    self.name = name
    self.seeds, self.nonSeeds = self.__SplitSeeds(players)
    self.doubles: GroupDoubles = {}
    self.isDrawn = False
    self.roundPatterns: list[RoundPattern] = []


  def __SplitSeeds(self, players:list[Player]) -> tuple[list[Player], list[Player]]:

    def CheckSize(players:list[Player]) -> bool:
      return len(players) == 4

    seeds = []
    nonSeeds = []
    for p in players:
      if p.isSeed:
        seeds.append(p)
      else:
        nonSeeds.append(p)

    if CheckSize(seeds) and CheckSize(nonSeeds):
      return seeds, nonSeeds
    else:
      raise Exception("Division in seeds and non seeds is incorrect. It must be four seeds and four non seeds.")


  def Draw(self) -> None:
    if self.isDrawn:
      return

    random.shuffle(self.seeds)
    random.shuffle(self.nonSeeds)
    for i, team in enumerate(TeamColor):
      self.doubles[team] = Double(self.seeds[i], self.nonSeeds[i], team)

    self.isDrawn = True


  def __GetMatch(self, pattern:MatchPattern) -> Match:
    return Match(
      self.doubles[pattern.team1],
      self.doubles[pattern.team2],
      self.name,
    )


  def GetMatches(self, round:Literal[0, 1, 2]) -> tuple[Match, Match]:
    pattern = self.roundPatterns[round]
    match1 = self.__GetMatch(pattern.pattern1)
    match2 = self.__GetMatch(pattern.pattern2)
    return match1, match2


class Tournament:
  def __init__(self, name:str, groups:Groups):
    self.name = name
    self.groups = groups

    Yellow_x_Blue  = MatchPattern(TeamColor.Yellow, TeamColor.Blue)
    Yellow_x_Green = MatchPattern(TeamColor.Yellow, TeamColor.Green)
    Yellow_x_Red   = MatchPattern(TeamColor.Yellow, TeamColor.Red)
    Blue_x_Green   = MatchPattern(TeamColor.Blue,   TeamColor.Green)
    Blue_x_Red     = MatchPattern(TeamColor.Blue,   TeamColor.Red)
    Green_x_Red    = MatchPattern(TeamColor.Green,  TeamColor.Red)

    self.roundPatterns = [
      RoundPattern(Yellow_x_Blue, Green_x_Red),
      RoundPattern(Yellow_x_Green, Blue_x_Red),
      RoundPattern(Yellow_x_Red, Blue_x_Green),
    ]


  def DrawGroups(self) -> None:
    for group in self.groups.values():
      group.Draw()


  def GetTeams(self) -> Teams:
    teams = {t: {} for t in TeamColor}
    for group in self.groups.values():
      for t in TeamColor:
        teams[t][group.name] = group.doubles[t]
    return teams


  def GetTeamsStr(self) -> str:
    teams = self.GetTeams()
    teamsStr = ''
    for teamColor, team in teams.items():
      teamsStr += f'{kTeamNames[teamColor]}:\n'
      for groupName, double in team.items():
        teamsStr += f'\n{groupName}: {double}'
      teamsStr += '\n\n'

    return teamsStr


  def __UpdateGroupsRoundPatterns(self) -> None:

    def GetRoundPatterns(firstIndex:int) -> list[RoundPattern]:
      return self.roundPatterns[firstIndex:] + self.roundPatterns[:firstIndex]


    def UpdatePatternFirstIndex():
      nonlocal patternFirstIndex
      patternFirstIndex += 1
      if patternFirstIndex == len(self.roundPatterns):
        patternFirstIndex = 0


    patternFirstIndex = 0
    for group in self.groups.values():
      group.roundPatterns = GetRoundPatterns(patternFirstIndex)
      UpdatePatternFirstIndex()


  def GetRounds(self) -> list[Round]:
    self.__UpdateGroupsRoundPatterns()
    rounds = []
    for roundNumber in range(3):
      round = Round(roundNumber+1, [])
      for group in self.groups.values():
        matches = group.GetMatches(roundNumber)
        round.matches.extend(matches)
      rounds.append(round)

    return rounds


  def GetMatchesStr(self) -> str:
    matchesStr = f'Jogos do {self.name}:\n'
    for round in self.GetRounds():
      matchesStr += f'\n{round}'

    return matchesStr


  @staticmethod
  def __WriteInFile(filePath:str, content:str) -> None:
    with open(filePath, 'x', encoding='utf-8') as file:
      file.write(content)


  def WriteTeams(self, filePath:str) -> None:
    Tournament.__WriteInFile(filePath, self.GetTeamsStr())


  def WriteMatches(self, filePath:str) -> None:
    Tournament.__WriteInFile(filePath, self.GetMatchesStr())
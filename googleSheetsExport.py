from gspread.utils import rowcol_to_a1
from googleSheetsUtils import GoogleSheetsConnection

from teams import GetTeamIcon

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  import rolandoGarrafasMain as rg


# Formulas definitions (PT-BR)
kIf = "SE"


def rowcol_to_fixed_a1(row:int, column:int, isFixed:bool=False) -> str:
  a1 = rowcol_to_a1(row, column)
  if isFixed:
    return f"${a1[0]}${a1[1:]}"
  return a1


def GetRange(row1:int, column1:int, row2:int|None=None, column2:int|None=None, isFixed:bool=False) -> str:
  range = rowcol_to_fixed_a1(row1, column1, isFixed)
  if row2 is None:
    return range
  return range + ":" + rowcol_to_fixed_a1(row2, column2, isFixed)


def ExportMatches(tournament:"rg.Tournament", gsConnection:GoogleSheetsConnection) -> None:

  # Columns definitions
  kGroup = 1
  kTeam1 = 2
  kDouble1 = 3
  kDouble2 = 4
  kTeam2 = 5
  kGamesD1Set1 = 6
  kGamesD2Set1 = 7
  kGamesD1Set2= 8
  kGamesD2Set2 = 9
  kPointsD1Set3 = 10
  kPointsD2Set3 = 11
  kUpdateScore = 12
  kSetsD1 = 13
  kSetsD2 = 14
  kVictoryD1 = 15
  kVictoryD2 = 16
  kSetsScoreD1 = 17
  kSetsScoreD2 = 18
  kGamesScoreD1 = 19
  kGamesScoreD2 = 20

  values = [[
    "Linha",
    "Equipe D1",
    "Dupla 1 (D1)",
    "Dupla 2 (D2)",
    "Equipe D2",
    "Games Set 1 D1",
    "Games Set 1 D2",
    "Games Set 2 D1",
    "Games Set 2 D2",
    "Pontos Set 3 D1",
    "Pontos Set 3 D2",
    "Atualizar Classificação",
    "Sets D1",
    "Sets D2",
    "Vitória D1",
    "Vitória D2",
    "Saldo Sets D1",
    "Saldo Sets D2",
    "Saldo Games D1",
    "Saldo Games D2",
  ]]

  for group in tournament.groups.values():
    for match in group.GetAllMatches():
      d1 = match.double1
      d2 = match.double2

      rowValues = [group.name, GetTeamIcon(d1.team), str(d1), str(d2), GetTeamIcon(d2.team)]
      rowValues.extend([""] * 7) # match score and update score cell to be updated manually

      row = len(values) + 1
      gamesD1Set1Cell = GetRange(row, kGamesD1Set1)
      gamesD2Set1Cell = GetRange(row, kGamesD2Set1)
      gamesD1Set2Cell = GetRange(row, kGamesD1Set2)
      gamesD2Set2Cell = GetRange(row, kGamesD2Set2)
      pointsD1Set3Cell = GetRange(row, kPointsD1Set3)
      pointsD2Set3Cell = GetRange(row, kPointsD2Set3)

      set1D1Formula = f"{kIf}({gamesD1Set1Cell}>{gamesD2Set1Cell};1;0)"
      set1D2Formula = f"{kIf}({gamesD2Set1Cell}>{gamesD1Set1Cell};1;0)"
      set2D1Formula = f"{kIf}({gamesD1Set2Cell}>{gamesD2Set2Cell};1;0)"
      set2D2Formula = f"{kIf}({gamesD2Set2Cell}>{gamesD1Set2Cell};1;0)"
      set3D1Formula = f"{kIf}({pointsD1Set3Cell}>{pointsD2Set3Cell};1;0)"
      set3D2Formula = f"{kIf}({pointsD2Set3Cell}>{pointsD1Set3Cell};1;0)"

      setsD1Formula = f"={set1D1Formula}+{set2D1Formula}+{set3D1Formula}"
      setsD2Formula = f"={set1D2Formula}+{set2D2Formula}+{set3D2Formula}"

      setsD1Cell = GetRange(row, kSetsD1)
      setsD2Cell = GetRange(row, kSetsD2)

      victoryD1Formula = f"={kIf}({setsD1Cell}>{setsD2Cell};1;0)"
      victoryD2Formula = f"={kIf}({setsD2Cell}>{setsD1Cell};1;0)"

      setsScoreD1Formula = f"={setsD1Cell}-{setsD2Cell}"
      setsScoreD2Formula = f"={setsD2Cell}-{setsD1Cell}"

      gamesScoreD1Formula = f"={gamesD1Set1Cell}+{gamesD1Set2Cell}-{gamesD2Set1Cell}-{gamesD2Set2Cell}"
      gamesScoreD2Formula = f"={gamesD2Set1Cell}+{gamesD2Set2Cell}-{gamesD1Set1Cell}-{gamesD1Set2Cell}"

      rowValues.extend([
        setsD1Formula,
        setsD2Formula,
        victoryD1Formula,
        victoryD2Formula,
        setsScoreD1Formula,
        setsScoreD2Formula,
        gamesScoreD1Formula,
        gamesScoreD2Formula,
      ])

      values.append(rowValues)

  workSheetName = "Jogos" # PT-BR
  gsConnection.AddWorkSheet(workSheetName)

  cellsRange = GetRange(1, kGroup, len(values), kGamesScoreD2)
  gsConnection.WriteInWorkSheet(workSheetName, cellsRange, values, isFormula=True)

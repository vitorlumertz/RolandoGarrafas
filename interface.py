import rolandoGarrafasMain as rg
from playersImport import GetGroups

import tkinter as tk
from tkinter import filedialog, messagebox

import random
import sys
from dataclasses import dataclass
from pathlib import Path


# PT-BR
kGroupPrefix = "Linha"

kDefaultFontSize = 14
kDoubleFontSize = 9


@dataclass
class DrawStatus:
  maxIndex: int
  groupIndex: int = 0
  isSeed: bool = True
  finished: bool = False
  team: rg.TeamColor = rg.TeamColor.Yellow
  teamName: str = 'Equipe Amarela'
  color: str = 'yellow'
  hasToUpdatePlayers: bool = False

  def Update(self) -> None:
    if self.finished or self.hasToUpdatePlayers:
      return

    self.team = {
      rg.TeamColor.Yellow: rg.TeamColor.Blue,
      rg.TeamColor.Blue:   rg.TeamColor.Green,
      rg.TeamColor.Green:  rg.TeamColor.Red,
      rg.TeamColor.Red:    rg.TeamColor.Yellow,
    }.get(self.team)

    self.teamName = {
      rg.TeamColor.Yellow: 'Equipe Amarela',
      rg.TeamColor.Blue:   'Equipe Azul',
      rg.TeamColor.Green:  'Equipe Verde',
      rg.TeamColor.Red:    'Equipe Vermelha',
    }.get(self.team)

    self.color = {
      rg.TeamColor.Yellow: 'yellow',
      rg.TeamColor.Blue:   'blue',
      rg.TeamColor.Green:  'green',
      rg.TeamColor.Red:    'red',
    }.get(self.team)

    if self.team != rg.TeamColor.Yellow:
      return

    self.hasToUpdatePlayers = True
    self.isSeed = not self.isSeed

    if self.isSeed:
      if self.groupIndex < self.maxIndex:
        self.groupIndex += 1
      else:
        self.finished = True


class TouranentApp(tk.Tk):
  def __init__(self, tournamentName:str, title:str):
    super().__init__()

    inputFilePath = self.__SelectFile()
    self.tournament = self.__GetTournamentAndSave(inputFilePath, tournamentName)

    self.groupsNames = [name for name in self.tournament.groups.keys()]
    self.drawStatus = DrawStatus(len(self.tournament.groups) - 1)

    self.mainWindow = self.__GetMainWindow()

    self.__CreateTitle(title)
    self.drawButton = self.__CreateDrawButton()
    self.__UpdateDrawButtonText()
    self.__CreateNextPlayersButton()
    self.playersToDrawLabels = self.__CreatePlayersToDrawLabels()
    self.__CreateSeparatorLine()
    self.__CreateTeamsTitles()
    self.__CreateGroupsLabel()
    self.teamsLabels = self.__CreateTeamsLabels()


  def __SelectFile(self) -> str:
    self.withdraw()
    filePath = filedialog.askopenfilename(
      title = "Selecione o arquivo de inscritos",
      filetypes = [("CSV files", "*.csv")],
    )

    if not filePath:
      messagebox.showerror('Erro', 'Nenhum arquivo selecionado.')
      self.destroy()
      sys.exit()

    return filePath


  def __GetTournamentAndSave(self, inputFilePath:str, tournamentName:str) -> rg.Tournament:
    groups = GetGroups(inputFilePath, kGroupPrefix)
    tournament = rg.Tournament(tournamentName, groups)
    tournament.DrawGroups()

    outputFolder = Path(inputFilePath).parent
    baseOutputPath = f'{outputFolder}\\{tournamentName} - '
    tournament.WriteTeams(f'{baseOutputPath}Equipes.txt')
    tournament.WriteMatches(f'{baseOutputPath}Jogos.txt')

    return tournament


  def __GetMainWindow(self) -> tk.Tk:
    mainWindow = tk.Tk()
    mainWindow.title("Sorteio Rolando Garrafas")
    mainWindow.geometry('800x600-100-80')
    mainWindow['padx'] = 20
    mainWindow.columnconfigure(0, weight=20)
    for i in range(1, 5):
      mainWindow.columnconfigure(i, weight=100)
    return mainWindow


  def __CreateLabel(self, text:str, fontSize:int, backgroundColor:str|None=None) -> tk.Label:
    kwargs = {
      'text': text,
      'font': f'Verdana {fontSize} bold',
    }
    if backgroundColor is not None:
      kwargs['bg'] = backgroundColor

    return tk.Label(self.mainWindow, **kwargs)


  def __CreateTitle(self, title:str) -> None:
    label = self.__CreateLabel(title, 38)
    label.grid(row=0, column=0, columnspan=5, pady=0)


  def __UpdateDrawButtonText(self) -> None:
    text = f'Sortear tenista da {self.drawStatus.teamName}'
    self.drawButton.config(text=text)


  def __CreateDrawButton(self) -> tk.Button:
    button = tk.Button(self.mainWindow, command=self.__AddPlayerInTeam, text='', font='Verdana 12')
    button.grid(row=1, column=1, columnspan=2, sticky='ew', pady=10)
    return button


  def __CreateNextPlayersButton(self) -> None:
    button = tk.Button(self.mainWindow, command=self.__UpdatePlayersToDraw, text='Próximos Tenistas', font='Verdana 12')
    button.grid(row=1, column=3, columnspan=2, sticky='ew', pady=10)


  def __GetGroup(self) -> rg.Group:
    return self.tournament.groups[self.groupsNames[self.drawStatus.groupIndex]]


  def __GetPlayersToDraw(self) -> list[rg.Player]:
    group = self.__GetGroup()
    players = group.seeds if self.drawStatus.isSeed else group.nonSeeds
    random.shuffle(players)
    return players


  def __CreatePlayersToDrawLabels(self) -> dict[rg.TeamColor, tk.Label]:
    players = self.__GetPlayersToDraw()
    labels = {p.team: self.__CreateLabel(p.name, kDefaultFontSize) for p in players}
    for i, label in enumerate(labels.values()):
      label.grid(row=2, column=i+1, sticky='ew', pady=0)
      label.config(border=4, relief='raised')

    return labels


  def __CreateSeparatorLine(self) -> None:
    separator = tk.Frame(self.mainWindow, height=2, bd=1, relief='sunken')
    separator.grid(row=3, column=0, columnspan=5, sticky='ew', pady=10)


  def __CreateTeamsTitles(self) -> None:
    labels = (
      self.__CreateLabel('EQUIPE AMARELA:',  kDefaultFontSize, 'yellow'),
      self.__CreateLabel('EQUIPE AZUL:',     kDefaultFontSize, 'blue'),
      self.__CreateLabel('EQUIPE VERDE:',    kDefaultFontSize, 'green'),
      self.__CreateLabel('EQUIPE VERMELHA:', kDefaultFontSize, 'red'),
    )

    for i, label in enumerate(labels):
      label.grid(row=4, column=i+1, sticky='ew')
      label.config(border=4, relief='raised')


  def __CreateGroupsLabel(self) -> None:
    groupNames = [name + ':' for name in self.tournament.groups.keys()]
    text = '\n\n'.join(groupNames)

    label = self.__CreateLabel(text, kDoubleFontSize)
    label.grid(row=5, column=0, sticky='nw', padx=5)


  def __CreateTeamsLabels(self) -> dict[rg.TeamColor, tk.Label]:
    labels = {}
    for i in range(1, 5):
      label = self.__CreateLabel('', kDoubleFontSize)
      label.grid(row=5, column=i, sticky='n')
      labels[rg.TeamColor(i)] = label
    return labels


  def __AddPlayerInTeam(self) -> None:
    ds = self.drawStatus
    if ds.finished or ds.hasToUpdatePlayers:
      return

    player = self.__GetGroup().GetPlayerByTeam(ds.team, ds.isSeed)
    label = self.playersToDrawLabels[player.team]
    label.config(bg=ds.color)

    label = self.teamsLabels[ds.team]
    text = label['text']
    text += player.name
    text += '/' if ds.isSeed else '\n\n'
    label.config(text=text)

    ds.Update()
    self.__UpdateDrawButtonText()


  def __UpdatePlayersToDraw(self) -> None:
    ds = self.drawStatus
    if (ds.finished) or (ds.team != rg.TeamColor.Yellow) or (not ds.hasToUpdatePlayers):
      return

    players = self.__GetPlayersToDraw()
    labels = [l for l in self.playersToDrawLabels.values()]
    for i, player in enumerate(players):
      label = labels[i]
      self.playersToDrawLabels[player.team] = label
      label.config(text=player.name, bg=self.mainWindow.cget('bg'))

    ds.hasToUpdatePlayers = False

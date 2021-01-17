import random as r
import time as t
import logging

#logging.basicConfig(level=logging.DEBUG)

players = [dict(Team="Cambridge United",Name="Simon Brown"),
  dict(Team="Manchester United",Name="Michael Knighton"),
  dict(Team="Cambridge United",Name="William Brown"),
  dict(Team="Manchester United",Name="Charlie Frampton"),
  dict(Team="Chelsea",Name="Warren O'Neil"),
  dict(Team="Chelsea",Name="Liam O'Neil"),
  dict(Team="Cambridge United",Name="Andrew Brown"),
  dict(Team="Cambridge United",Name="Geoff Hurst"),
  dict(Team="Chelsea",Name="Nathan O'Neil"),
  dict(Team="Chelsea",Name="Mark O'Neil"),
  dict(Team="Manchester United",Name="Paul Knighton"),
  dict(Team="Manchester United",Name="Tom Noble")]

actions = [dict(type="pass",text="{p1} passes to {p2}"),
  dict(type="intercept",text="{p1} intercepts the pass"),
  dict(type="intercept",text="Intercepted by {p1}"),
  dict(type="cross",text="{p1} crosses the ball"),
  dict(type="cross",text="{p1} puts it in the box"),
  dict(type="pass",text="{p1} to {p2}"),
  dict(type="shot",text="{p1} shoots!"),
  dict(type="goal",text="{p1} scores!"),
  dict(type="save",text="What a save!"),
  dict(type="intercept",text="Possesion goes back to {possessingTeam}"),
  dict(type="pass",text="Long ball to {p2}"),
  dict(type="pass",text="Lovely ball by {p1}"),
  dict(type="pass",text="{p1} passes"),
  dict(type="intercept",text="What a tackle!"),
  dict(type="goal",text="It's unbelievable Jeff!  He's only gone and scored!"),
  dict(type="pass",text="Lovely little one-two"),
  dict(type="cross",text="Through ball by {p1}"),
  dict(type="finesse",text="What a turn"),
  dict(type="finesse",text="Lovely bit of skill"),
  dict(type="finesse",text="He's done 'im!"),
  dict(type="finesse",text="Nutmeg!"),
  dict(type="save",text="Great Save! Sent back up field"),
  dict(type="clear",text="Good clearance")]

closingStatements = ["They think it's all over... it is now",
  "There goes the final whistle",
  "And that's all she wrote"]

welcomeTxt = "Welcome to {t1} vs {t2}"
coinFlipTxt = "{team} won the coin flip and will be kicking off todays action"

def getAllActions():
  allActions = []
  for action in actions:
    allActions.append(action["type"])
  return allActions

def getAllTeams():
  allTeams = []
  for player in players:
    if player["Team"] not in allTeams:
      allTeams.append(player["Team"])
  return allTeams

def createTeam(teamName):
  team = []
  for player in players:
    if player["Team"] == teamName:
      team.append(player["Name"])
  return team

def getActionText(action):
  output = []
  for a in actions:
    if a["type"] == action:
      output.append(a["text"])
  return output

def switchPossession(poss):
  if poss == teamOneName:
    poss = teamTwoName
  else:
    poss = teamOneName
  return poss

def startPlay():
  global possession
  global teamOneScore
  global teamTwoScore
  global p1
  global p2
  global teamMembers
  global actionType
  global lastAction
  actionType = "center"
  inPlay = True
  while inPlay:
    if actionType == "shot":
      actionType = r.choice(["goal","save"])
    elif actionType == "cross":
      actionType = r.choice(["intercept","shot", "clear"])
    elif actionType == "center":
      actionType = "pass"
    elif actionType == "intercept":
      actionType = r.choice(["pass"])
    else:
      allActions = getAllActions()
      allActions.remove("save")
      actionType = r.choice(allActions)
    logging.debug("actionType: {}".format(actionType))
    actionText = r.choice(getActionText(actionType))
    if actionType == "intercept":
      possession = switchPossession(possession)
      teamMembers = createTeam(possession)
      p1 = r.choice(teamMembers)
      logging.debug("player1: {}".format(p1))
      teamMembers.remove(p1)
      p2 = r.choice(teamMembers)
      logging.debug("player2: {}".format(p2))
      logging.debug("possession: {}".format(possession))
    elif actionType == "pass" and lastAction != "center":
      p1 = p2
      teamMembers = createTeam(possession)
      teamMembers.remove(p1)
      p2 = r.choice(teamMembers)
    else:
      teamMembers = createTeam(possession)
      p1 = r.choice(teamMembers)
      logging.debug("player1: {}".format(p1))
      teamMembers.remove(p1)
      p2 = r.choice(teamMembers)
      logging.debug("player2: {}".format(p2))
    print(actionText.format(p1=p1,p2=p2,possessingTeam=possession))
    if actionType == "goal":
      inPlay = False
    t.sleep(0.5)
    lastAction = actionType
    #input("Press any key to continue...")
  if possession == teamOneName:
    teamOneScore += 1
  elif possession == teamTwoName:
    teamTwoScore += 1
  possession = switchPossession(possession)
  logging.debug("Center by: {}".format(possession))
  print("Back to {t1} for center".format(t1=possession))
  t.sleep(1)

'''
def startPlay():
  global possession
  logging.debug("Possession: {}".format(possession))
  t.sleep(0.3)
  possession = switchPossession(possession)
'''

allTeams = getAllTeams()
teamOneName = r.choice(allTeams)
allTeams.remove(teamOneName)
teamTwoName = r.choice(allTeams)
teamOne = createTeam(teamOneName)
teamTwo = createTeam(teamTwoName)
teamOneScore = 0
teamTwoScore = 0
actionType = "center"
lastAction = "center"

gameLength = int(t.time())+10
print(welcomeTxt.format(t1=teamOneName,t2=teamTwoName))
t.sleep(0.2)
print("This promises to be an exciting match up")
t.sleep(0.5)
possession = r.choice([teamOneName,teamTwoName])
print(coinFlipTxt.format(team=possession))
t.sleep(0.5)
teamMembers = createTeam(possession)
p1 = r.choice(teamMembers)
teamMembers.remove(p1)
p2 = r.choice(teamMembers)
print("{p1} passes to {p2}".format(p1=p1,p2=p2))
while(int(t.time())<=gameLength):
  startPlay()
  lastAction = "center"
  #possession = newPossession
signoff = r.choice(closingStatements)
print(signoff)
print("Final Score: |{t1}|{t1score}|{t2}|{t2score}|".format(t1=teamOneName,t2=teamTwoName,t1score=teamOneScore,t2score=teamTwoScore))

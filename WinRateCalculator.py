import random
import requests
import math

base_url = 'https://api.worldoftanks.com/wot/account/'
application_id = 'insert_application_id_here'

print '\nWoT Win Rate Goal Calculator\n'

# Get account id
username = raw_input('Player name: ')
request = requests.get(base_url + 'list/?application_id=' + application_id + '&search=' + username)
print 'Retrieving account...'
index = 0

# No results
if len(request.json()['data']) < 1:
   print 'No results found. Please restart and refine request.'
   exit()

# Multiple results (maxed at 100)
if len(request.json()['data']) > 1:
   print '\nPlease enter number of correct player, or restart and refine request:'
   for i in range(len(request.json()['data'])):
      print str(i + 1) + '. ' +  request.json()['data'][i]['nickname']
   choice = input('Player number: ')
   if choice < 1 or choice > len(request.json()['data']):
      exit()
   index = choice - 1
account_id = str(request.json()['data'][index]['account_id'])

# Get player stats
print '\nRetrieving stats...'
request = requests.get(base_url + 'info/?application_id=' + application_id + '&account_id=' + account_id)
stats =  request.json()['data'][account_id]['statistics']['all']

wins = stats['wins'] * 1.0
losses = stats['losses'] * 1.0
battles = stats['battles'] * 1.0
if battles > 0:
   win_rate = wins / battles * 100.0
else:
   win_rate = 0

print '\n-----|Current Stats|-----'
print 'Current wins: ' + str(wins)
print 'Current losses: ' + str(losses)
print 'Total battles: ' + str(battles)
print 'Current win rate: ' + str(win_rate)

# User goal input
print '\n-----|Goal Parameters|-----'
new_rate = input('New rate: ')
goal_rate = input('Goal rate: ')
new_wins = 0.0
new_losses = 0.0

if goal_rate <= win_rate:
   print 'Goal already achieved!'
   exit()

if goal_rate >= new_rate:
   print 'Goal not possible.'
   exit()

milestones = {}
next_milestone = math.floor(win_rate + 1)

# Calculations
while win_rate < goal_rate: 
   if win_rate >= next_milestone:
      milestones[str(win_rate)] = new_wins + new_losses
      next_milestone = math.floor(next_milestone + 1)
   battles = battles + 1 
   if random.randint(1, 100) < new_rate: 
     new_wins = new_wins + 1 
     wins = wins + 1 
     win_rate = wins / battles * 100.0 
   else: 
     new_losses = new_losses + 1 
     losses = losses + 1 
     win_rate = wins / battles * 100 

# Result printing
print '\n-----|Results|-----'
print "Num wins to goal: " + str(new_wins)
print "Num losses to goal: " + str(new_losses)
print "Num battles to goal: " + str(new_wins + new_losses)

print "Milestones:"
for p in sorted(milestones, key =  milestones.get):
   print str(math.floor(float(p))) + ': ' + str(milestones[p]) + ' battles'


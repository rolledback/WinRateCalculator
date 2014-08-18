import random
import requests
import math
import matplotlib.pyplot as plt

class WinRateCalculator(object):
   base_url = 'https://api.worldoftanks.com/wot/'
   application_id = 'insert application id here'
   account_id = ''

   wins = 0.0
   losses = 0.0
   battles = 0.0
   win_rate = 0.0

   goal_rate = 0.0
   milestones = {}
   data_points = list()

   new_rate = 0.0
   new_wins = 0.0
   new_losses = 0.0

   vehicle_ids = {}

   # load vehicle id mappings
   def loadVehicles(self):
      request = requests.get(self.base_url + 'encyclopedia/tanks/?application_id=' + self.application_id + '&fields=tank_id,short_name_i18n')
      data = request.json()['data']
      for tank_id in data:
         self.vehicle_ids[tank_id] = data[tank_id]['short_name_i18n']

   def getAccountId(self):
      # Get account id
      print 'Player name: '
      username = raw_input('> ')
      print '\nRetrieving account...'
      request = requests.get(self.base_url + 'account/list/?application_id=' + self.application_id + '&search=' + username)
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
         print ''
      self.account_id = str(request.json()['data'][index]['account_id'])

   # Choose between overall and vehicle request
   def chooseAndMakeRequest(self):
      print 'Calculate based off of profile win rate or specific tank (profile/tank):'
      input = ''
      while input != 'profile' and input != 'tank':
         input = raw_input('> ')
      if input == 'profile':
         self.overallRequest()
      else:
         self.vehicleRequest()

   # Get player stats
   def overallRequest(self):
      print '\nRetrieving player stats...'
      request = requests.get(self.base_url + 'account/info/?application_id=' + self.application_id + '&account_id=' + self.account_id)
      stats =  request.json()['data'][self.account_id]['statistics']['all']

      self.wins = stats['wins'] * 1.0
      self.losses = stats['losses'] * 1.0
      self.battles = stats['battles'] * 1.0
      if self.battles > 0:
         self.win_rate = self.wins / self.battles * 100.0
      else:
         self.win_rate = 0

   # Get vehicle stats
   def vehicleRequest(self):
      print '\nRetrieving vehicle stats...'
      request = requests.get(self.base_url + 'account/tanks/?application_id=' + self.application_id + '&account_id=' + self.account_id)
      player_tanks = []
      for tank in request.json()['data'][self.account_id]:
         tank_win_rate = (tank['statistics']['wins'] * 1.0 / tank['statistics']['battles']) * 100
         tank_battles = tank['statistics']['battles']
         player_tanks.append(self.vehicle_ids[str(tank['tank_id'])] + ', ' + str(tank_win_rate) + '%, ' + str(tank_battles) + ' battles')
      for i in range(len(player_tanks)):
         print str(i + 1) + '. ' + str(player_tanks[i])

      print 'Choose number of tank to use:'
      choice = ''
      choice = input('> ')
      if choice < 1 or choice > len(player_tanks):
         exit()
      index = choice - 1

      stats = request.json()['data'][self.account_id][index]['statistics']
      self.wins = stats['wins'] * 1.0
      self.battles = stats['battles'] * 1.0
      self.losses = self.battles - self.wins
      if self.battles > 0:
         self.win_rate = self.wins /self.battles * 100
      else:
         self.win_rate = 0

   def displayStats(self):
      print '\n-----|Current Stats|-----'
      print 'Current wins: ' + str(self.wins)
      print 'Current losses: ' + str(self.losses)
      print 'Total battles: ' + str(self.battles)
      print 'Current win rate: ' + str(self.win_rate)

   def getGoal(self):
      # User goal input
      print '\n-----|Goal Parameters|-----'
      self.new_rate = input('New rate: ')
      self.goal_rate = input('Goal rate: ')

      if self.goal_rate == self.win_rate:
         print 'Goal already achieved!'
         exit()

      if self.goal_rate >= self.new_rate and self.goal_rate > self.win_rate:
         print 'Goal not possible.'
         exit()

   def calcBattlesForGoal(self):
      self.data_points.append(self.win_rate)

      increasing = self.new_rate > self.goal_rate
      if increasing:
         next_milestone = math.floor(self.win_rate + 1)
      else:
         next_milestone = math.ceil(self.win_rate - 1)
      # Calculations
      while (increasing and self.win_rate < self.goal_rate) or (not increasing and self.win_rate > self.goal_rate):
         self.data_points.append(self.win_rate)
         
         if (increasing and self.win_rate >= next_milestone) or (not increasing and self.win_rate <= next_milestone):
            self.milestones[next_milestone] = self.new_wins + self.new_losses
            if increasing:
               next_milestone = math.floor(next_milestone + 1)
            else:
               next_milestone = math.ceil(next_milestone - 1)
         self.battles = self.battles + 1
         
         if random.randint(1, 100) < self.new_rate:
            self.new_wins = self.new_wins + 1
            self.wins = self.wins + 1
            self.win_rate = self.wins / self.battles * 100.0
         else:
            self.new_losses = self.new_losses + 1
            self.losses = self.losses + 1
            self.win_rate = self.wins / self.battles * 100
      self.data_points.append(self.win_rate)

   def printResults(self):
      # Result printing
      print '\n-----|Results|-----'
      print "Num wins to goal: " + str(self.new_wins)
      print "Num losses to goal: " + str(self.new_losses)
      print "Num battles to goal: " + str(self.new_wins + self.new_losses)

      print "Milestones:"
      for p in sorted(self.milestones, key =  self.milestones.get):
         print str(math.floor(float(p))) + ': ' + str(self.milestones[p])

      plt.plot(self.data_points)
      plt.ylabel('Win Rate')
      plt.xlabel('Battles')
      plt.show()
   def run(self):
      print '\vWoT Win Rate Calculator'
      self.loadVehicles()
      self.getAccountId()
      self.chooseAndMakeRequest()
      self.displayStats()
      self.getGoal()
      self.calcBattlesForGoal()
      self.printResults()

if __name__ == '__main__':
   test = WinRateCalculator()
   test.run()

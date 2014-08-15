import random
import requests
import math

class WinRateCalculator(object):
   base_url = 'https://api.worldoftanks.com/wot/account/'
   application_id = '1379369a8b79ed7fc6c715c410fd4eae'
   account_id = ''

   wins = 0.0
   losses = 0.0
   battles = 0.0

   goal_rate = 0.0
   milestones = {}

   new_rate = 0.0
   new_wins = 0.0
   new_losses = 0.0

   def getAccountId(self):
      # Get account id
      username = raw_input('Player name: ')
      print 'Retrieving account...'
      request = requests.get(self.base_url + 'list/?application_id=' + self.application_id + '&search=' + username)
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

   # Get player stats
   def overallRequest(self):
      print 'Retrieving stats...'
      request = requests.get(self.base_url + 'info/?application_id=' + self.application_id + '&account_id=' + self.account_id)
      stats =  request.json()['data'][self.account_id]['statistics']['all']

      self.wins = stats['wins'] * 1.0
      self.losses = stats['losses'] * 1.0
      self.battles = stats['battles'] * 1.0
      if self.battles > 0:
         self.win_rate = self.wins / self.battles * 100.0
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

      if self.goal_rate <= self.win_rate:
         print 'Goal already achieved!'
         exit()

      if self.goal_rate >= self.new_rate:
         print 'Goal not possible.'
         exit()

   def calcBattlesForGoal(self):
      next_milestone = math.floor(self.win_rate + 1)

      # Calculations
      while self.win_rate < self.goal_rate:
         if self.win_rate >= next_milestone:
            self.milestones[str(self.win_rate)] = self.new_wins + self.new_losses
            next_milestone = math.floor(next_milestone + 1)
         self.battles = self.battles + 1
         if random.randint(1, 100) < self.new_rate:
            self.new_wins = self.new_wins + 1
            self.wins = self.wins + 1
            self.win_rate = self.wins / self.battles * 100.0
         else:
            self.new_losses = self.new_losses + 1
            self.losses = self.losses + 1
            self.win_rate = self.wins / self.battles * 100

   def printResults(self):
      # Result printing
      print '\n-----|Results|-----'
      print "Num wins to goal: " + str(self.new_wins)
      print "Num losses to goal: " + str(self.new_losses)
      print "Num battles to goal: " + str(self.new_wins + self.new_losses)

      print "Milestones:"
      for p in sorted(self.milestones, key =  self.milestones.get):
         print str(math.floor(float(p))) + ': ' + str(self.milestones[p]) + ' self.battles'

   def run(self):
      print '\vWoT Win Rate Calculator'
      self.getAccountId()
      self.overallRequest()
      self.displayStats()
      self.getGoal()
      self.calcBattlesForGoal()
      self.printResults()

if __name__ == '__main__':
   test = WinRateCalculator()
   test.run()

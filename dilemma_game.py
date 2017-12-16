# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 17:40:39 2016

@author: Lluis Carreras Gonzalez
"""

from random import randint, random


class Player():
    ''' This class defines a player in the game
    '''
    
    def __init__(self, name, initial_points=0):
        self._name = name
        self._points = initial_points
        self._num_penalties = 0
        self._num_rewards = 0
        self._historic = [-1]
        self._election = -1
        self._points_to_add = 0
        
    def get_election(self):
        return self._election
        
    def set_election(self, election):
        self._election = election
        
    def get_points_to_add(self):
        return self._points_to_add
        
    def set_points_to_add(self, points_to_add):
        self._points_to_add = points_to_add
    
    def get_points(self):
        return self._points
        
    def add_points(self, points):
        self._points += points
        
    def get_name(self):
        return self._name
        
    def get_num_penalties(self):
        return self._num_penalties
    
    def increment_penalties(self):
        self._num_penalties += 1
        
    def get_num_rewards(self):
        return self._num_rewards
    
    def increment_rewards(self):
        self._num_rewards += 1
        
        
class Game():
    ''' This class defines a new game to be played
    '''
    
    def __init__(self, p0, p1, goal=50, offset=0, 
                 rounds_for_penalty=3, penalty=5, incr_penalty=1, 
                 rounds_for_reward=3, reward=5, incr_reward=1):
        self._players = [0, 0]
        self._players[0] = Player(p0, 0)
        self._players[1] = Player(p1, 0)
        self._goal = goal
        self._offset = offset
        self._rounds_for_penalty = rounds_for_penalty
        self._penalty = penalty
        self._incr_penalty = incr_penalty
        self._rounds_for_reward = rounds_for_reward
        self._reward = reward
        self._incr_reward = incr_reward
        self._payoff_both_cooperate = 3
        self._payoff_both_defect = 1
        self._payoff_who_defects = 5
        self._payoff_who_cooperates = 0
        self._current_round = 1
        print(" ROUND | PLAYERS BEHAVIOUR\t\t| A B |   {0:s}    {1:s} |   {0:s}     {1:s} | CURRENT WINNER".format(
                self._players[0].get_name(), self._players[1].get_name(),
                self._players[0].get_name(), self._players[1].get_name()))
        print("-" * 95) 
        print("     0 | The game begins...")
        self.play()
        
    def actualize(self, message, summary, show_round=True):
        ''' Shows a message about wich player is wining
        '''
        
        # Pluralize message
        plural = "s"
        
        # Add points to both players
        p0_add = self._players[0].get_points_to_add()
        p1_add = self._players[1].get_points_to_add()
        self._players[0].add_points(p0_add)
        self._players[1].add_points(p1_add)
        
        # Get points from both players
        p0_total = int(self._players[0].get_points())
        p1_total = int(self._players[1].get_points())
        
        # Build message about who's winning
        if self._players[0].get_points() == self._players[1].get_points():
            whos_winning_str = "  Draw on {0:d} points".format(self._players[0].get_points())
        elif self._players[0].get_points() > self._players[1].get_points():
            diff = self._players[0].get_points() - self._players[1].get_points()
            if diff == 1:
                plural = ""
            whos_winning_str = "Player {0:s} wins on {1:d} point{2:s}".format(
                    self._players[0].get_name(), diff, plural)
        else:
            diff = self._players[1].get_points() - self._players[0].get_points()
            if diff == 1:
                plural = ""
            whos_winning_str = "    Player {0:s} wins on {1:d} point{2:s}".format(
                        self._players[1].get_name(), diff, plural)
            
        # Print message
        if show_round:
            current_round = self._current_round
            print("{0:6d} | {1:<30s} | {2:s} | {3:>3d}  {4:>3d} | {5:3d}   {6:3d} | {7:s}".format(
                    current_round, message, summary, p0_add, p1_add, 
                    p0_total, p1_total, whos_winning_str))
        else:
            current_round = ""
            print("{0:6s} | {1:<30s} | {2:s} | {3:>3d}  {4:>3d} | {5:3d}   {6:3d} | {7:s}".format(
                        current_round, message, summary, p0_add, p1_add, 
                        p0_total, p1_total, whos_winning_str))
      
    def penalize(self, player): 
        ''' Penalizes a player when doesn't collaborate several times in a row
        '''
        
        if player == self._players[0]:
            other = self._players[1]
        else:
            other = self._players[0]
            
        player.increment_penalties()
        
        message = "Player {0:s} gets the penalty #{1:d}.".format(player.get_name(), 
                    player.get_num_penalties())              
        plus_penalty = ((player.get_num_penalties() - 1) // 3) * self._incr_penalty
        
        if (self._penalty + plus_penalty) > player.get_points():
            player._points_to_add = - player.get_points()
        else:
            player._points_to_add = - self._penalty - plus_penalty 
            
        other._points_to_add = 0
        summary = "   "  
        self.actualize(message, summary, show_round=False)                         
        player._historic[-1] = -1
        
    def reward(self, player):
        ''' Rewards a player for collaborating several times in a row
        '''
        
        if player == self._players[0]:
            other = self._players[1]
        else:
            other = self._players[0]
            
        player.increment_rewards()
        
        message = "Player {0:s} gets the reward #{1:d}.".format(player.get_name(),
                    player.get_num_rewards())              
        plus_reward = ((player.get_num_rewards() - 1) // 3) * self._incr_reward
        
        player._points_to_add = self._reward + plus_reward
        other._points_to_add = 0
        summary = "   "  
        self.actualize(message, summary, show_round=False)                   
        player._historic[-1] = -1
        
    def calculate_points(self):
        ''' Calculates the points of both playes after every round
        '''
        
        # Set the points to add to both players
        if self._players[0].get_election() == 0 and self._players[1].get_election() == 0:
            # Both players defect
            self._players[0]._points_to_add = self._payoff_both_cooperate
            self._players[1]._points_to_add = self._payoff_both_cooperate
            message = "Both players cooperate."
            summary = "- -"
        elif self._players[0].get_election() == 0 and self._players[1].get_election() == 1:
            # Player1 defects and player2 cooperates
            self._players[0]._points_to_add = self._payoff_who_cooperates
            self._players[1]._points_to_add = self._payoff_who_defects
            message = "Only Player {0:s} cooperates.".format(self._players[1].get_name())
            summary = "- X"
        elif self._players[0].get_election() == 1 and self._players[1].get_election() == 0:
            # Player1 cooperates and player2 defects
            self._players[0]._points_to_add = self._payoff_who_defects
            self._players[1]._points_to_add = self._payoff_who_cooperates
            message = "Only Player {0:s} cooperates.".format(self._players[0].get_name())
            summary = "X -"
        else:
            # Both players cooperate
            self._players[0]._points_to_add = self._payoff_both_defect
            self._players[1]._points_to_add = self._payoff_both_defect  
            message = "Both players defect.  "
            summary = "X X"
        
        return message, summary
       
    def random_strategy(self, player):
        '''This strategy makes random decissions, with 50% cooperations and 50% defections.
        '''
        
        return randint(0, 1)
        
    
    def tit_for_tat_strategy(self, player):
        '''This strategy begins collaborating in the first round and continues repeating
        the option of the opponent in the former round.
        '''
    
        if player == self._players[0]:
            other = self._players[1]
        else:
            other = self._players[0]
            
        if self._current_round <= 1:
            return 0
        else:
            if other._historic[self._current_round - 1] != -1:
                return other._historic[self._current_round - 1]
            else:
               return other._historic[self._current_round - 2] 
        
    def maximum_outcome_strategy(self, player, rand=0.0):
        '''This strategy calculates the four possible outcomes in the next round and
        chooses the one with the maximum difference of points.
        '''
 
        # Calculate the points of all the feasible results in the round
        results_p0 = [self._payoff_both_cooperate, self._payoff_who_cooperates,
                      self._payoff_who_defects, self._payoff_both_defect]
        results_p1 = [self._payoff_both_cooperate, self._payoff_who_cooperates,
                      self._payoff_who_defects, self._payoff_both_defect]
        
        # Calculate the feasible penalizations and rewards
        pens_and_rews = self.dummy_penalties_and_rewards()
        p_r_p0 = [0, 0, 0, 0]
        p_r_p1 = [0, 0, 0, 0]
        if pens_and_rews[0] == 1:
            p_r_p0[0] = self._reward
            p_r_p0[1] = self._reward
        if pens_and_rews[1] == 1:
            p_r_p1[0] = self._reward
            p_r_p1[2] = self._reward
        if pens_and_rews[2] == 1:
            p_r_p0[2] = - self._penalty
            p_r_p0[3] = - self._penalty
        if pens_and_rews[3] == 1:
            p_r_p1[1] = - self._penalty
            p_r_p1[3] = - self._penalty
        
        # Calculate the totals
        totals_p0 = [a + b for a, b in zip(results_p0, p_r_p0)]
        totals_p1 = [a + b for a, b in zip(results_p1, p_r_p1)]
        
        # Calculate de differences between both players
        results_diff = [a - b for a, b in zip(totals_p0, totals_p1)]

        # Get the best option
        if random() <= rand:
            return randint(0, 1)
        else:
            if player == self._players[0]:
                idx_option = results_diff.index(max(results_diff))
                if idx_option in (0, 1):
                    return 0
                else:
                    return 1
            else:
                idx_option = results_diff.index(min(results_diff))
                if idx_option in (0, 2):
                    return 0
                else:
                    return 1
    
    def penalties_and_rewards(self, strategy=False):   
        ''' Calculate the feasible penalizations and rewards
        '''
        
        results = []
        functions = [self.reward, self.penalize]
        for f in (0, 1):
            for p in (0, 1):
                if (self._players[p]._historic[-1] == f and
                        self._players[p]._historic[-1] == self._players[p]._historic[-2] and
                        self._players[p]._historic[-1] == self._players[p]._historic[-3]):                    
                    results.append(1)
                    if strategy == False:
                        functions[f](self._players[p])
                else:
                    results.append(0)
        if strategy:
#             print(results)
             return results
             
    def dummy_penalties_and_rewards(self):  
        ''' Calculate the feasible penalizations and rewards
        '''
        
        results = [0, 0, 0, 0]

        if len(self._players[0]._historic) > 1:
            if (self._players[0]._historic[-1] == self._players[0]._historic[-2]):
                if(self._players[0]._historic[-1] == 0):
                     results[0] = 1
                elif(self._players[0]._historic[-1] == 1):
                    results[2] = 1
            if (self._players[1]._historic[-1] == self._players[1]._historic[-2]):
                if(self._players[1]._historic[-1] == 0):
                     results[1] = 1
                elif(self._players[1]._historic[-1] == 1):
                    results[3] = 1   
#        print(self._players[0]._historic)
#        print(self._players[1]._historic)
#        print(results)
        return results

    def play(self):
        
#        # Set variables to initial values
#        current_round = 1
        
        # Iterate over the game
        while (self._players[0].get_points() < self._goal and
               self._players[1].get_points() < self._goal or
               self._players[0].get_points() == self._players[1].get_points() or
               abs(self._players[0].get_points() - self._players[1].get_points()) < self._offset):
                   
            # Get random elections for both players 
            self._players[0].set_election(self.random_strategy(self._players[0]))
#            self._players[1].set_election(self.random_strategy(self._players[1]))

            # Set maximum outcome strategy
#            self._players[0].set_election(self.maximum_outcome_strategy(self._players[0], 0.3))
#            self._players[1].set_election(self.maximum_outcome_strategy(self._players[1], 0.3))


            # Set tit for tat strategy
#            self._players[0].set_election(self.tit_for_tat_strategy(self._players[0]))
            self._players[1].set_election(self.tit_for_tat_strategy(self._players[1]))
                                     
            # Insert the last elections in historic lists
            for player in self._players:
                player._historic.append(player.get_election())
                
            # Actualize the results
            message, summary = self.calculate_points()
            self.actualize(message, summary)
            
            # Penalizations and rewards
            self.penalties_and_rewards(False)
                              
            # Actualize variables
            self._current_round += 1
        
        # Show the winner              
        if self._players[0].get_points() < self._players[1].get_points():
            who_wins_str = "PLAYER {0:s} WINS!!!".format(self._players[1].get_name())
        elif self._players[0].get_points() > self._players[1].get_points():
            who_wins_str = "PLAYER {0:s} WINS!!!".format(self._players[0].get_name())
        else:
            who_wins_str = "THERE'S A DRAW!!!"
        print("\n", who_wins_str)   
 

# Play a game
if __name__ == '__main__':           
    p0 = "A"
    p1 = "B"
    goal = 50
    offset = 10
    rounds_for_penalty = 3
    rounds_for_reward = 3
    penalty = 5
    reward = 3
    incr_penalty = 1
    incr_reward = 1
        
    game = Game(p0, p1, goal, offset, 
                rounds_for_penalty, penalty, incr_penalty,
                rounds_for_reward, reward, incr_reward)    
    

    
    
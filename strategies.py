from abc import ABC, abstractmethod
from typing import List
import utils
import numpy as np

strategies = ['unit', 'fixed', 'fixed_pct', 'kelly_criterion', 'martingale',
              'percent_martingale', 'anti_martingale','percent_anti_martingale',
              'kelly_martingale', 'kelly_anti_martingale', 'winners_bet',
              'percent_winners_bet', 'kelly_winners', 'fibonacci', 'anti_fibonacci',
              'percent_fibonacci', 'percent_anti_fibonacci', 'kelly_fibonacci',
              'kelly_anti_fibonacci', 'dalembert', 'anti_dalembert', 'percent_dalembert',
              'anti_percent_dalembert']

class Strategies(ABC):
    def __init__(self, results: List[List], prob_info: List[List], initial_amt: float):
        self.bet_results = results # outcomes over multiple runs
        self.prob_info = prob_info # [[prob, payout]] -- like the distribution of a bet/option
        self.implied_probability = None
        self.unit_payout = None
        self.initial_amt = initial_amt # principal
        
        self.return_value = None
        self.sizing = None # fixed, variable
        self.kind = None # unit, percentage
    
    def simulate_strategy(self):
        self.__current_bankroll = self.initial_amt
        self.__bet_size = None
        self.current_index = 0
        self.pct_bet_size = None

        self.bankroll_values = []
        self.bet_sizes = []

        while self.__current_bankroll > 0 and self.__bet_size < self.__current_bankroll:
            return

class BettingStrategies(Strategies):
    def __init__(self, results, prob_info):
        super().__init__(results, prob_info)
        self.implied_probability = [[utils.convert_american_odds_implied_probability(odd) for odd in prob_info]]
        self.unit_payout = [[utils.convert_american_odds_return(odd) for odd in prob_info]]
    
class UnitBet(BettingStrategies):
    def __init__(self, results, prob_info):
        super().__init__(results, prob_info)
        self.kind = 'unit'
        self.sizing = 'fixed'
        
class FixedBet(UnitBet):
    def __init__(self, results, prob_info):
        super().__init__(results, prob_info)
    pass

class FixedPercentage(FixedBet):
    def __init__(self, results, prob_info, percent=0.15):
        super().__init__(results, prob_info)
        self.kind = 'percent'
        self.pct_bet_size = percent
    pass

class KellyCriterion(BettingStrategies):
    def __init__(self, results, prob_info):
        super().__init__(results, prob_info)
        self.kind = 'percent'
        self.sizing = 'variable'
        self.pct_bet_size = percent
        pass
     
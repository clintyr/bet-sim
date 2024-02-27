from abc import ABC, abstractmethod
from typing import List
import utils
import numpy as np
from decimal import Decimal

strategies = ['unit/fixed', 'fixed_pct', 'kelly_criterion', 'martingale',
              'percent_martingale', 'anti_martingale','percent_anti_martingale',
              'kelly_martingale', 'kelly_anti_martingale', 'winners_bet',
              'percent_winners_bet', 'kelly_winners', 'fibonacci', 'anti_fibonacci',
              'percent_fibonacci', 'percent_anti_fibonacci', 'kelly_fibonacci',
              'kelly_anti_fibonacci', 'dalembert', 'anti_dalembert', 'percent_dalembert',
              'anti_percent_dalembert']

class Strategies(ABC):
    def __init__(self, results: List[List[str]], prob_info):
        self.bet_results = results # outcomes over multiple runs
        self.prob_info = prob_info # odds 
        self.return_value = None

class BettingStrategies(Strategies):
    def __init__(self, results, prob_info, initial_amt=100):
        super().__init__(results, prob_info)
        self.implied_probability = [[utils.convert_american_odds_implied_probability(odd) for odd in odds] for odds in prob_info]
        self.unit_payout = [[utils.convert_american_odds_return(odd) for odd in odds] for odds in prob_info]
        self.num_runs = len(self.bet_results)
        self.initial_amt = initial_amt

        self.current_index = 0

    def simulate_bankroll(self, num_bets, outcome, unit_payout):

        self.current_bankroll = self.initial_amt
        self.current_index = 0

        self.bankrolls = []
        self.betsize_history = []

        while self.current_bankroll > 0 and self.bet_size < self.current_bankroll and self.current_index < num_bets:
            bet_size = round(self.bet_size, 2)

            bet_result = outcome[self.current_index]
            bet_payout = unit_payout[self.current_index]
            
            outcome_payout = utils.calculate_bet_outcome(bet_size, bet_result, bet_payout)
            outcome_payout = round(outcome_payout, 2)

            self.current_bankroll += outcome_payout
            self.current_bankroll = round(self.current_bankroll, 2)

            self.bankrolls.append(self.current_bankroll)
            self.betsize_history.append(bet_size)

            self.current_index += 1

            self.last_outcome = bet_result
            self.last_bet_size = bet_size
            self.last_payout = outcome_payout

            if self.sizing == 'variable':
                self.change_bet_size()

    def simulate_strategy(self):
        self.bankroll_values = []
        self.bet_sizes = []

        for i in range(self.num_runs):
            self.bet_size = self.initial_bet_size
            unit_payout = self.unit_payout[i]
            outcome = self.bet_results[i]

            num_bets = len(self.bet_results[self.current_index])

            self.simulate_bankroll(num_bets, outcome, unit_payout)
            
            self.bankroll_values.append(self.bankrolls)
            self.bet_sizes.append(self.betsize_history)
        
    def verify_min_bet(self):
        if self.bet_size < 1:
            self.bet_size = 1

    def change_bet_size(self):
        pass

class UnitBet(BettingStrategies):
    # want to support changing unit size per bet in diff class
    def __init__(self, results, prob_info, initial_amt=100, unit_size=1):
        super().__init__(results, prob_info, initial_amt)
        self.unit_size = unit_size

        self.kind = 'unit'
        self.sizing = 'fixed'
        self.initial_bet_size = 1 * self.unit_size
        self.bet_size = self.initial_bet_size

class FixedPercentage(BettingStrategies):
    def __init__(self, results, prob_info, initial_amt=100, pct=0.01, unit_size=1):
        super().__init__(results, prob_info, initial_amt)
        self.unit_size = unit_size

        self.kind = 'percent'
        self.sizing = 'variable'
        self.pct_bet_size = pct

        self.initial_bet_size = self.pct_bet_size * self.initial_amt
        self.bet_size = self.initial_bet_size

    def change_bet_size(self):
        self.bet_size = self.current_bankroll * self.pct_bet_size

class Martingale(BettingStrategies):
    def __init__(self, results, prob_info, initial_amt=100, unit_size=1):
        super().__init__(results, prob_info, initial_amt)
        self.unit_size = unit_size

        self.kind = 'unit'
        self.sizing = 'variable'
        self.initial_bet_size = 1 * self.unit_size
        self.bet_size = self.initial_bet_size

    def change_bet_size(self):

        if self.last_outcome == 'Push':
            pass
        elif self.last_outcome == 'W':
            self.bet_size = self.initial_bet_size
        elif self.last_outcome == 'L':
            self.bet_size *= 2

class AntiMartingale(BettingStrategies):
    def __init__(self, results, prob_info, initial_amt=100, unit_size=1):
        super().__init__(results, prob_info, initial_amt)
        self.unit_size = unit_size

        self.kind = 'unit'
        self.sizing = 'variable'
        self.initial_bet_size = 1 * self.unit_size
        self.bet_size = self.initial_bet_size

    def change_bet_size(self):

        if self.last_outcome == 'Push':
            pass
        elif self.last_outcome == 'L':
            self.bet_size = self.initial_bet_size
        elif self.last_outcome == 'W':
            self.bet_size *= 2

class KellyCriterion(BettingStrategies):
    def __init__(self, results, prob_info, pct=None, unit_size=1):
        super().__init__(results, prob_info)
        self.unit_size = unit_size

        self.kind = 'percent'
        self.sizing = 'variable'
        self.pct_bet_size = pct

        self.initial_bet_size = self.initial_amt
        self.initial_kelly_fraction = utils.calculate_kelly_criterion()
        self.bet_size = 0
    
    def change_bet_size(self):
        pass

class WinnersBet(BettingStrategies):
    def __init__(self, results, prob_info, initial_amt=100, unit_size=1):
        super().__init__(results, prob_info, initial_amt)
        self.unit_size = unit_size

        self.kind = 'unit'
        self.sizing = 'variable'

        self.initial_bet_size = 1 * self.unit_size
        self.bet_size = self.initial_bet_size

    def change_bet_size(self):

        if self.last_outcome == 'Push':
            pass
        elif self.last_outcome == 'L':
            self.bet_size = self.initial_bet_size
        elif self.last_outcome == 'W':
            self.bet_size = self.last_payout

class Fibonacci(BettingStrategies):
    def __init__(self, results, prob_info, initial_amt=100, unit_size=1):
        super().__init__(results, prob_info, initial_amt)
        self.unit_size = unit_size

        self.kind = 'unit'
        self.sizing = 'variable'

        self.initial_bet_size = 1 * self.unit_size
        self.bet_size = self.initial_bet_size

    def change_bet_size(self):

        if self.last_outcome == 'Push':
            pass
        elif self.last_outcome == 'L':
            self.bet_size = self.initial_bet_size
        elif self.last_outcome == 'W':
            self.bet_size = self.last_payout

class AntiFibonacci(BettingStrategies):
    pass

class Dalembert(BettingStrategies):
    pass

class AntiDalembert(BettingStrategies):
    pass
import unittest
from strategies import UnitBet, FixedPercentage, Martingale, AntiMartingale, KellyCriterion
from strategies import WinnersBet, Fibonacci, AntiFibonacci, Dalembert, AntiDalembert

bet_results = [["W", "W", "W", "Push", "Push", "W"],
               ["L", "L", "L", "Push", "L", "L"],
               ["L", "W", "L", "W", "L", "W"],
               ["W", "W", "W", "W", "W", "W"],
               ["L", "L", "L", "L", "L", "L"],
               ["Push", "Push", "Push", "Push", "Push", "Push"],
               ["W", "W", "W", "L", "L", "L"]]

test_input = {'win_rate': 0.5, 'unit_payout': 1, 'bet_size': 1, 'initial_amt': 100}

prob_info = [[100]*len(bet_results[0])]*len(bet_results) # corresponds to test input

class UnitBetTest(unittest.TestCase):
    def test_bankroll_values(self):

        expected_bet_sizes = [[1]*len(bet_results[0])]*len(bet_results)
        expected_running_bankroll = [[101, 102, 103, 103, 103, 104],
                                     [99, 98, 97, 97, 96, 95],
                                     [99, 100, 99, 100, 99, 100],
                                     [101, 102, 103, 104, 105, 106],
                                     [99, 98, 97, 96, 95, 94],
                                     [100, 100, 100, 100, 100, 100],
                                     [101, 102, 103, 102, 101, 100]]

        u_bet = UnitBet(bet_results, prob_info)
        u_bet.simulate_strategy()
        # print(u_bet.bankroll_values) 
        self.assertEqual(expected_running_bankroll, u_bet.bankroll_values)
        self.assertEqual(expected_bet_sizes, u_bet.bet_sizes)

class FixedPercentageTest(unittest.TestCase):
    def test_bankroll_values(self):
        expected_bet_sizes = [[1, 1.01, 1.02, 1.03, 1.03, 1.03],
                              [1, 0.99, 0.98, 0.97, 0.97, 0.96],
                              [1, 0.99, 1, 0.99, 1, 0.99],
                              [1, 1.01, 1.02, 1.03, 1.04, 1.05],
                              [1, 0.99, 0.98, 0.97, 0.96, 0.95],
                              [1, 1, 1, 1, 1, 1],
                              [1, 1.01, 1.02, 1.03, 1.02, 1.01]]
        
        expected_running_bankroll = [[101, 102.01, 103.03, 103.03, 103.03, 104.06],
                                     [99, 98.01, 97.03, 97.03, 96.06, 95.1],
                                     [99, 99.99, 98.99, 99.98, 98.98, 99.97],
                                     [101, 102.01, 103.03, 104.06, 105.1, 106.15],
                                     [99, 98.01, 97.03, 96.06, 95.1, 94.15],
                                     [100, 100, 100, 100, 100, 100],
                                     [101, 102.01, 103.03, 102, 100.98, 99.97]]

        fp_bet = FixedPercentage(bet_results, prob_info)
        fp_bet.simulate_strategy()
        # print(fp_bet.bankroll_values)
        self.assertEqual(expected_running_bankroll, fp_bet.bankroll_values)
        self.assertEqual(expected_bet_sizes, fp_bet.bet_sizes)

class MartingaleTest(unittest.TestCase):
    def test_bankroll_values(self):
        expected_bet_sizes = [[1, 1, 1, 1, 1, 1],
                              [1, 2, 4, 8, 8, 16],
                              [1, 2, 1, 2, 1, 2],
                              [1, 1, 1, 1, 1, 1],
                              [1, 2, 4, 8, 16, 32],
                              [1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 2, 4]]
        
        expected_running_bankroll = [[101, 102, 103, 103, 103, 104],
                                     [99, 97, 93, 93, 85, 69],
                                     [99, 101, 100, 102, 101, 103],
                                     [101, 102, 103, 104, 105, 106],
                                     [99, 97, 93, 85, 69, 37],
                                     [100, 100, 100, 100, 100, 100],
                                     [101, 102, 103, 102, 100, 96]]

        m_bet = Martingale(bet_results, prob_info)
        m_bet.simulate_strategy()
        # print(m_bet.bankroll_values)
        self.assertEqual(expected_running_bankroll, m_bet.bankroll_values)
        self.assertEqual(expected_bet_sizes, m_bet.bet_sizes)

class AntiMartingaleTest(unittest.TestCase):
    def test_bankroll_values(self):
        expected_bet_sizes = [[1, 2, 4, 8, 8, 8],
                              [1, 1, 1, 1, 1, 1],
                              [1, 1, 2, 1, 2, 1],
                              [1, 2, 4, 8, 16, 32],
                              [1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1],
                              [1, 2, 4, 8, 1, 1]]
        
        expected_running_bankroll = [[101, 103, 107, 107, 107, 115],
                                     [99, 98, 97, 97, 96, 95],
                                     [99, 100, 98, 99, 97, 98],
                                     [101, 103, 107, 115, 131, 163],
                                     [99, 98, 97, 96, 95, 94],
                                     [100, 100, 100, 100, 100, 100],
                                     [101, 103, 107, 99, 98, 97]]

        am_bet = AntiMartingale(bet_results, prob_info)
        am_bet.simulate_strategy()
        self.assertEqual(expected_running_bankroll, am_bet.bankroll_values)
        self.assertEqual(expected_bet_sizes, am_bet.bet_sizes)

class KellyCriterionTest(unittest.TestCase):
    def test_bankroll_values(self):
        expected_bet_sizes = [[25, 31.25, 39.06, 48.83, 48.83, 48.83],
                              [25, 18.75, 14.06, 10.55, 10.55, 7.91],
                              [25, 18.75, 23.44, 17.59, 21.97, 16.48],
                              [25, 31.25, 39.06, 48.83, 61.04, 76.3],
                              [25, 18.75, 14.06, 10.55, 7.91, 5.93],
                              [25, 25, 25, 25, 25, 25],
                              [25, 31.25, 39.06, 48.83, 36.62, 27.47]]
        
        expected_running_bankroll = [[125, 156.25, 195.31, 195.31, 195.31, 244.14],
                                     [75, 56.25, 42.19, 42.19, 31.64, 23.73],
                                     [75, 93.75, 70.31, 87.89, 65.92, 82.4],
                                     [125, 156.25, 195.31, 244.14, 305.18, 381.48],
                                     [75, 56.25, 42.19, 31.64, 23.73, 17.80],
                                     [100, 100, 100, 100, 100, 100],
                                     [125, 156.25, 195.31, 146.48, 109.86, 82.39]]

        kc_bet = KellyCriterion(bet_results, prob_info, pct=None, unit_size=1)
        kc_bet.simulate_strategy()

        self.assertEqual(expected_running_bankroll, kc_bet.bankroll_values)
        self.assertEqual(expected_bet_sizes, kc_bet.bet_sizes)

class WinnersBetTest(unittest.TestCase):
    def test_bankroll_values(self):

        expected_bet_sizes = [[1]*len(bet_results[0])]*len(bet_results)
        
        expected_running_bankroll = [[101, 102, 103, 103, 103, 104],
                                     [99, 98, 97, 97, 96, 95],
                                     [99, 100, 99, 100, 99, 100],
                                     [101, 102, 103, 104, 105, 106],
                                     [99, 98, 97, 96, 95, 94],
                                     [100, 100, 100, 100, 100, 100],
                                     [101, 102, 103, 102, 101, 100]]

        w_bet = WinnersBet(bet_results, prob_info)
        w_bet.simulate_strategy()
        self.assertEqual(expected_running_bankroll, w_bet.bankroll_values)
        self.assertEqual(expected_bet_sizes, w_bet.bet_sizes)

class FibonacciTest(unittest.TestCase):
    def test_bankroll_values(self):
        expected_bet_sizes = [[1, 1, 1, 1, 1, 1],
                              [1, 1, 2, 2, 3, 5],
                              [1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1],
                              [1, 1, 2, 3, 5, 8],
                              [1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 2]]
        
        expected_running_bankroll = [[101, 102, 103, 103, 103, 104],
                                     [99, 98, 96, 96, 93, 88],
                                     [99, 100, 99, 100, 99, 100],
                                     [101, 102, 103, 104, 105, 106],
                                     [99, 98, 96, 93, 88, 80],
                                     [100, 100, 100, 100, 100, 100],
                                     [101, 102, 103, 102, 101, 99]]
        f_bet = Fibonacci(bet_results, prob_info)
        f_bet.simulate_strategy()
        self.assertEqual(expected_running_bankroll, f_bet.bankroll_values)
        self.assertEqual(expected_bet_sizes, f_bet.bet_sizes)

class AntiFibonacciTest(unittest.TestCase):
    def test_bankroll_values(self):
        expected_bet_sizes = [[1, 1, 2, 2, 2, 3],
                              [1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1],
                              [1, 1, 2, 3, 5, 8],
                              [1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1],
                              [1, 1, 2, 3, 1, 1]]
        
        expected_running_bankroll = [[101, 102, 104, 104, 104, 107],
                                     [99, 98, 97, 97, 96, 95],
                                     [99, 100, 99, 100, 99, 100],
                                     [101, 102, 104, 107, 112, 120],
                                     [99, 98, 97, 96, 95, 94],
                                     [100, 100, 100, 100, 100, 100],
                                     [101, 102, 104, 101, 100, 99]]
        af_bet = AntiFibonacci(bet_results, prob_info)
        af_bet.simulate_strategy()
        self.assertEqual(expected_running_bankroll, af_bet.bankroll_values)
        self.assertEqual(expected_bet_sizes, af_bet.bet_sizes)

class DalembertTest(unittest.TestCase):
    def test_bankroll_values(self):
        expected_bet_sizes = [[1, 2, 3, 4, 4, 4],
                              [1, 1, 1, 1, 1, 1],
                              [1, 1, 2, 1, 2, 1],
                              [1, 2, 3, 4, 5, 6],
                              [1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1],
                              [1, 2, 3, 4, 3, 2]]
        
        expected_running_bankroll = [[101, 103, 106, 106, 106, 110],
                                     [99, 98, 97, 97, 96, 95],
                                     [99, 100, 98, 99, 97, 98],
                                     [101, 103, 106, 110, 115, 121],
                                     [99, 98, 97, 96, 95, 94],
                                     [100, 100, 100, 100, 100, 100],
                                     [101, 103, 106, 102, 99, 97]]
        
        d_bet = Dalembert(bet_results, prob_info)
        d_bet.simulate_strategy()
        self.assertEqual(expected_running_bankroll, d_bet.bankroll_values)
        self.assertEqual(expected_bet_sizes, d_bet.bet_sizes)

class AntiDalembertTest(unittest.TestCase):
    def test_bankroll_values(self):
        expected_bet_sizes = [[1, 1, 1, 1, 1, 1],
                              [1, 2, 3, 3, 4, 5],
                              [1, 2, 1, 2, 1, 2],
                              [1, 1, 1, 1, 1, 1],
                              [1, 2, 3, 4, 5, 6],
                              [1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 2, 3, 4]]
        
        expected_running_bankroll = [[101, 102, 103, 103, 103, 104],
                                     [99, 97, 94, 94, 90, 85],
                                     [99, 101, 100, 102, 101, 103],
                                     [101, 102, 103, 104, 105, 106],
                                     [99, 97, 94, 90, 85, 79],
                                     [100, 100, 100, 100, 100, 100],
                                     [101, 102, 103, 101, 98, 94]]
        
        ad_bet = AntiDalembert(bet_results, prob_info)
        ad_bet.simulate_strategy()
        self.assertEqual(expected_running_bankroll, ad_bet.bankroll_values)
        self.assertEqual(expected_bet_sizes, ad_bet.bet_sizes)

if __name__ == '__main__':
    unittest.main()
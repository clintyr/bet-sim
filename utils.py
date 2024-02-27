def convert_american_odds_return(odds: int):
    if odds < 0:
        ret = -100/odds
        ret = float(f"{ret:.2f}")
    else:
        ret = odds/100
    return ret

def convert_american_odds_implied_probability(odds: int):
    if odds < 0:
        prob = -odds/(-odds+100)
    else:
        prob = 100/(100+odds)
    return prob

def calculate_unit_bet_outcome(bet_result, bet_payout):
    if bet_result == 'W':
        return bet_payout
    if bet_result == 'Push':
        return 0
    if bet_result == 'L':
        return -1
    
def calculate_bet_outcome(bet_size, bet_result, bet_payout):
    return bet_size * calculate_unit_bet_outcome(bet_result, bet_payout)

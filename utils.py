
def determine_position(position_string):
    positions = ["Dealer", "Small Blind", "Big Blind", "UTG", "UTG+1", "UTG+2"]
    if not position_string in positions:
        raise Exception("Unknown position string detected")
    return positions.index(position_string)

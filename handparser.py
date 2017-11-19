
from os import listdir
from os.path import isfile, join
from models import Hand, Card, Player, HandHistory

hand_history_path = "/Users/lingtongsun/code/poker/hand_history/"
hand_history_files = [f for f in listdir(hand_history_path) if isfile(join(hand_history_path, f))]

hands = []
def parse(content, hands):
    temp_hands = content.split("\n\n")
    for hand in temp_hands:
        hand = hand.strip()

        # skip empty lines at the end of files
        if not hand:
            break

        hh = HandHistory(hand)
        hands.append(hh)
        break;


i = 0
for file_name in hand_history_files:
    file = open(hand_history_path + file_name, "r")
    parse(file.read(), hands)
    i = i + 1
    if i == 1:
        break


c = Card('s', 'J')
h = Hand('s', 'J', 'd', 'J')
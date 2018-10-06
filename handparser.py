
from os import listdir
from os.path import isfile, join
from models import HandHistory
import pygal

hand_history_path = "/Users/lingtongsun/code/poker/hand_history/ignition/1-2-new/"
hand_history_files = [f for f in listdir(hand_history_path) if isfile(join(hand_history_path, f))]

hands = []
############################################################
# Parsing
hands_dict = {}

def parse(content, hands):
    temp_hands = content.split("\n\n")
    for hand in temp_hands:
        hand = hand.strip()
        # skip empty lines at the end of files
        if not hand:
            break
        try:
            hh = HandHistory(hand)
            if hh.hand_number not in hands_dict:
                hands_dict[hh.hand_number] = hh;
                hands.append(hh)
        except:
            pass

for file_name in hand_history_files:
    file = open(hand_history_path + file_name, "r")
    parse(file.read(), hands)
print(hands.__len__())
print(hands_dict.__len__())

#############################################################
# Some Rendering

positions = [HandHistory.POSITION_DEALER, HandHistory.POSITION_SMALL_BLIND,
             HandHistory.POSITION_BIG_BLIND, HandHistory.POSITION_UTG,
             HandHistory.POSITION_UGT_PLUS_1, HandHistory.POSITION_UGT_PLUS_2]
winnings_by_position = {}
winnings_by_hand = {}
# initialization
for pos in positions:
    winnings_by_position[pos] = 0


for hand in hands:
    curr_seat = hand.my_position()
    winnings = hand.my_winnings()
    if not winnings_by_position.__contains__(curr_seat):
        raise Exception("Incorrect seating: " + curr_seat)

    curr_hand_type = hand.my_hand_type()
    if winnings_by_hand.__contains__(curr_hand_type):
        winnings_by_hand[curr_hand_type] += winnings
    else:
        winnings_by_hand[curr_hand_type] = winnings

    winnings_by_position[curr_seat] += winnings

sorted_by_position = sorted(winnings_by_position.items(), key=lambda x: x[1], reverse=True)
sorted_by_hand = sorted(winnings_by_hand.items(), key=lambda x: x[1], reverse=True)

# print (sorted_by_position)
# print(winnings_by_hand)


pos_graph = pygal.Bar()
sum1 = 0
sum2 = 0
for pair in sorted_by_position:
    pos_graph.add(pair[0], pair[1])
    sum1 += pair[1]
pos_graph.render_to_file('win_by_pos.svg')

hand_graph = pygal.Bar()
for pair in sorted_by_hand:
    print(pair[0] + ": "+ str(pair[1]))
    sum2 += pair[1]
    hand_graph.add(pair[0], pair[1])
hand_graph.render_to_file('win_by_hand.svg')

print(sum1)
print(sum2)

from treys.treys import Card, Deck, Evaluator
import matplotlib.pyplot as plt
import numpy as np

sixes = [
   Card.new('6s'),
   Card.new('6c')
]

fours = [
   Card.new('4s'),
   Card.new('4c')
]

ten_jack = [
   Card.new('Ts'),
   Card.new('Js')
]

king_queen = [
   Card.new('Ks'),
   Card.new('Qs')
]

# deck = Deck(fours)
# print(deck.size())
# print(deck)

# count = 0
# sums = set()
# for i in range(len(deck._FULL_DECK)):
#     for j in range(len(deck._FULL_DECK) - i - 1):
#         count += 1
#         sums.add(deck._FULL_DECK[i] + deck._FULL_DECK[j])

# print(count)
# print(len(sums))

# print(c.get_prime())



#### way one

# evaluator = Evaluator()
# pctiles = []
# for x in range(1000):
#     hand = fours
#     deck = Deck(hand)

#     board = deck.draw(5)
#     score = evaluator.evaluate(board, hand)
#     wins = 0
#     num_opp_hands_to_simulate = 990
#     for x in range(num_opp_hands_to_simulate):
#         seen_hards = hand + board
#         rem_deck = Deck(seen_hards)

#         opp_hand = rem_deck.draw(2)
#         opp_score = evaluator.evaluate(board, opp_hand)
#         if score > opp_score:
#             wins += 1

#     # pct_rank = (7462 - score) * 1.0 / 7462
#     win_percentage = 1.0 * wins / num_opp_hands_to_simulate
#     pctiles.append(win_percentage)


# print("done")
# percentiles = np.array(pctiles)
# print(np.mean(percentiles))

# ### way two

evaluator = Evaluator()
# print(Card.print_pretty_cards(fours))
pctiles = []
for x in range(2000):
   # print("=========== {}".format(x))
   hand = king_queen
   deck = Deck(hand)
   board = deck.draw(5)
   # print(Card.print_pretty_cards(fours))
   # print(Card.print_pretty_cards(board))
   score = evaluator.evaluate(board, hand)
   wins = 0
   losses = 0
   opp_hands = deck.get_all_possible_hands()
    
   #  num_opp_hands_to_simulate = 1225
   for j in range(len(opp_hands)):
      opp_hand = opp_hands[j]
      # print(Card.print_pretty_cards(opp_hand))

      # Card.print_pretty_cards(hand)
      # print("hello")
      #   Card.print_pretty_cards(board)
      #   print()
      #   Card.print_pretty_cards(opp_hand)
      #   print()
      opp_score = evaluator.evaluate(board, opp_hand)
      if score < opp_score:
         wins += 1
      if opp_score == score:
         wins += 0.5

    # pct_rank = (7462 - score) * 1.0 / 7462
   win_percentage = 1.0 * wins / len(opp_hands)
   pctiles.append(win_percentage)


print("done")
percentiles = np.array(pctiles)
print(np.mean(percentiles))

### way three

# evaluator = Evaluator()
# hand = ten_jack
# deck = Deck(hand)
# opp_hands = deck.get_all_possible_hands()

# pctiles = []
# for i in range(len(opp_hands)):
#    # print("=========== {}".format(x))
#    opp_hand = opp_hands[i]
#    # print(Card.print_pretty_cards(hand))
#    # print(Card.print_pretty_cards(opp_hand))

#    seen_cards = hand + opp_hand

#    wins = 0
#    losses = 0
#    for j in range(1000):
#       r_deck = Deck(seen_cards)
#       board = r_deck.draw(5)
#       score = evaluator.evaluate(board, hand)
#       opp_score = evaluator.evaluate(board, opp_hand)
#       if score < opp_score:
#          wins += 1
#       if opp_score < score:
#          losses += 1

#     # pct_rank = (7462 - score) * 1.0 / 7462
#    win_percentage = 1.0 * wins / (wins + losses)
#    # print(win_percentage)
#    pctiles.append(win_percentage)


# print("done")
# percentiles = np.array(pctiles)
# print(np.mean(percentiles))

### end 
print(np.mean(pctiles))

plt.hist(pctiles, bins = 50)
plt.show()

import numpy as np 

from treys.treys import Card

board = [
    Card.new('Ah'),
    Card.new('Kd'),
    Card.new('Jc')
]
hand = [
   Card.new('Qs'),
   Card.new('Th')
]

print(Card.print_pretty_cards(board + hand))

from treys.treys import Evaluator
evaluator = Evaluator()
print(evaluator.evaluate(board, hand))


from treys.treys import Deck
deck = Deck()
board = deck.draw(5)
player1_hand = deck.draw(2)
player2_hand = deck.draw(2)

print(Card.print_pretty_cards(board))
print(Card.print_pretty_cards(player1_hand))
print(Card.print_pretty_cards(player2_hand))

p1_score = evaluator.evaluate(board, player1_hand)
p2_score = evaluator.evaluate(board, player2_hand)
p1_class = evaluator.get_rank_class(p1_score)
p2_class = evaluator.get_rank_class(p2_score)

print("Player 1 hand rank = %d (%s)\n" % (p1_score, evaluator.class_to_string(p1_class)))
print("Player 2 hand rank = %d (%s)\n" % (p2_score, evaluator.class_to_string(p2_class)))


hands = [player1_hand, player2_hand]
evaluator.hand_summary(board, hands)

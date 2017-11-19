from utils import determine_position
from collections import deque
import re


class Card:
    def __init__(self, s, v):
        self.suit = s
        self.value = v

    def __str__(self):
        return self.value + self.suit


class Hand:
    def __init__(self, s1, v1, s2, v2):
        self.first = Card(s1, v1)
        self.second = Card(s2, v2)
        self.suited = s1 == s2

    def __str__(self):
        return self.first.__str__() + " " + self.second.__str__()


class Player:
    def __init__(self, s, p, is_me):
        self.stack = s
        self.seat = p
        self.position = determine_position(p)
        self.hand = None
        self.is_me = is_me

    def set_hand(self, h):
        self.hand = h

    def __str__(self):
        return self.seat + "($" + self.stack + "): " + self.hand.__str__()


class HandHistory:
    REGEX_TITLE = "^Ignition Hand #([0-9]{10})"
    REGEX_PHASE = "^\*\*\* ([A-Z ]*) \*\*\*$"
    REGEX_SEAT = "(Dealer|Small Blind|Big Blind|UTG|UTG\\+1|UTG\\+2) (\\[ME\\] )?"
    REGEX_SEATING = "^Seat [0-9]: " + REGEX_SEAT + "\\(\\$(\\d+(\\.\\d{1,2})?) in chips\\)$"
    REGEX_CARD = "([2-9TJQKA][sdhc])"
    REGEX_HC = "^" + REGEX_SEAT + ": Card dealt to a spot \\[" + REGEX_CARD + " " + REGEX_CARD + "\\] $"
    PHASES = ["INITIAL", "HOLE CARDS", "FLOP", "TURN", "RIVER", "SUMMARY"]

    PHASE_INITIAL = 0
    PHASE_HC = 1
    PHASE_FLOP = 2
    PHASE_TURN = 3
    PHASE_RIVER = 4
    PHASE_SUMMARY = 5

    def __init__(self, c):
        self.content_string = c
        self.players = {}
        self.hand_number = None
        self.parse()

    @staticmethod
    def is_phase_valid(phase):
        if phase < 0 or phase > HandHistory.PHASE_SUMMARY:
            return False
        return True

    def parse(self):
        input = self.content_string.split('\n')
        queue = deque(input)
        count = 0
        curr_phase = HandHistory.PHASE_INITIAL

        while len(queue) > 0:
            line = queue.popleft()
            count += 1

            # header
            if count == 1:
                rx_matcher = re.compile(HandHistory.REGEX_TITLE)
                self.hand_number = rx_matcher.match(line).group(1)
                if self.hand_number is None:
                    raise Exception("Failed to parse hand number")
                print("=== " + self.hand_number)
                continue

            # hand phase headers (flop, turn, river, etc)
            phase_header = re.match(HandHistory.REGEX_PHASE, line)
            if phase_header is not None:
                phase_str = phase_header.group(1)
                # find the current phase at the signal
                curr_phase = HandHistory.PHASES.index(phase_str)
                if not self.is_phase_valid(curr_phase):
                    raise Exception("Failed to parse hand phase")
                print(phase_str + ": " + str(curr_phase))
                continue

            if curr_phase == HandHistory.PHASE_INITIAL:
                rx_matcher = re.compile(HandHistory.REGEX_SEATING)
                match_obj = rx_matcher.match(line)

                # seating
                if match_obj is not None:
                    position = match_obj.group(1)
                    is_me = match_obj.group(2)
                    stack = match_obj.group(3)
                    player = Player(stack, position, is_me is not None)
                    print(player)
                    self.players[position] = player
                    continue
                # parse action(blind info) later

            print(curr_phase)
            if curr_phase == HandHistory.PHASE_HC:
                hc_matcher = re.compile(HandHistory.REGEX_HC)
                print(line)
                match_obj = hc_matcher.match(line)

                if match_obj is not None:
                    print ("hi")

                    position = match_obj.group(1)
                    first = match_obj.group(2)
                    second = match_obj.group(3)
                    print (position)
                    print (first + ", " + second)
                    player = self.players.get(position)
                    player.hand = Hand(first[0], first[1], second[0], second[1])
                    print(player.hand)

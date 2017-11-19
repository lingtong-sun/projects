from utils import determine_position
from collections import deque
import re


class Card:
    def __init__(self, v, s):
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
    ROUND_PREFLOP = 0
    ROUND_FLOP = 1
    ROUND_TURN = 2
    ROUND_RIVER = 3

    def __init__(self, s, p, is_me):
        self.stack = s
        self.seat = p
        self.position = determine_position(p)
        self.hand = None
        self.is_me = is_me
        self.hand_result = 0.0
        # preflop, flop, turn, river
        self.bets = [0, 0, 0, 0]

    def set_hand(self, h):
        self.hand = h

    def total_bets(self):
        return sum(self.bets)

    def set_hand_result(self, result):
        self.hand_result = result

    def bet(self, r, amount):
        if r < Player.ROUND_PREFLOP or r > Player.ROUND_RIVER:
            raise Exception("Invalid betting detected.")
        self.bets[r] += amount

    def bet_to(self, r, amount):
        if r < Player.ROUND_PREFLOP or r > Player.ROUND_RIVER:
            raise Exception("Invalid betting detected.")
        self.bets[r] = amount

    def net_result(self):
        return float(self.hand_result) - self.total_bets()

    def __str__(self):
        return self.seat + "($" + str(self.stack) + "): " + self.hand.__str__() + " ==> $" + str(self.net_result())


class HandHistory:
    REGEX_TITLE = "^Ignition Hand #([0-9]{10})"
    REGEX_PHASE = "^\*\*\* ([A-Z ]*) \*\*\*"
    REGEX_SEAT = "(Dealer|Small Blind|Big Blind|UTG|UTG\\+1|UTG\\+2) ( ?\\[ME\\] )?"
    REGEX_MONEY = "\\$(\\d+(\\.\\d{1,2})?)"
    REGEX_SEATING = "^Seat [0-9]: " + REGEX_SEAT + "\\(" + REGEX_MONEY + " in chips\\)$"
    REGEX_CARD = "([2-9TJQKA][sdhc])"
    REGEX_HC = "^" + REGEX_SEAT + ": Card dealt to a spot \\[" + REGEX_CARD + " " + REGEX_CARD + "\\] $"
    REGEX_MOVE = "(Small Blind|Big [bB]lind|Calls|Bets|Raises|All-in|All-in\\(raise\\))"
    REGEX_ACTION = "^" + REGEX_SEAT + ": " + REGEX_MOVE + " " + REGEX_MONEY
    REGEX_OTHER_ACTIONS = "^.*(Folds|[Ll]eave|Checks|[Ee]nter|Set dealer|[Dd]eposit|Does not show|Showdown|" \
                          "sit out|re-join|stand|[Mm]ucks).*"
    REGEX_RETURN = "^" + REGEX_SEAT + ": Return uncalled portion of bet " + REGEX_MONEY
    REGEX_RESULT = "^" + REGEX_SEAT + ": (Hand result|Hand result-Side pot) " + REGEX_MONEY
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
        self.sanity_check()

    def __str__(self):
        ret = ""
        for k, player in self.players.items():
            ret += player.__str__() + "\n"
        return ret

    @staticmethod
    def is_phase_valid(phase):
        if phase < 0 or phase > HandHistory.PHASE_SUMMARY:
            return False
        return True

    def parse_header(self, line):
        # header
        rx_matcher = re.compile(HandHistory.REGEX_TITLE)
        self.hand_number = rx_matcher.match(line).group(1)
        if self.hand_number is None:
            raise Exception("Failed to parse hand number")

    def parse_phase_header(self, curr_phase, line):
        # hand phase headers (flop, turn, river, etc)
        phase_header = re.match(HandHistory.REGEX_PHASE, line)
        if phase_header is not None:
            phase_str = phase_header.group(1)
            # find the current phase at the signal
            new_phase = HandHistory.PHASES.index(phase_str)
            if not self.is_phase_valid(new_phase):
                raise Exception("Failed to parse hand phase")
            return new_phase
        return curr_phase

    def parse_seating(self, line):
        rx_matcher = re.compile(HandHistory.REGEX_SEATING)
        match_obj = rx_matcher.match(line)

        # seating
        if match_obj is not None:
            position = match_obj.group(1)
            is_me = match_obj.group(2)
            stack = match_obj.group(3)
            player = Player(stack, position, is_me is not None)
            self.players[position] = player
            return True
        return False

    def parse_dealing(self, line):
        hc_matcher = re.compile(HandHistory.REGEX_HC)
        match_obj = hc_matcher.match(line)

        if match_obj is not None:
            position = match_obj.group(1)
            is_me = match_obj.group(2)
            first = match_obj.group(3)
            second = match_obj.group(4)
            player = self.players.get(position)
            player.hand = Hand(first[0], first[1], second[0], second[1])
            return True
        return False

    def parse_action(self, line, curr_phase):
        # align parse phasing with betting round
        r = curr_phase - 1
        if r < 0:
            r = 0

        action_matcher = re.compile(HandHistory.REGEX_ACTION)
        match_obj = action_matcher.match(line)

        if match_obj is not None:
            position = match_obj.group(1)
            is_me = match_obj.group(2)
            action = match_obj.group(3)
            amount = match_obj.group(4)
            player = self.players.get(position)
            player.bet(r, float(amount))
            return

        return_matcher = re.compile(HandHistory.REGEX_RETURN)
        match_obj = return_matcher.match(line)
        if match_obj is not None:
            position = match_obj.group(1)
            is_me = match_obj.group(2)
            amount = match_obj.group(3)
            player = self.players.get(position)
            player.bet(r, -float(amount))
            return

        nonaction_matcher = re.compile(HandHistory.REGEX_OTHER_ACTIONS)
        if nonaction_matcher.match(line) is not None:
            return

        result_matcher = re.compile(HandHistory.REGEX_RESULT)
        match_obj = result_matcher.match(line)
        if match_obj is not None:
            position = match_obj.group(1)
            is_me = match_obj.group(2)
            result = match_obj.group(4)
            player = self.players.get(position)
            player.set_hand_result(result)
            return

        raise Exception("Unexpect parsing error during action.")

    def parse(self):
        input = self.content_string.split('\n')
        queue = deque(input)
        count = 0
        curr_phase = HandHistory.PHASE_INITIAL

        while len(queue) > 0:
            line = queue.popleft()
            print(line)
            count += 1

            # header
            if count == 1:
                self.parse_header(line)
                continue

            new_phase = self.parse_phase_header(curr_phase, line)
            if new_phase != curr_phase:
                curr_phase = new_phase
                continue

            if curr_phase == HandHistory.PHASE_INITIAL:
                if self.parse_seating(line):
                    continue
                # parse action(blind info) later
                self.parse_action(line, curr_phase)
                continue

            if curr_phase == HandHistory.PHASE_HC:
                if self.parse_dealing(line):
                    continue
                self.parse_action(line, curr_phase)
                # parse action

            if curr_phase == HandHistory.PHASE_FLOP or curr_phase == HandHistory.PHASE_TURN or curr_phase == HandHistory.PHASE_RIVER:
                self.parse_action(line, curr_phase)

            if curr_phase == HandHistory.PHASE_SUMMARY:
                #do something
                continue

    def sanity_check(self):
        total = 0
        totalpot = 0
        for k, player in self.players.items():
            total += player.net_result()
            totalpot += abs(player.net_result())
        if total > totalpot * 0.05:
            raise Exception("Sanity Check Failed.")

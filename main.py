# Import the set of lower cased english wrds (without punctuation)
from english_words import english_words_lower_alpha_set
from Player import Player
from random import randint


def getNewServerWord(server_word, new_word):
    new_server_word = ''
    find_start_index = len(server_word) - len(new_word)
    for i in range(len(new_word)):
        substrng = new_word[0:len(new_word) - i]
        server_idx = server_word.find(substrng, find_start_index + i)
        if server_idx == -1 or server_idx + len(substrng) < len(server_word):
            if i == len(new_word) - 1:
                new_server_word = server_word + new_word
                score = 0
                return new_server_word, score
            continue;
        segment = new_word[len(substrng)::]
        new_server_word = server_word + segment
        score = len(substrng) * len(substrng)
        return new_server_word, score


def mirrorWord(word):
    bdmw_dict = dict()
    bdmw_dict['b'] = []
    bdmw_dict['d'] = []
    bdmw_dict['m'] = []
    bdmw_dict['w'] = []

    mirror_dict = dict()
    mirror_dict['b'] = 'd'
    mirror_dict['d'] = 'b'
    mirror_dict['m'] = 'w'
    mirror_dict['w'] = 'm'

    for index, letter in enumerate(word):
        if letter == 'b':
            bdmw_dict['b'].append(index)
        if letter == 'd':
            bdmw_dict['d'].append(index)
        if letter == 'm':
            bdmw_dict['m'].append(index)
        if letter == 'w':
            bdmw_dict['w'].append(index)

    for key in bdmw_dict:
        idxs = bdmw_dict[key]
        new_character = mirror_dict[key]
        for index in idxs:
            word = word[:index] + new_character + word[index + 1:]

    return word


def run(num_rounds, num_players):
    players = dict()
    scores = dict()
    for i in range(1, num_players + 1):
        p = Player()
        pid = 'player' + str(i)
        players[pid] = p
        scores[pid] = 0

    game_words_played_set = set()
    game_words_played_list = []
    current_server_word = ''

    minlen_words = []
    for word in english_words_lower_alpha_set:
        if len(word) >= 8:
            minlen_words.append(word)
        if len(minlen_words) == 30:
            break

    starting_word = minlen_words[randint(0, len(minlen_words) - 1)]
    game_words_played_set.add(starting_word)
    game_words_played_list.append(starting_word)

    total_rounds = num_rounds
    current_round = 1
    current_server_word = starting_word

    print('SERVER WORD:   ', starting_word)
    while current_round <= total_rounds:
        print('\n____________________Round ', current_round, '____________________')

        for i in range(1, num_players + 1):
            pid = 'player' + str(i)
            player = players[pid]
            player_powers_used, player_words_played = player.play(current_server_word, game_words_played_set,
                                                                  total_rounds - current_round + 1, total_rounds, i)
            # Checks
            while len(player_powers_used) == 0 or len(player_words_played) == 0 or len(player_powers_used) != len(
                    player_words_played) or (len(player_powers_used) == 1 and player_powers_used[0] == 'gotwice'):
                player_powers_used, player_words_played = player.play(current_server_word, game_words_played_set,
                                                                      total_rounds - current_round + 1, total_rounds, i)

            for index, value in enumerate(player_powers_used):
                if value == 'flip':
                    temp_server_word = current_server_word[::-1]
                elif value == 'mirror':
                    temp_server_word = mirrorWord(current_server_word)
                elif value == 'remove':
                    temp_server_word = current_server_word[0:len(current_server_word) - 1]
                elif value == 'gotwice' or value == 'nopower':
                    temp_server_word = current_server_word
                current_server_word, sc = getNewServerWord(temp_server_word, player_words_played[index])
                scores[pid] += sc
                print(pid, ': Power Used - ', value, '  | Word Played - ', player_words_played[index],
                      '  | Points Gained - ', sc, '  | Player1 Score - ', scores[pid])
                print('SERVER WORD:   ', current_server_word)
                game_words_played_set.add(player_words_played[index])
                game_words_played_list.append(player_words_played[index])

        current_round += 1

        printResults(scores)


def printResults(scores):
    max_score = 0
    winners = []
    print('\n --------------- Final Scores: ---------------')
    for pid in scores:
        print(pid, ' -> ', scores[pid])
        if scores[pid] > max_score:
            max_score = scores[pid]

    for pid in scores:
        if scores[pid] == max_score:
            winners.append(pid)

    if len(winners) == 1:
        print(winners[0], ' Wins !!! ')
    elif len(winners) > 1:
        print('It is a tie between ', winners)
    else:
        print('Something went wrong :( ')


if __name__ == '__main__':
    num_rounds = 7
    num_players = 5
    run(num_rounds, num_players)

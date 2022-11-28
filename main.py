# Import the set of lower cased english wrds (without punctuation)
from english_words import english_words_lower_alpha_set
from Player import Player
from random import randint


def getNewServerWord(server_word, new_word):
    new_server_word = ''
    find_start_index = len(server_word) - len(new_word)
    for i in range(len(new_word)):
        substrng = new_word[0:len(new_word) - i]
        server_idx = server_word.find(substrng, find_start_index+i)
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
    player1 = Player()
    player2 = Player()

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

    player1_score = 0
    player2_score = 0

    print('SERVER WORD:   ', starting_word)
    while current_round <= total_rounds:
        print('\n____________________Round ', current_round, '____________________')
        # Client 1 plays first
        player1_powers_used, player1_words_played = player1.play(current_server_word, game_words_played_set,
                                                                 total_rounds - current_round + 1, total_rounds, 1)

        # Checks
        while len(player1_powers_used) == 0 or len(player1_words_played) == 0 or len(player1_powers_used) != len(
                player1_words_played) or (len(player1_powers_used) == 1 and player1_powers_used[0] == 'gotwice'):
            player1_powers_used, player1_words_played = player1.play(current_server_word, game_words_played_set,
                                                                     total_rounds - current_round + 1, total_rounds,
                                                                     1)

        for index, value in enumerate(player1_powers_used):
            if value == 'flip':
                temp_server_word = current_server_word[::-1]
            elif value == 'mirror':
                temp_server_word = mirrorWord(current_server_word)
            elif value == 'remove':
                temp_server_word = current_server_word[0:len(current_server_word) - 1]
            elif value == 'gotwice' or value == 'nopower':
                temp_server_word = current_server_word
            current_server_word, sc = getNewServerWord(temp_server_word, player1_words_played[index])
            player1_score += sc
            print('Player1: Power Used - ', value, '  | Word Played - ', player1_words_played[index],
                  '  | Points Gained - ', sc, '  | Player1 Score - ', player1_score)
            print('SERVER WORD:   ', current_server_word)
            game_words_played_set.add(player1_words_played[index])
            game_words_played_list.append(player1_words_played[index])

        # Client 2 plays second
        player2_powers_used, player2_words_played = player2.play(current_server_word, game_words_played_set,
                                                                 total_rounds - current_round + 1, total_rounds, 2)

        # Checks
        while len(player2_powers_used) == 0 or len(player2_words_played) == 0 or len(player2_powers_used) != len(
                player2_words_played) or (len(player2_powers_used) == 1 and player2_powers_used[0] == 'gotwice'):
            client2_powers_used, player2_words_played = player2.play(current_server_word, game_words_played_set,
                                                                     total_rounds - current_round + 1, total_rounds,
                                                                     2)

        for index, value in enumerate(player2_powers_used):
            if value == 'flip':
                temp_server_word = current_server_word[::-1]
            elif value == 'mirror':
                temp_server_word = mirrorWord(current_server_word)
            elif value == 'remove':
                temp_server_word = current_server_word[0:len(current_server_word) - 1]
            elif value == 'gotwice' or value == 'nopower':
                temp_server_word = current_server_word
            current_server_word, sc = getNewServerWord(temp_server_word, player2_words_played[index])
            player2_score += sc
            print('Player2: Power Used - ', value, '  | Word Played - ', player2_words_played[index],
                  '  | Points Gained - ', sc, '  | Player2 Score - ', player2_score)
            print('SERVER WORD:   ', current_server_word)
            game_words_played_set.add(player2_words_played[index])
            game_words_played_list.append(player2_words_played[index])

        current_round += 1

    if player1_score > player2_score:
        print('Client 1 wins!')
    elif player1_score < player2_score:
        print('Client 2 wins!')
    else:
        print('Its a tie!')


if __name__ == '__main__':
    num_rounds = 7
    num_players = 2
    run(num_rounds, num_players)

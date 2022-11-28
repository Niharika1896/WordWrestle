from random import randint
from english_words import english_words_lower_alpha_set
from Trie import Trie, TrieNode


class Player:
    def __init__(self):
        self.wordwrestle_trie = Trie()
        all_words_list = list(english_words_lower_alpha_set)
        self.wordwrestle_trie.build(all_words_list)

        self.spl_pow_dict = dict()
        self.spl_pow_dict['gotwice'] = 1
        self.spl_pow_dict['flip'] = 1
        self.spl_pow_dict['remove'] = 1
        self.spl_pow_dict['mirror'] = 1

        self.game_words_played = set()

    def getNextWordToPlay(self, root_word: str):
        for i in range(len(root_word)):
            base_word = root_word[i:len(root_word)]
            play_options = self.wordwrestle_trie.autocomplete(base_word)
            play_word = ''
            for option in play_options:
                if option not in self.game_words_played:
                    play_word = option
                    break
            if play_word == '':
                continue
            score = len(root_word) - i
            score = score * score

            return play_word, score

    def mirrorWord(self, word):
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

    def getNextWordGoTwice(self, server_word, last_word_played, words_to_play, powers_to_use):
        new_server_word = ''
        find_start_index = len(server_word) - len(last_word_played)
        for i in range(len(last_word_played)):
            substrng = last_word_played[0:len(last_word_played) - i]
            server_idx = server_word.find(substrng, find_start_index+i)
            if server_idx == -1 or server_idx + len(substrng) < len(server_word):
                if i == len(last_word_played) - 1:
                    new_server_word = server_word + last_word_played
                continue;
            segment = last_word_played[len(substrng)::]
            new_server_word = server_word + segment
            break

        new_word_to_play, score = self.getNextWordToPlay(new_server_word)
        # print(new_word_to_play, ' - ', score)

        words_to_play.append(new_word_to_play)
        self.game_words_played.add(new_word_to_play)
        powers_to_use.append('gotwice')

    def play(self, server_word, words_played, turns_left, total_rounds, turn):
        for word in words_played:
            self.game_words_played.add(word)

        no_spl_power_score = -1
        flip_power_score = -1
        removelast_power_score = -1
        mirror_power_score = -1

        powers_to_use = []
        words_to_play = []

        # Get the next word to play and score in all cases
        no_spl_power_word_option, no_spl_power_score = self.getNextWordToPlay(server_word)
        if self.spl_pow_dict['flip'] == 1:
            flipped_server_word = server_word[::-1]
            flip_power_word_option, flip_power_score = self.getNextWordToPlay(flipped_server_word)
        if self.spl_pow_dict['remove'] == 1:
            removelast_server_word = server_word[0:len(server_word) - 1]
            removelast_power_word_option, removelast_power_score = self.getNextWordToPlay(removelast_server_word)
        if self.spl_pow_dict['mirror'] == 1:
            mirror_server_word = self.mirrorWord(server_word)
            mirror_power_word_option, mirror_power_score = self.getNextWordToPlay(mirror_server_word)

        # Compare the scores obtained in all cases and play the turn that gives maximum score
        if flip_power_score > no_spl_power_score and flip_power_score >= removelast_power_score and flip_power_score >= mirror_power_score:
            words_to_play.append(flip_power_word_option)
            self.game_words_played.add(flip_power_word_option)
            powers_to_use.append('flip')
            self.spl_pow_dict['flip'] = 0
            if flip_power_word_option[-1] not in ['q', 'w', 'y', 'u', 'd', 'f', 'g', 'z', 'x', 'v', 'b'] and \
                    self.spl_pow_dict['gotwice'] == 1:
                self.getNextWordGoTwice(flipped_server_word, flip_power_word_option, words_to_play, powers_to_use)
                self.spl_pow_dict['gotwice'] = 0

        elif removelast_power_score >= flip_power_score and removelast_power_score > no_spl_power_score and removelast_power_score >= mirror_power_score:
            words_to_play.append(removelast_power_word_option)
            self.game_words_played.add(removelast_power_word_option)
            powers_to_use.append('remove')
            self.spl_pow_dict['remove'] = 0
            if removelast_power_word_option[-1] not in ['q', 'w', 'y', 'u', 'd', 'f', 'g', 'z', 'x', 'v', 'b'] and \
                    self.spl_pow_dict['remove'] == 1:
                self.getNextWordGoTwice(removelast_server_word, removelast_power_word_option, words_to_play,
                                        powers_to_use)
                self.spl_pow_dict['gotwice'] = 0

        elif mirror_power_score >= flip_power_score and mirror_power_score > no_spl_power_score and mirror_power_score >= removelast_power_score:
            words_to_play.append(mirror_power_word_option)
            self.game_words_played.add(mirror_power_word_option)
            powers_to_use.append('mirror')
            self.spl_pow_dict['mirror'] = 0
            if mirror_power_word_option[-1] not in ['q', 'w', 'y', 'u', 'd', 'f', 'g', 'z', 'x', 'v', 'b'] and \
                    self.spl_pow_dict['mirror'] == 1:
                self.getNextWordGoTwice(mirror_server_word, mirror_power_word_option, words_to_play, powers_to_use)
                self.spl_pow_dict['gotwice'] = 0

        elif no_spl_power_score >= flip_power_score and no_spl_power_score >= removelast_power_score and no_spl_power_score >= mirror_power_score:
            words_to_play.append(no_spl_power_word_option)
            self.game_words_played.add(no_spl_power_word_option)
            powers_to_use.append('nopower')
            self.game_words_played.add(no_spl_power_word_option)
            if no_spl_power_word_option[-1] not in ['q', 'w', 'y', 'u', 'd', 'f', 'g', 'z', 'x', 'v', 'b'] and \
                    self.spl_pow_dict['gotwice'] == 1:
                self.getNextWordGoTwice(server_word, no_spl_power_word_option, words_to_play, powers_to_use)
                self.spl_pow_dict['gotwice'] = 0

        return powers_to_use, words_to_play

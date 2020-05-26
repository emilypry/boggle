import string
import random
import nltk
english_vocab = set(w.lower() for w in nltk.corpus.words.words())

class Game:
    def __init__(self, points = 0, words_already_played = []):
        self.points = points
        self.words_already_played = words_already_played

    def print_points(self):
        msg = 'You currently have'
        if self.points == 1:
            print(msg, self.points, 'point.')
        else:
            print(msg, self.points, 'points.')
    
    def add_word(self, word):
        self.words_already_played.append(word)

class Board:
    def __init__(self, letters):
        self.letters = letters

def make_board():
    '''Draws collections of vowels and consonants, and puts them in a shuffled list. Consonants are more likely to show up on the board than vowels. 
    '''
    letters = []
    vowels = ['a', 'e', 'i', 'o', 'u'] 
    easy_consonants = ['d', 'l', 'm', 'n', 'r', 's', 't']
    hard_consonants = ['b', 'c', 'f', 'g', 'h', 'j', 'k', 'p', 'q', 'v', 'w', 'x', 'y', 'z']

    while len(letters) < 16:
        vow_ind = random.randint(0, 4)
        easy_con_ind = random.randint(0, 6)
        hard_con_ind = random.randint(0, 13)

        vow_or_con = random.randint(0,2)
        if vow_or_con == 0:
            letters.append(vowels[vow_ind])
            letters.append(easy_consonants[easy_con_ind])
        elif vow_or_con == 1:
            letters.append(hard_consonants[hard_con_ind])
            letters.append(vowels[vow_ind])
        else:
            letters.append(easy_consonants[easy_con_ind])
 
    board = Board(letters)
    return board

def print_board(board):
    '''Prints the board. Returns nothing.
    '''
    line_num = 0
    i = 0

    while line_num < 4:
        print(board.letters[i]+'  '+board.letters[i+1]+'  '+board.letters[i+2]+'  '+board.letters[i+3])
        i += 4
        line_num += 1

def check_length(text):
    '''Checks if the text is at least three letters long. Returns boolean.
    '''
    if len(text)<3:
        return False
    return True

def check_letters(board, text):
    '''Checks if all letters in the text appear somewhere on the board. Returns boolean. 
    '''
    for x in text:
        if x not in board.letters:
            return False
    return True

def check_word(text):
    '''Checks if the word is an English word. Returns boolean.
    '''
    if text in english_vocab:
        return True
    else:
        return False

def get_indices(board, a):
    '''Gets the index/indices of a given letter in a board. Returns the indices as a list.
    '''
    indices = []
    i = 0
    while i < 16:
        if board.letters[i] == a:
            indices.append(i)
        i+=1

    return indices

def check_horizontally(board, a, b):
    '''Checks if two letter-types appear next to each other horizontally on a board. Returns a list containing lists of two indices of letter-types that appear next to each other horizontally. 
    '''
    all_a = get_indices(board, a)
    all_b = get_indices(board, b)
    true_of = []
    
    for i_a in all_a:
        for i_b in all_b:
            pair = []

            # If the smaller index is 3, 7, or 11, that means that it is on the right edge of the board, and moving from the right edge of the board (say, at index 3) to the left edge of the board (say, at index 4) does not count as a horizontal connection. 
            if i_a - 1 == i_b and (i_b != 3 and i_b != 7 and i_b != 11):
                pair.append(i_a)
                pair.append(i_b)
                true_of.append(pair)
            elif i_a + 1 == i_b and (i_a != 3 and i_a != 7 and i_a != 11):
                pair.append(i_a)
                pair.append(i_b)
                true_of.append(pair)
    
    return true_of

def check_vertically(board, a, b):
    '''Checks if two letter-types appear next to each other vertically on a board. Returns a list containing lists of two indices of letter-types that appear next to each other vertically. 
    '''
    all_a = get_indices(board, a)
    all_b = get_indices(board, b)
    true_of = []

    for i_a in all_a:
        for i_b in all_b:
            pair = []
            if i_a - 4 == i_b:
                pair.append(i_a)
                pair.append(i_b)
                true_of.append(pair)
            elif i_a + 4 == i_b:
                pair.append(i_a)
                pair.append(i_b)
                true_of.append(pair)
    
    return true_of

def check_diagonally(board, a, b):
    '''Checks if two letter-types appear next to each other diagonally on a board. Returns a list containing lists of two indices of letter-types that appear next to each other diagonally. 
    '''   
    all_a = get_indices(board, a)
    all_b = get_indices(board, b)
    true_of = []

    for i_a in all_a:
        for i_b in all_b:
            pair = []

            # If the larger index is 5 greater than the smaller index, and is 8 or 12, because it is on the left edge of the board, it can't connect to an index 5 less than it via a diagonal. 
            if i_a - 5 == i_b and (i_a != 8 and i_a != 12):
                pair.append(i_a)
                pair.append(i_b)
                true_of.append(pair)

            # If the smaller index is 5 less than the larger index, and is 3 or 7, because it is on the right edge of the board, it can't connect to an index 5 greater than it via a diagonal. 
            elif i_a + 5 == i_b and (i_a != 3 and i_a != 7):
                pair.append(i_a)
                pair.append(i_b)
                true_of.append(pair)

            # If the larger index is 3 greater than the smaller index, and is 3, 7, 11, or 15, because it is on the right edge of the board, it can't connect to another index 3 less than it via a diagonal. 
            elif i_a - 3 == i_b and (i_a != 3 and i_a != 7 and i_a != 11 and i_a != 15):
                pair.append(i_a)
                pair.append(i_b)
                true_of.append(pair)

            # If the smaller index is 3 less than the larger index, and is 0, 4, 8, or 12, because it is on the left edge of the board, it can't connect to another index 3 greater than it via a diagonal. 
            elif i_a + 3 == i_b and (i_a != 0 and i_a != 4 and i_a != 8 and i_a != 12):
                pair.append(i_a)
                pair.append(i_b)
                true_of.append(pair)

    return true_of


def check_if_connected(board, text):
    '''Checks if the text follows the rules of connection. Returns boolean. 
    '''
    #For each set of two consecutive letters in text, combine lists of indices for all horizontal, vertical, and diagonal connections for that letter pair into connections_for_pair. Then add connections_for_pair to all_cons_for_let_set, which is a list (for the entire text) of the lists (for each letter pair) showing the connections between each set of two consecutive letters in text. 
    num_of_pairs = len(text) - 1
    ind_pair = 0
    ind_let = 0
    all_cons_for_let_set = []
    while ind_pair < num_of_pairs:
        connections_for_pair = []
        connections_for_pair.extend(check_horizontally(board, text[ind_let], text[ind_let+1]))
        connections_for_pair.extend(check_vertically(board, text[ind_let], text[ind_let+1]))
        connections_for_pair.extend(check_diagonally(board, text[ind_let], text[ind_let+1]))

        all_cons_for_let_set.append(connections_for_pair)

        ind_pair += 1
        ind_let += 1

    # We already have sets of two consecutive letters that are connected on the board. Now we need sets of three, four, etc. until we finally have the length of text, showing that each letter in text is connected in the right way. con_length is the number of consecutive letters that we've shown are connected so far. 
    con_length = 2
    while con_length < len(text):

        # Get the list of connections for a set of con_length (size) letters in text, and the list of connections for the following set of con_length (size) letters in text. For each connection, check if all of its indices after the first one are identical to all but the final index for any connection in the following list of connections. If it is, that means that the first con_length (size) characters of text are connected to each other in some way. 
    
        # cons_for_let_set indexes a given list of connections for a set of con_length letters in text. cons_for_let_set_plus_one is a list for all discovered connections for a set of con_length+1 letters in text.
        cons_for_let_set = 0
        cons_for_let_set_plus_one = []
        while cons_for_let_set < len(all_cons_for_let_set) - 1:

            # For each particular connection in one list of connections for a set of of con_length letters, see if the final indices of that connection appear as the first indices of some connection in the following list of connections. If so, create a new list of con_length+1 consisting the indices of the first connection and the final index of the second connection. Store all of these for this list of connections in cons_for_a_set, and add it to cons_for_let_set_plus_one.
            cons_for_a_set = []
            for a_con_in_set in all_cons_for_let_set[cons_for_let_set]:
                for a_con_in_next_set in all_cons_for_let_set[cons_for_let_set+1]:
                    
                    if a_con_in_set[1:] == a_con_in_next_set[0:con_length-1]:
                        new_con = [] 
                        for num in a_con_in_set:
                            new_con.append(num)

                        new_con.append(a_con_in_next_set[-1])
                        cons_for_a_set.append(new_con)
            
            cons_for_let_set_plus_one.append(cons_for_a_set)

            cons_for_let_set +=1
            
        # Now we have something like what we started off with: a list of lists of indices of con_length+1. Need to run them through again (where con_length += 1, all_cons_for_let_set == cons_for_let_set_plus_one.
        all_cons_for_let_set = cons_for_let_set_plus_one
        con_length += 1

    # Get rid of extra pair of brackets in all_cons_for_let_set. 
    all_cons = []
    for con in all_cons_for_let_set:
        all_cons.extend(con)

    # But still not sufficient for getting rid of all badnesses; need to go through all lists of indices and make sure at least one of them has no repeated indices (since that would mean the word used a given index on a board multiple times, which isn't allowed).
    good_word = False
    for a_list_of_indices in all_cons:
        if len(a_list_of_indices) == len(set(a_list_of_indices)):
            good_word = True
            break
    
    return good_word

def check_text(board, text, game):    
    '''Checks if text is a legitimate word on the board. Returns a boolean and a message about whether the word was legitimate or not - if not, says why.
    '''
    msg = 'Good word!'

    if check_length(text) == False:
        msg = 'Words must be at least three characters long.'
        return False, msg
    if check_letters(board, text) == False:
        msg = 'Not all of those characters are on the board.'
        return False, msg
    if check_word(text) == False:
        msg = 'That is not a real word.'
        return False, msg
    if check_if_connected(board, text) == False:
        msg = 'Not all of those characters are properly connected.'
        return False, msg
    if text in game.words_already_played:
        msg = "You've already played that word."
        return False, msg

    game.add_word(text)
    return True, msg
    
def get_points(game, text):
    '''Returns the number of points for a word played. 
    '''
    if len(text) < 5:
        return 1
    if len(text) < 6:
        return 2
    if len(text) < 7:
        return 3
    if len(text) < 8:
        return 5
    if len(text) >= 8:
        return 11

def feedback(game, board, text):
    '''Gives the player a message and (if applicable) points on the basis of the word they played.
    '''
    verdict = check_text(board, text, game)

    if verdict[0] == False:
        print(verdict[1])
        game.print_points()
    else:
        points = get_points(game, text)
        if points == 1:
            print('Good word! +' + str(points) + ' point')
        else:
            print('Good word! +' + str(points)+' points')
        game.points += points
        game.print_points()

def print_welcome():
    print('**********************************')
    print('WELCOME TO BOGGLE!')
    print('Find as many words as you can. The letters must be connected horizontally, vertically, and/or diagonally, and you cannot use a single letter multiple times in a word. Points are awarded based on the length of the word.')
    print('Whenever you want to start a new game with a new board, type N.')

def main():
    print_welcome()

    the_game = Game()
    the_board = make_board()
    print_board(the_board)

    while True: 
        text = input()
        if text == 'N':
            the_game = Game()
            the_board = make_board()
            print_board(the_board)
        else:
            feedback(the_game, the_board, text)
            print_board(the_board)

main()

# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

from ps4a import get_permutations


def load_words(file_name):
    """
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    return wordlist


def is_word(word_list, word):
    """
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|:;'<>?,./\"")
    return word in word_list


WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'


class SubMessage(object):
    def __init__(self, text):
        """
        Initializes a SubMessage object

        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        """
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        """
        Used to safely access self.message_text outside the class

        Returns: self.message_text
        """
        return self.message_text

    def get_valid_words(self):
        """
        Used to safely access a copy of self.valid_words outside the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        """
        return self.valid_words[:]

    def build_transpose_dict(self, vowels_permutation):
        """
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)

        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled
        according to vowels_permutation. The first letter in vowels_permutation
        corresponds to a second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        """
        transpose_dict = {}
        for x, letter in enumerate(vowels_permutation):
            transpose_dict[letter] = VOWELS_LOWER[x]
            transpose_dict[letter.upper()] = VOWELS_UPPER[x]
        return transpose_dict

    def apply_transpose(self, transpose_dict):
        """
        transpose_dict (dict): a transpose dictionary

        Returns: an encrypted version of the message text, based
        on the dictionary
        """
        transpose_text = []
        for char in self.get_message_text():
            if char in transpose_dict.keys():
                transpose_text.append(transpose_dict[char])
            else:
                transpose_text.append(char)
        return ''.join(transpose_text)


class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        """
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        """
        super().__init__(text)

    def decrypt_message(self):
        """
        Attempt to decrypt the encrypted message

        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.

        If no good permutations are found (i.e. no permutations result in
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message

        Hint: use your function from Part 4A
        """
        permutations_list = get_permutations(VOWELS_LOWER)
        tested_permutations = {}
        for perm in permutations_list:
            test_dict = self.build_transpose_dict(perm)
            test_dict = {v: k for k, v in test_dict.items()}
            test_text = self.apply_transpose(test_dict)
            for word in test_text.split():
                if is_word(self.get_valid_words(), word) is True:
                    tested_permutations[test_text] = tested_permutations.get(test_text, 0) + 1
        return [k for k, v in tested_permutations.items() if v == max(tested_permutations.values())][0]


encryption_cases = [
    ("eaiuo", "Hello World!", "Hallu Wurld!"),
    ("aeiou", "Python is fun!", "Python is fun!"),
    ("ouaei", "Programming is cool", "Pragrimmung us caal"),
]


if __name__ == '__main__':
    print("\nStarting encryption tests: \n\n")

    for case in encryption_cases:
        msg = SubMessage(case[1])
        trans_dict = msg.build_transpose_dict(case[0])
        encryption = msg.apply_transpose(trans_dict)
        print("Original message:", msg.get_message_text(), "Permuation:", case[0])
        print("Expected:", case[2], "Actual:", encryption)
        print("Results:", case[2] == encryption)

    print("\nStarting decryption tests: \n\n")

    for decryption_case in encryption_cases:
        msg = EncryptedSubMessage(decryption_case[2])
        decryption = msg.decrypt_message()
        print("Original encrypted message:", msg.get_message_text())
        print("Expected:", decryption_case[1], "Actual:", decryption)
        print("Results:", decryption_case[1] == decryption)

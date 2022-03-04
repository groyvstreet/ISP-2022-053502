from text_analyzer import TextAnalyzer


class UserUI:

    def __init__(self):
        self.text_analyzer = TextAnalyzer()
        self.k = 10
        self.n = 4

    def request_input(self) -> None:
        """Asks for input text, k and n."""
        text = input('Enter text: ')
        if not text or text.isspace():
            print('Void string')
            exit()
        else:
            self.text_analyzer.text = text
        k = input('Enter k: ')
        n = input('Enter n: ')
        if k.isnumeric():
            self.k = int(k) if int(k) >= 1 else self.k
        if n.isnumeric():
            self.n = int(n) if int(n) >= 1 else self.n

    def print_words(self) -> None:
        """Displays the list of the words with amount of the repetitions."""
        word_dict = self.text_analyzer.get_word_dict(0)
        print('Words repetitions: ')
        for word in word_dict:
            print(word, word_dict[word])

    def print_average_number(self) -> None:
        """Displays average number of the words in the sentence."""
        average = self.text_analyzer.get_average_number()
        print('Average number of the words in the sentence - ', average)

    def print_median_number(self) -> None:
        """Displays the median number of the words in the sentence."""
        median = self.text_analyzer.get_median_number()
        print('Median number of the words in the sentence - ', median)

    def print_top_of_ngrams(self) -> None:
        """Displays the top-k of the ngrams with the repetitions."""
        sorted_ngram_dict = self.text_analyzer.get_ngram_dict(self.n)
        print('Top', self.k, 'of', self.n, '- grams:')
        counter = 0
        for key in sorted_ngram_dict.keys():
            print(key, sorted_ngram_dict[key])
            counter += 1
            if counter == self.k:
                break
        if counter == 0:
            print('Nothing')

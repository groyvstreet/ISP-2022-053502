from text_analyzer import TextAnalyzer


class UserUI:

    def __init__(self):
        self.text_analyzer = TextAnalyzer()
        self.k = 10
        self.n = 4

    def request_input(self) -> None:
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
        word_dict = self.text_analyzer.get_word_dict(0)
        print('Word repetitions: ')
        for word in word_dict:
            print(word, word_dict[word])

    def print_average_number(self) -> None:
        average = self.text_analyzer.get_average_number()
        print('Average number of words in a sentence - ', average)

    def print_median_number(self) -> None:
        median = self.text_analyzer.get_median_number()
        print('Median number of words in a sentence - ', median)

    def print_top_of_ngrams(self) -> None:
        sorted_ngram_dict = self.text_analyzer.get_top_of_ngrams(self.n)
        print('Top', self.k, 'of', self.n, '- grams:')
        counter = 0
        for key in sorted_ngram_dict.keys():
            print(key, sorted_ngram_dict[key])
            counter += 1
            if counter == self.k:
                break
        if counter == 0:
            print('Nothing')

import typing


class TextAnalyzer:

    def __init__(self):
        self.text = ''

    @staticmethod
    def _get_word_dict(text, start) -> typing.Dict[str, int]:
        """Returns the dictionary of the words with amount of the repetitions in the text."""
        text = text.lower()
        for i in range(0x21, 0x2d):
            text = text.replace(chr(i), ' ')
        for i in range(0x2e, 0x41):
            text = text.replace(chr(i), ' ')
        for i in range(0x5b, 0x61):
            text = text.replace(chr(i), ' ')
        for i in range(0x7b, 0x7f):
            text = text.replace(chr(i), ' ')
        text = text.replace('-', '')
        word_list = text.split()
        word_dict = {}
        for word in word_list:
            if word in word_dict.keys():
                word_dict[word] += 1
            else:
                word_dict[word] = start
        return word_dict

    def get_word_dict(self, start) -> typing.Dict[str, int]:
        """Returns the dictionary of the words with amount of the repetitions."""
        return self._get_word_dict(self.text, start)

    def get_sent_list(self) -> typing.List[typing.Dict[str, int]]:
        """Returns the list of the sentences - dictionaries of the words with amount of the repetitions."""
        text = self.text
        sent_list = []
        temp = ''
        for i in range(0, len(text)):
            temp += text[i]
            if text[i] == '.' or text[i] == '!' or text[i] == '?' or i == len(text) - 1:
                sent_list.append(temp)
                temp = ''
        sent_list2 = []
        for i in sent_list:
            temp = self._get_word_dict(i, 1)
            if temp:
                sent_list2.append(temp)
        return sent_list2

    def get_average_number(self) -> float:
        """Returns the average number of the words in the sentence."""
        sent_list = self.get_sent_list()
        average = 0
        for sent in sent_list:
            for value in sent.values():
                average += value
        return average / len(sent_list)

    def get_median_number(self) -> float:
        """Returns the median number of the words in the sentence."""
        sent_list = self.get_sent_list()
        temp = 0
        value_list = []
        for sent in sent_list:
            for value in sent.values():
                temp += value
            value_list.append(temp)
            temp = 0
        value_list.sort()
        index = len(value_list)
        if index % 2 == 0:
            index //= 2
            return (value_list[index] + value_list[index - 1]) / 2
        else:
            index = (index - 1) // 2
            return value_list[index]

    def get_ngram_dict(self, n) -> typing.Dict[str, int]:
        """Returns the sorted dictionary of the ngrams with amount of the repetitions by the value."""
        word_dict = self.get_word_dict(1)
        ngram_dict = {}
        for word in word_dict:
            for i in range(0, len(word) - n + 1):
                temp = word[i:i + n]
                if temp in ngram_dict.keys():
                    ngram_dict[temp] += word_dict[word]
                else:
                    ngram_dict[temp] = word_dict[word]
        sorted_values = sorted(ngram_dict.values(), reverse=True)
        sorted_ngram_dict = {}
        for value in sorted_values:
            for key in ngram_dict.keys():
                if ngram_dict[key] == value:
                    sorted_ngram_dict[key] = ngram_dict[key]
        return sorted_ngram_dict

class TextAnalyzer:

    def __init__(self):
        self.text = ''

    @staticmethod
    def _get_word_dict(text, start):
        for i in range(0x21, 0x41):
            text = text.replace(chr(i), ' ')
        word_list = text.split()
        word_dict = {}
        for word in word_list:
            if word in word_dict.keys():
                word_dict[word] += 1
            else:
                word_dict[word] = start
        return word_dict

    def get_word_dict(self, start) -> dict:
        return self._get_word_dict(self.text, start)

    def get_sent_list(self) -> list:
        text = self.text
        sent_list = []
        temp = ''
        for i in range(0, len(text)):
            temp += text[i]
            if i == len(text) - 1 or (text[i] == '.' and (0x30 > ord(text[i + 1]) or ord(text[i + 1]) > 0x39)) or \
                    text[i] == '!' or text[i] == '?':
                sent_list.append(temp)
                temp = ''
        return [self._get_word_dict(i, 1) for i in sent_list]

    def get_average_number(self) -> float:
        sent_list = self.get_sent_list()
        average = 0
        for sent in sent_list:
            for value in sent.values():
                average += value
        return average / len(sent_list)

    def get_median_number(self) -> float:
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
            index /= 2
            return (value_list[index] + value_list[index - 1]) / 2
        else:
            index = (index - 1) // 2
            return value_list[index]

    def get_top_of_ngrams(self, n) -> dict:
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

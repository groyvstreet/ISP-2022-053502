def get_word_dict(text, start) -> dict:
    if not text or text.isspace():
        exit()
    for i in range(0x21, 0x42):
        text = text.replace(chr(i), '')
    word_list = text.split()
    word_dict = {}
    for word in word_list:
        if word in word_dict.keys():
            word_dict[word] += 1
        else:
            word_dict[word] = start
    return word_dict


def main(text) -> None:
    k = input('Enter k: ')
    n = input('Enter n: ')
    if not k.isnumeric():
        k = 10
    else:
        k = int(k)
    if not n.isnumeric():
        n = 4
    else:
        n = int(n)
    word_dict = get_word_dict(text, 0)
    for word in word_dict:
        print(word, word_dict[word])

    temp = ''
    sent_list = []
    for i in range(0, len(text)):
        temp += text[i]
        if (text[i] == '.' and (0x30 > ord(text[i + 1]) or ord(text[i + 1]) > 0x39)) or text[i] == '!' or \
                text[i] == '?' or i == len(text) - 1:
            sent_list.append(temp)
            temp = ''
    sent_list = [get_word_dict(i, 1) for i in sent_list]
    average = 0
    temp = 0
    value_list = []
    for sent in sent_list:
        for value in sent.values():
            average += value
            temp += value
        value_list.append(temp)
        temp = 0
    average /= len(sent_list)
    print('Average number of words in a sentence - ', average)

    value_list.sort()
    index = len(value_list)
    if index % 2 == 0:
        index /= 2
        median = (value_list[index] + value_list[index - 1]) / 2
    else:
        index = (index - 1) // 2
        median = value_list[index]
    print('Median number of words in a sentence - ', median)

    word_dict = get_word_dict(text, 1)
    ngram_dict = {}
    for word in word_dict:
        for i in range(0, len(word) - n + 1):
            temp = word[i:i+n]
            if temp in ngram_dict.keys():
                ngram_dict[temp] += word_dict[word]
            else:
                ngram_dict[temp] = word_dict[word]
    for key in ngram_dict:
        print(key, ngram_dict[key])
    sorted_values = sorted(ngram_dict.values(), reverse=True)
    sorted_ngram_dict = {}
    for value in sorted_values:
        for key in ngram_dict.keys():
            if ngram_dict[key] == value:
                sorted_ngram_dict[key] = ngram_dict[key]
    print('Top', k, 'of', n, '- grams:')
    counter = 0
    for key in sorted_ngram_dict.keys():
        print(key, sorted_ngram_dict[key])
        counter += 1
        if counter == k:
            break
    if counter == 0:
        print('Nothing')


if __name__ == '__main__':
    main('So, i want to say, that tomorrow we will get a patch 8.31. aaa aaa aaatch aaa aaa! ddd d ddd bbb ddd ddd dd dd?')
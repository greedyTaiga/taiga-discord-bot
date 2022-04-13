import re
import string

from config import MAX_MESSAGE_LENGTH

def remove_brackets(s):
    return re.sub("[\(\[].*?[\)\]]", "", s)


def remove_entities(text):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

#divides the message given in a list of lines to multiple chunks to fit the maximum message length limit
def divide_to_chunks(lines):
    chunks = list()
    chunk = ""
    for line in lines:
        if len(chunk) + len(line) < MAX_MESSAGE_LENGTH:
            chunk = chunk + line + "\n"
        else:
            chunks.append(chunk)
            chunk = ""
    if chunk != "":
        chunks.append(chunk)
    return chunks

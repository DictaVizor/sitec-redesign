def chunks(list, n):
    for i in range(0, len(list), n):
        yield list[i:i + n]

def clean_spanish_characters(string):
    return string.replace('\ufffd', 'ñ')
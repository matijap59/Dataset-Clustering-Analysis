


def process_text_data(data):          # stop words are not removed

    import re
    word_pattern = re.compile(r'\b\w+\b')           ## This simplification was kept for now, but handling such variations (e.g., through stemming or lemmatization) could be a useful improvement in future versions of the algorithm.

    for id, info in data.items():
        words = word_pattern.findall(info["concat"].lower())  # convert to lowercase + extract only words
        data[id]["tokens"] = words  # store as a list under a new key "tokens"
        del data[id]["concat"]

    return data
from bs4 import BeautifulSoup
from collections import Counter
from nltk import PorterStemmer
from nltk.corpus import stopwords
import re
from nltk.util import ngrams


def tag_visible(element) -> bool:
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    return True


def get_ngrams(words: list, n: int) -> list:
    n_grams = ngrams(words, n)
    return [' '.join(grams) for grams in n_grams]


def counts(words: list) -> dict:
    # Create a PorterStemmer object
    stemmer = PorterStemmer()

    # Use the PorterStemmer to stem each word, excluding stopwords
    stop_words = set(stopwords.words('english'))

    # Map a stem word with a normal word (randomly)
    stemmed_normal_index = {stemmer.stem(word): word for word in words if word not in stop_words}

    # Exclude english stop words and words with length <=2
    stemmed_words = [stemmed_normal_index[stemmer.stem(word)] for word in words if word not in stop_words and len(word) > 2]

    # Count the frequency of each stemmed word
    word_counts = Counter(stemmed_words)

    # Find most frequent words
    most_common_words = word_counts.most_common(20)

    # Create a list of bigrams and count their frequency
    bigrams = get_ngrams(stemmed_words, 2)
    bigram_counts = Counter(bigrams)

    # Find most frequent bigrams
    most_common_bigrams = bigram_counts.most_common(10)

    # Create a list of trigrams and count their frequency
    trigrams = get_ngrams(stemmed_words, 3)
    trigram_counts = Counter(trigrams)

    # Find most frequent trigrams
    most_common_trigrams = trigram_counts.most_common(5)

    return {"words": stemmed_words, "word_counts": word_counts, "most_common_words": most_common_words,
            "bigrams": bigrams, "bigram_counts": bigram_counts, "most_common_bigrams": most_common_bigrams,
            "trigrams": bigrams, "trigram_counts": bigram_counts, "most_common_trigrams": most_common_trigrams,
            "words_num_all": len(words), "words_num": len(stemmed_words)
            }


def page_analyzer(soup) -> dict:
    # Parse the HTML content using BeautifulSoup
    h1 = soup.find('h1').text.strip()
    h2 = soup.find(['h2', 'h3']).text.strip()

    # Find all text content in the HTML document
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    text = u" ".join(t.strip() for t in visible_texts)

    # Split the text content into words
    words = re.findall('\w+', text.lower())

    counters = counts(words)

    rs = {"h1": h1, "h2": h2}

    return {**counters, **rs}


def safe_div(x: int, y: int) -> float:
    try:
        return x / y
    except ZeroDivisionError:
        return 0


def counter_to_text(lst: list) -> str:
    return ", ".join([f"{x[0]}({x[1]})" for x in lst])


def stats_to_text(stats: dict, other_stats: dict) -> str:
    return f"""
        <b>Heading 1</b>: {stats["h1"]}<br>
        <b>Heading 2</b>: {stats["h2"]}<br>
        <br>
        <b>Published At</b>: {str(other_stats["published_at"]["date"])} {other_stats["published_at"]["time_period"]}<br>
        <b>Claps per Person</b>: {round(safe_div(other_stats["clap_count"], other_stats["voter_count"]), 1)} ({other_stats["voter_count"]} / {other_stats["clap_count"]})<br>
        <b>Responses</b>: {other_stats["post_responses"]}<br>
        <br>
        <b>Word Count (Stemmed)</b>: {stats["words_num"]}<br>
        <b>Most Common Words</b>:<br> {counter_to_text(stats["most_common_words"])}<br><br>
        <b>Most Common Bigrams</b>:<br> {counter_to_text(stats["most_common_bigrams"])}<br><br>
        <b>Most Common Trigrams</b>:<br> {counter_to_text(stats["most_common_trigrams"])}<br><br>
        """


def profile_to_text(data: dict, aggregated_stats: dict, other_profile_stats: dict) -> str:
    publication_count = Counter(other_profile_stats['publication']).most_common(10)
    published_time_period_count = Counter([f"{x['time_period'][0]}-{x['time_period'][1]}" for x in other_profile_stats["published_at"]]).most_common(10)
    followers = data["user"]["info"]["followers_count"]
    return f"""
        <b>Articles</b>: {len(data["articles"])} ({len(aggregated_stats["words"])} words) <br>
        <b>Publications</b>: {counter_to_text(publication_count)} <br>
        <b>Followers</b>: {followers} <br>
        <b>Voters / Followers</b>: {round(safe_div(other_profile_stats["voter_count"], followers) * 100, 1)}% ({other_profile_stats["voter_count"]} / {followers})<br>
        <b>Claps per Person</b>: {round(safe_div(other_profile_stats["clap_count"], other_profile_stats["voter_count"]), 1)} ({other_profile_stats["clap_count"]} / {other_profile_stats["voter_count"]})<br>
        <b>Preferred Published Time</b>: {counter_to_text(published_time_period_count)} <br>

        <br>
        <b>Most Common Words</b>:<br> {", ".join([f"{x[0]}({x[1]})" for x in aggregated_stats["most_common_words"]])}<br><br>
        <b>Most Common Bigrams</b>:<br> {", ".join([f"{x[0]}({x[1]})" for x in aggregated_stats["most_common_bigrams"]])}<br><br>
        <b>Most Common Trigrams</b>:<br> {", ".join([f"{x[0]}({x[1]})" for x in aggregated_stats["most_common_trigrams"]])}<br><br>
        """

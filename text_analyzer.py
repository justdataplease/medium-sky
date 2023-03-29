import re
from collections import Counter
import datetime
from urllib.parse import urlparse
from excluded_urls import EXCLUDE_URLS

from nltk import PorterStemmer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.util import ngrams
import validators


def tag_visible(element) -> bool:
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    return True


def get_ngrams(words: list, n: int) -> list:
    n_grams = ngrams(words, n)
    return [' '.join(grams) for grams in n_grams]


def pos_tagger(words: list) -> dict:
    # Part-of-speech tag each token
    pos_tags = pos_tag(words)

    # Count the number of adjectives, nouns, and verbs
    num_adjectives = len([word for word, pos in pos_tags if pos in ['JJ', 'JJR', 'JJS']])
    num_nouns = len([word for word, pos in pos_tags if pos in ['NN', 'NNS', 'NNP', 'NNPS']])
    num_verbs = len([word for word, pos in pos_tags if pos in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']])

    return {"adj": num_adjectives, "noun": num_nouns, "verb": num_verbs}


def text_stemmer(words: list) -> dict:
    stemmer = PorterStemmer()

    # Use the PorterStemmer to stem each word, excluding stopwords
    stop_words = set(stopwords.words('english'))

    # Map a stem word with a normal word (randomly)
    stemmed_normal_index = {stemmer.stem(word): word for word in words if word not in stop_words}

    # Exclude english stop words and words with length <=2
    stemmed_words = [stemmed_normal_index[stemmer.stem(word)] for word in words if word not in stop_words and len(word) > 2]
    return stemmed_words


def count_external_domains(articles: dict) -> int:
    """
    To calculate external domains for each profile we create a list with the unique external domains for each article, for all articles
    """
    domains = []
    for links_per_article in articles:
        domains_per_article = []
        for link in links_per_article["links"]:
            href = link[1]
            if validators.url(href) and not re.search(EXCLUDE_URLS + "|medium", href):
                domains_per_article.append(urlparse(href).netloc)
        domains.extend(list(set(domains_per_article)))
    return len(domains)


def counts(words: list, include_stemming=True) -> dict:
    """
    Calculates article statistics : most common words, most common bigrams/trigrams etc
    """
    if include_stemming:
        # Create a PorterStemmer object
        stemmed_words = text_stemmer(words)
    else:
        stemmed_words = words

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

    # Get article type
    if len(stemmed_words) < 100:
        words_num_cat = "short"
    elif len(stemmed_words) < 500:
        words_num_cat = "normal"
    elif len(stemmed_words) < 1000:
        words_num_cat = "medium"
    elif len(stemmed_words) < 1800:
        words_num_cat = "large"
    elif len(stemmed_words) > 1800:
        words_num_cat = "very large"

    return {"words": stemmed_words, "words_all": words, "word_counts": word_counts, "most_common_words": most_common_words,
            "bigrams": bigrams, "bigram_counts": bigram_counts, "most_common_bigrams": most_common_bigrams,
            "trigrams": bigrams, "trigram_counts": bigram_counts, "most_common_trigrams": most_common_trigrams,
            "words_num_all": len(words), "words_num": len(stemmed_words), "words_num_cat": words_num_cat,
            "unique_words_num_all": len(list(set(words))), "unique_words_num": len(list(set(stemmed_words))),
            }


def page_analyzer(soup) -> dict:
    # Parse the HTML content using BeautifulSoup
    try:
        h1 = soup.find('h1').text.strip()
    except Exception as exc:
        print("no h1 found...")
        h1 = ""

    try:
        h2 = soup.find(['h2', 'h3', 'h4']).text.strip()
    except Exception as exc:
        print("no h2 found...")
        h2 = ""

    # Find all text content in the HTML document
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    text = u" ".join(t.strip() for t in visible_texts)

    # Split the text content into words
    words = re.findall('\w+', text.lower())

    pos_tags = pos_tagger(words)
    counters = counts(words)

    rs = {"h1": h1, "h2": h2}

    return {**counters, **rs, **pos_tags}


def safe_div(x: int, y: int) -> float:
    try:
        return x / y
    except ZeroDivisionError:
        return 0


def counter_to_text(lst: list) -> str:
    return ", ".join([f"{x[0]}({x[1]})" for x in lst])


def find_list_div_avg(list1, list2):
    total = 0
    for i in range(len(list1)):
        total += safe_div(list1[i], list2[i])

    average = total / len(list1)
    return average


def find_dates_frequency(dates: list) -> float:
    # Sort the list of dates in ascending order
    dates.sort()

    # Calculate the frequency of each interval
    freq = []
    for i in range(len(dates) - 1):
        interval = dates[i + 1] - dates[i]
        freq.append(interval.days)

    # Calculate the average frequency
    avg_freq = sum(freq) / len(freq)
    min_date = str(max(dates))
    max_date = str(min(dates))

    return avg_freq, max_date, min_date


def days_between(d1: datetime, d2: datetime = None) -> int:
    if d2 is None:
        d2 = datetime.date.today()
    else:
        d2 = datetime.datetime.strptime(d2, "%Y-%m-%d").date()
    return abs((d2 - d1).days)


def stats_to_text(article_stats: dict, article_chars: dict, user_chars: dict) -> str:
    claps_per_person = safe_div(article_chars["clap_count"], article_chars["voter_count"])
    voter_follower = safe_div(article_chars["voter_count"], user_chars["info"]["followers_count"])

    return f"""
        <b>Heading 1</b>: {article_stats["h1"]}<br>
        <b>Heading 2</b>: {article_stats["h2"]}<br>
        <br>
        <b>Publication</b>: <a href='{article_chars["publisher_url"]}'>{article_chars["publisher_name"]}</a> <br>
        <b>Published At</b>: {str(article_chars["published_at"]["date"])} {article_chars["published_at"]["time_period"]}<br>
        <b>Voters - Followers %</b>: {round(voter_follower * 100, 1)}%<br>
        <b>Claps per Person</b>: {round(claps_per_person, 1)} ({article_chars["voter_count"]} / {article_chars["clap_count"]})<br>
        <b>Responses</b>: {article_chars["post_responses"]}<br>
        <br>
        <b>Word Count (All)</b>: {article_stats["words_num_all"]}<br>
        <b>Word Count (Stemmed)</b>: {article_stats["words_num"]} ({article_stats["words_num_cat"]})<br>
        <b>Stemmed words / words</b>: {round(safe_div(article_stats["words_num"], article_stats["words_num_all"]) * 100, 1)}% ({article_stats["words_num"]} / {article_stats["words_num_all"]})<br>
        <b>Unique words / words</b>: {round(safe_div(article_stats["unique_words_num_all"], article_stats["words_num_all"]) * 100, 1)}% ({article_stats["unique_words_num_all"]} / {article_stats["words_num_all"]})<br>
        <b>Unique words / words (stemmed)</b>: {round(safe_div(article_stats["unique_words_num"], article_stats["words_num_all"]) * 100, 1)}% ({article_stats["unique_words_num_all"]} / {article_stats["words_num_all"]})<br>
        <b>Verb / words</b>: {round(safe_div(article_stats["verb"], article_stats["words_num_all"]) * 100, 1)}% ({article_stats["verb"]} / {article_stats["words_num_all"]})<br>
        <b>Adj / words</b>: {round(safe_div(article_stats["adj"], article_stats["words_num_all"]) * 100, 1)}% ({article_stats["adj"]} / {article_stats["words_num_all"]})<br>
        <b>Noun / words</b>: {round(safe_div(article_stats["noun"], article_stats["words_num_all"]) * 100, 1)}% ({article_stats["noun"]} / {article_stats["words_num_all"]})<br>

        <br>
        <b>Most Common Words</b>:<br> {counter_to_text(article_stats["most_common_words"])}<br><br>
        <b>Most Common Bigrams</b>:<br> {counter_to_text(article_stats["most_common_bigrams"])}<br><br>
        <b>Most Common Trigrams</b>:<br> {counter_to_text(article_stats["most_common_trigrams"])}<br><br>
        """


def profile_to_text(all_data: dict, profile_stats: dict, other_profile_stats: dict) -> str:
    domains_number = count_external_domains(all_data["articles"])
    article_length_cat = Counter(other_profile_stats['article_length_cat']).most_common(3)
    publication_count = Counter(other_profile_stats['publication']).most_common(10)
    published_frequency = find_dates_frequency([x['date'] for x in other_profile_stats["published_at"]])
    published_time_period_count = Counter([f"{x['time_period'][0]}-{x['time_period'][1]}" for x in other_profile_stats["published_at"]]).most_common(10)
    followers = all_data["user"]["info"]["followers_count"]

    words_all_num = len(other_profile_stats["user_words_all"])
    unique_words_all_num = len(set(other_profile_stats["user_words_all"]))
    words_num = len(other_profile_stats["user_words"])
    unique_words_num = len(set(other_profile_stats["user_words"]))

    clap_voter_avg = find_list_div_avg(other_profile_stats["clap_count"], other_profile_stats["voter_count"])
    voter_follower_avg = find_list_div_avg(other_profile_stats["voter_count"], [followers] * len(other_profile_stats["voter_count"]))

    pos_stats = other_profile_stats["pos_stats"]

    last_date_seen = max([x["date"] for x in other_profile_stats["published_at"]])
    bio = all_data["user"]["info"]["bio"]

    return f"""
        <b>BIO</b>: {bio} <br>

        <b>Articles</b>: {len(all_data["articles"])} ({len(profile_stats["words"])} stemmed words) <br>
        <b>Top article</b>: <a href='{other_profile_stats["top_article"][0]}'>{other_profile_stats["top_article"][1]} ({other_profile_stats["top_article"][2]})</a> <br>

        <b>Publications</b>: {counter_to_text(publication_count)} <br>
        <b>Followers</b>: {followers} <br>
        
        <b>Voters - Followers % (Article AVG)</b>: {round(voter_follower_avg * 100, 1)}%<br>
        <b>Claps per Person (Article AVG)</b>: {round(clap_voter_avg, 1)}<br>
        <br>
        
        <b>Preferred Published Time</b>: {counter_to_text(published_time_period_count)} <br>
        <b>Preferred Article Length (stemmed)</b>: {counter_to_text(article_length_cat)} <br>
        <b>Published Frequency (AVG)</b>: per {round(published_frequency[0], 1)} days ({published_frequency[1]}/{published_frequency[2]}) <br>
        <b>Last Seen </b>: before {days_between(last_date_seen)} days<br>

        <b>External Domains per Article </b>: {round(safe_div(domains_number, len(all_data["articles"])), 1)}<br>

        <br>
        <b>Stemmed words / words</b>: {round(safe_div(words_num, words_all_num) * 100, 1)}% ({words_num} / {words_all_num})<br>
        <b>Unique words / words</b>: {round(safe_div(unique_words_all_num, words_all_num) * 100, 1)}% ({unique_words_all_num} / {words_all_num})<br>
        <b>Unique words / words (stemmed)</b>: {round(safe_div(unique_words_num, words_num) * 100, 1)}% ({unique_words_num} / {words_num})<br>
        <b>Verb / words</b>: {round(safe_div(pos_stats["verb"], words_all_num) * 100, 1)}% ({pos_stats["verb"]} / {words_all_num})<br>
        <b>Adj / words</b>: {round(safe_div(pos_stats["adj"], words_all_num) * 100, 1)}% ({pos_stats["adj"]} / {words_all_num})<br>
        <b>Noun / words</b>: {round(safe_div(pos_stats["noun"], words_all_num) * 100, 1)}% ({pos_stats["noun"]} / {words_all_num})<br>
        <br>


        <br>
        <b>Most Common Words</b>:<br> {counter_to_text(profile_stats["most_common_words"])}<br><br>
        <b>Most Common Bigrams</b>:<br> {counter_to_text(profile_stats["most_common_bigrams"])}<br><br>
        <b>Most Common Trigrams</b>:<br> {counter_to_text(profile_stats["most_common_trigrams"])}<br><br>
        """

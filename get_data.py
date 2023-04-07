import requests
import bs4
from text_analyzer import page_analyzer, stats_to_text, counts, profile_to_text, pos_tagger, chatgpt_parser
import re
import markdown
import backoff
import pickle
from dotenv import load_dotenv
import os
from subprocess import check_output
import json
import validators
from datetime import datetime
import os

# load environment variables from .env file
load_dotenv()

INLINE_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
FOOTNOTE_LINK_TEXT_RE = re.compile(r'\[([^\]]+)\]\[(\d+)\]')
FOOTNOTE_LINK_URL_RE = re.compile(r'\[(\d+)\]:\s+(\S+)')

API_URL = "https://medium2.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": os.environ.get('RAPID_API'),
    "X-RapidAPI-Host": "medium2.p.rapidapi.com"
}


def get_ld_json(soup) -> dict:
    return json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))


def safe_div(x: int, y: int) -> float:
    try:
        return x / y
    except ZeroDivisionError:
        return 0


def get_timestamp(timestamp):
    if not timestamp:
        return {"date": None, "time": None, "time_period": None, "day_of_week": None}

    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    parsed_date = datetime.strptime(timestamp, date_format)
    date = parsed_date.date()
    time = parsed_date.time()

    if time.hour < 5:
        time_period = ("night", "early")
    elif time.hour < 8:
        time_period = ("night", "late")
    elif time.hour < 12:
        time_period = ("morning", "morning")
    elif time.hour < 15:
        time_period = ("afternoon", "early")
    elif time.hour < 18:
        time_period = ("afternoon", "late")
    elif time.hour < 21:
        time_period = ("evening", "early")
    else:
        time_period = ("evening", "late")

    return {"date": date, "time": time, "time_period": time_period}


def find_md_links(md: str) -> list:
    """ Return dict of links in markdown """
    links = []
    try:
        links = list(INLINE_LINK_RE.findall(md))
        footnote_links = dict(FOOTNOTE_LINK_TEXT_RE.findall(md))
        footnote_urls = dict(FOOTNOTE_LINK_URL_RE.findall(md))

        for key in footnote_links.keys():
            links.append((footnote_links[key], footnote_urls[footnote_links[key]]))
    except Exception as exc:
        print(f"ERROR: {exc}")

    return links


def load_js_state(soup, state: str = 'window.__PRELOADED_STATE__') -> dict:
    """
    Load JS state from a soup object
    """
    s = [x for x in soup.find_all('script') if state in str(x)][0]
    with open('temp.js', 'w', encoding="utf-8") as f:
        f.write('window = {};\n' +
                s.text.strip() +
                f';\nprocess.stdout.write(JSON.stringify({state}));')
    window_init_state = check_output(['node', 'temp.js'])
    os.remove('temp.js')
    rs = json.loads(window_init_state)
    return rs


def get_user_id_unofficial(user: str) -> dict:
    """
    Unofficial method to get user info
    """
    user_url = f"https://medium.com/@{user}"
    response = requests.get(user_url, headers=HEADERS)
    soup = bs4.BeautifulSoup(response.content, features="lxml")
    preload_state = load_js_state(soup, state='window.__PRELOADED_STATE__')
    user_id = preload_state['client']['routingEntity']['id']
    appolo_state = load_js_state(soup, state='window.__APOLLO_STATE__')
    social_stats = appolo_state[f'User:{user_id}']['socialStats']
    return {"user_id": user_id, "social_stats": social_stats}


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_tries=3,
                      jitter=None)
def get_article_stats(url: str) -> list:
    """
    Unofficial method to get article stats.
    """
    article_response = requests.get(url)
    soup = bs4.BeautifulSoup(article_response.content, features="lxml")

    ld = get_ld_json(soup)
    preload_state = load_js_state(soup, state='window.__APOLLO_STATE__')

    article_id = ld.get("identifier", "")
    post_stats = preload_state[f'Post:{article_id}']

    # Get info
    info = {
        "url": article_response.url,
        "clap_count": post_stats.get("clapCount", 0),
        "voter_count": post_stats.get("voterCount", 0),
        "post_responses": post_stats.get("postResponses", {}).get("count", 0),
        "created_at": get_timestamp(ld.get("dateCreated")),
        "published_at": get_timestamp(ld.get("datePublished")),
        "modified_at": get_timestamp(ld.get("dateModified")),
        "name": ld.get("name", ""),
        "identifier": ld.get("identifier", ""),
        "publisher_name": ld.get("publisher", {}).get("name", ""),
        "publisher_url": ld.get("publisher", {}).get("url", ""),
        "isAccessibleForFree": ld.get("isAccessibleForFree", True)
    }
    return info


def get_article_content_unofficial(url: str) -> list:
    """
    Unofficial method to get article markdown. Only works with articles without a paywall
    """
    rs = []
    article_response = requests.get(url)
    soup = bs4.BeautifulSoup(article_response.content, features="lxml")

    preload_state = load_js_state(soup, state='window.__APOLLO_STATE__')

    # iterate over each key in the __APOLLO_STATE__ object and extract the markups and text
    for k in preload_state.keys():
        markups = preload_state[k].get('markups', [])
        markups_text = preload_state[k].get('text')

        # iterate over each markup and extract the start, end, href, and text
        for markup in markups:
            if markup:
                start = markup.get('start')
                end = markup.get('end')
                href = markup.get("href")
                text = markups_text[start:end]
                if href:
                    if validators.url(href):
                        rs.append((text, href))

    return rs


def get_user_id(user: str) -> str:
    """
    Get user_id using Medium API
    """
    url = f"{API_URL}/user/id_for/{user}"
    response = requests.get(url, headers=HEADERS)
    user_id = response.json()["id"]
    return user_id


def get_user_info(user_id: str) -> dict:
    """
    Get user_info using Medium API
    """
    url = f"{API_URL}/user/{user_id}"
    response = requests.get(url, headers=HEADERS)
    return response.json()


def get_user_articles(user_id: str) -> list:
    """
    Get user article_ids using Medium API
    """
    url = f"{API_URL}/user/{user_id}/articles"
    response = requests.request("GET", url, headers=HEADERS)
    articles = response.json()['associated_articles']
    return articles


def get_article_markdown(article_id: str) -> str:
    """
    Get article markdown using Medium API
    """
    url = f"{API_URL}/article/{article_id}/markdown"
    response = requests.request("GET", url, headers=HEADERS)
    return response.json()["markdown"]


def get_article_content(article_id: str) -> dict:
    markdown_text = get_article_markdown(article_id)
    links = find_md_links(markdown_text)
    return {"links": links, "markdown_text": markdown_text}


class MediumArticles:
    def __init__(self, username: str, articles_limit: int = 0, reset: bool = False, fixed_last_date=False, use_gpt=False):
        self.username = username
        self.fixed_last_date = fixed_last_date
        self.use_gpt = use_gpt
        self.user_words = []
        self.user_words_all = []
        self.articles_limit = articles_limit
        self.reset = reset
        self.clap_count = []
        self.voter_count = []
        self.clap_voter_count = []
        self.publication = []
        self.published_at = []
        self.article_length_cat = []
        self.user_upa_words_all = []
        self.user_upa_words = []
        self.chatgpt_keywords = []

    def get_all_articles(self) -> dict:
        """
        Get all user's articles and analyze them.
        If pickle file with data exists use the file else use the API (except the case you specify reset=True).
        File has the following format <username>_<articles_limit>.
        If <articles_limit>=0 then download all articles.
        Articles are saved before any NLP analysis (page_analyzer()) so you can adjust page_analyzer() to your needs.
        """
        file_name = f'data/{self.username}_{self.articles_limit}.pickle'
        # If file exists, load data from file
        print(file_name)
        if os.path.exists(file_name) and not self.reset:
            print("using the local file...")
            with open(file_name, 'rb') as f:
                data_to_keep = pickle.load(f)
        # If file does not exist, use Medium API
        else:
            print("using the api...")
            # Get user info
            user_id = get_user_id(self.username)
            user_info = get_user_info(user_id)
            article_ids = get_user_articles(user_id)

            # Parse articles
            data_to_keep = dict()
            data_to_keep["user"] = {"id": user_id, "info": user_info}
            data_to_keep["articles"] = []

            main_counter = 1
            for article_id in article_ids:
                print(f"getting article {article_id}...")
                article_content = get_article_content(article_id)
                article_stats = get_article_stats(f"https://{user_id}.medium.com/{article_id}")

                article_main = {
                    "id": article_id,
                    "links": article_content["links"],
                    "markdown": article_content["markdown_text"]
                }

                data_to_keep["articles"].append({**article_main, **article_stats})

                if self.articles_limit:
                    if main_counter >= self.articles_limit:
                        break
                main_counter += 1

            with open(file_name, 'wb') as f:
                pickle.dump(data_to_keep, f)

        # Generate keywords and summary using ChatGPT
        for article_content in data_to_keep["articles"]:
            if self.use_gpt:
                html = markdown.markdown(article_content["markdown"])
                soup = bs4.BeautifulSoup(html, features="lxml")
                article_content["chatgpt"] = chatgpt_parser(article_id=article_content["id"], soup=soup, username=self.username)
            else:
                article_content["chatgpt"] = {"keywords": [], "summary": "", "unikeywords": []}

        # Analyze articles
        most_voters = 0
        for article_content in data_to_keep["articles"]:
            html = markdown.markdown(article_content["markdown"])
            soup = bs4.BeautifulSoup(html, features="lxml")
            stats = page_analyzer(soup)
            article_content["stats_dict"] = stats
            article_content["stats"] = stats_to_text(article_stats=stats, article_chars=article_content, user_chars=data_to_keep["user"])

            self.user_words_all.extend(stats["words_all"])
            self.user_words.extend(stats["words"])

            self.user_upa_words_all.extend(list(set(stats["words_all"])))
            self.user_upa_words.extend(list(set(stats["words"])))

            self.clap_count.append(article_content["clap_count"])
            self.voter_count.append(article_content["voter_count"])
            self.article_length_cat.append(stats["words_num_cat"])
            self.publication.append(article_content["publisher_name"])
            self.published_at.append(article_content["published_at"])
            self.chatgpt_keywords.append(article_content["chatgpt"]["unikeywords"])

            # Find top article based on voters count (unique claps)
            if article_content["voter_count"] > most_voters:
                top_article = (article_content["url"], article_content["stats_dict"]["h1"], article_content["publisher_name"])
                most_voters = article_content["voter_count"]

        # Aggregate Statistics
        pos_stats = pos_tagger(self.user_words_all)

        # ChatGPT Most Common Words
        total_chatgpt_keywords = []
        for x in self.chatgpt_keywords:
            total_chatgpt_keywords.extend(x)
        chatgpt_words_count = counts(total_chatgpt_keywords)["most_common_words"]

        words_counts = counts(self.user_words, include_stemming=False)
        words_upa_counts = counts(self.user_upa_words, include_stemming=False)

        profile_stats = {
            "top_article": top_article,
            "user_words_all": self.user_words_all,
            "user_words": self.user_words,
            "user_upa_words_all": self.user_upa_words_all,
            "user_upa_words": self.user_upa_words,
            "clap_count": self.clap_count,
            "voter_count": self.voter_count,
            "publication": self.publication,
            "published_at": self.published_at,
            "article_length_cat": self.article_length_cat,
            "pos_stats": pos_stats,
            "chatgpt_words_count": chatgpt_words_count,
            "words_counts": words_counts,
            "words_upa_counts": words_upa_counts,
        }

        data_to_keep["user"]["profile"] = profile_to_text(all_data=data_to_keep, profile_stats=profile_stats, fixed_last_date=self.fixed_last_date)
        return data_to_keep

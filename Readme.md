[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![versions](https://img.shields.io/pypi/pyversions/pybadges.svg)

# Analyze your Medium.com articles with Knowledge Graphs and NLP with Medium-Sky

Medium-Sky is a simple open source Python-HTML app that allows you to explore a Medium.com user 
by analyzing the content of each article, as well as the relationship between the articles and
their referenced external website domains.

## Live Demo

Checkout [demo](https://justdataplease.com/db/medium-articles-analysis.html) (version 1)
or [demo](https://justdataplease.com/db/medium-articles-analysis-2.html) (version 2)

## How to Use

To use, you need to do the following actions:

1) You need to subscribe to medium.com api [rapidapi](https://rapidapi.com/nishujain199719-vgIfuFHZxVZ/api/medium2) (you
   get 150 requests per month for free - if you want to analyze all your articles, this app will work for free if you have less than 148 articles)
2) Copy paste .env_sample to .env and paste you X-RapidAPI-Key that you will
   find [here](https://rapidapi.com/nishujain199719-vgIfuFHZxVZ/api/medium2).
3) Install requirements <br>
   `pip install -r requirements.txt`
4) Run <br>
   `python kgraph -u=<username>` <br>
   <br>
   If you want to use just 10 of your most recent articles run: <br>
   `python kgraph -u=<username> -l=10` <br>
   <br>
   If you want to use an isolated knowledge graph (version 2 - Look Documentation), run: <br>
   `python kgraph -u=<username> -l=10 -i`
6) Find the generated HTML in output folder
   <username>_<number_of_articles>_m.html (mixed or version 1)
   <username>_<number_of_articles>_i.html (-i : isolated or version 2)

## Metrics Documentation

### Network Graph

A network graph is a diagram that shows how different elements (nodes) are related to each other by using lines (edges).
In this network graph, we have two types of nodes and one type of edge:

- Star (node) : This represents the main article. The larger the star, the greater the number of voters the article had. Voters are defined as unique users that clapped or unique claps.
- Dot or Circle (node) : This represents the external website domain. The larger the dot, the more frequently this domain appeared. Next to domain name there is a number that shows how many times this domain appeared.
- Edge (link) - These are the bidirectional links between the stars and dots.

This app provides 2 versions of Network Graphs:
1. Isolated (with the -i argument): This version focuses on the connections between main articles. It also allows us to inspect the external website domains that are referenced in each article. The same external website domain may appear multiple times in different articles. 
2. Mixed (without the -i argument): This version shows the connections between both main articles and external website domains. Each external website domain appears only once, allowing us to see the most frequently used domains and how they are connected to all the articles.

### Profile Section

The Profile section, is the area on the right navigation bar that shows user metrics. This is visible when the app is first opened.

- **Articles [Number]** : Number of articles that were used for the analysis (not the total number of articles of a user). Next to articles, there is also the total numbers of words.
  To find the total number of words we exclude english stopwords (based on [NTLK](https://www.nltk.org/) package) and words less than 3 characters. 
- **Top article [String]** : Top article is the article with the maximum number of Voters. Voters are defined as unique users that clapped or unique claps.
- **Publications [List]** : This is a frequency list of the articles based on their publication. If there is no publication the name 'Medium' is used. The format is \<publication\> \(\<articles published\>\)
- **Voters - Followers % (Article AVG) [Number]** : This is the average of the Voters / Followers per article. For an article, Voters are defined as unique users that clapped or unique claps. Followers is the actual number of followers at a specific time.
- **Claps per Person (Article AVG) [Number]** : This is the average of Claps / Voters per article. For an article, Voters are defined as unique users that clapped or unique claps.
- **Preferred Published Time [List]** : This is a frequency list of the preferred publishing time period. This refers to a time period (24h time cluster) inside a day, using the following rules
    [00:00 and 05:00) : "night", "early" <br>
    [05:00 and 08:00) : "night", "late" <br>
    [08:00 and 12:00) : "morning", "morning" <br>
    [12:00 and 15:00) : "afternoon", "early" <br>
    [15:00 and 18:00) : "afternoon", "late" <br>
    [18:00 and 21:00) : "evening", "early" <br>
    [21:00 and 00:00) : "evening", "late" <br>
- **Preferred Article Length (stemmed) [Number]** : This is a frequency list of the article words length. To find the total number of words we exclude english stopwords (based on NTLK package) and words less than 3 characters. This is a cluster that is calculated using the total number of words as follows:
    words < 100 : "very short" <br>
    words < 300 : "short" <br>
    words < 500 : "normal" <br>
    words < 1800 : "large" <br>
    words > 1800 : "very large" <br>

- **Published Frequency (AVG) [Number]** : This is the average of the difference in days, between the published dates of 2 consecutive articles. Next to this metric there is also the start date and the end date of the analysis.
- **Last Seen [Number]** : This the difference in days, between today and the maximum published date.
- **External Domains per Article [Number]** : For each article we calculate the number of unique domains (unique per article) that are referenced in it. Then, we find external domains for the user by summing up external domains per article. Finally, we divide external domains for the user with the number of the articles (not total articles of the user). 
- **Stemmed words / words [Number]** : This refers to the number of words if we exclude english stop words and words with less than 3 characters. Then we divide with the total number of words.
- **Unique words / words [Number]** : This refers to the unique number of words divided by the total number of words.
- **Unique words / words (stemmed) [Number]** : This refers to the unique number of words, after using Porter Stemming, if we exclude english stopwords and words with less than 3 characters, divided by the number of words if we exclude english stopwords and words with less than 3 characters.
- **Verb / words [Number]** : Using NLTK pos_tagger, this the percentage of (recognised) verbs in the text.
- **Adj / words [Number]** : Using NLTK pos_tagger, this the percentage of (recognised) adjectives in the text.
- **Noun / words [Number]** : Using NLTK pos_tagger, this the percentage of (recognised) nouns in the text.
- **Most Common Words [List]** : This is a frequency list of the most common words after using Porter Stemming (as a representation of stemmed words we used a random original word of the stemmed version.)
- **Most Common Bigrams [List]** : This is a frequency list of the most common bigrams after using Porter Stemming (as a representation of stemmed words we used a random original word of the stemmed version.)
- **Most Common Trigrams [List]** : This is a frequency list of the most common trigrams after using Porter Stemming (as a representation of stemmed words we used a random original word of the stemmed version.)
- **Most Common Words (UPA) [List]** : Look at Most Common Words. UPA stands for Unique Per Article. This means that if a word is mentioned more than once in an article it will not count. The maximum frequency equals to the number of articles of the analysis.
- **Most Common Bigrams (UPA) [List]** : Look at Most Common Bigrams. UPA stands for Unique Per Article. This means that if a word is mentioned more than once in an article it will not count. The maximum frequency equals to the number of articles of the analysis.
- **Most Common Trigrams (UPA) [List]** : Look at Most Common Trigrams. UPA stands for Unique Per Article. This means that if a word is mentioned more than once in an article it will not count. The maximum frequency equals to the number of articles of the analysis.


### Article Section

The Article section, is the area on the right navigation bar that shows article or external website domain metrics. This is visible when a node is clicked.

- **Published At [Date]** : Published Date and publishing time period.
- **Voters - Followers % [Number]** : Voters / Followers, where Voters are defined as unique users that clapped or unique claps and Followers the number of user followers at a specific time.
- **Claps per Person [Number]** : Claps / Voters, where Voters are defined as unique users that clapped or unique claps.
- **Responses [Number]** : The number of post comments.
- **Word Count (All) [Number]** : This refers to the number of words.
- **Word Count (Stemmed) [Number]** : This refers to the number of words, if we exclude english stopwords and words with less than 3 characters.
- **Stemmed words / words [Number]** : This refers to the number of words if we exclude english stop words and words with less than 3 characters. Then, we divide with the total number of words.
- **Unique words / words [Number]** : This refers to the unique number of words divided by the total number of words.
- **Unique words / words (stemmed) [Number]** : This refers to the unique number of words, after using Porter Stemming, if we exclude english stopwords and words with less than 3 characters, divided by the number of words if we exclude english stopwords and words with less than 3 characters.
- **Verb / words [Number]** : Using NLTK pos_tagger, this the percentage of (recognised) verbs in the text.
- **Adj / words [Number]** : Using NLTK pos_tagger, this the percentage of (recognised) adjectives in the text.
- **Noun / words [Number]** : Using NLTK pos_tagger, this the percentage of (recognised) nouns in the text.
- **Most Common Words [List]** : This is a frequency list of the most common words after using Porter Stemming (as a representation of stemmed words we used a random original word of the stemmed version.)
- **Most Common Bigrams [List]** : This is a frequency list of the most common bigrams after using Porter Stemming (as a representation of stemmed words we used a random original word of the stemmed version.)
- **Most Common Trigrams [List]** : This is a frequency list of the most common trigrams after using Porter Stemming (as a representation of stemmed words we used a random original word of the stemmed version.)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

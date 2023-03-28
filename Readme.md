[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![versions](https://img.shields.io/pypi/pyversions/pybadges.svg)

# Analyze your Medium.com articles with Knowledge Graphs and NLP with Medium-Sky

Medium-Sky is an Open Source Python-HTML app that allows you to explore a Medium.com profile by analyzing the content of each article, as well as the relationship between the articles and
their referenced external website domains.

## Live Demo

Checkout [demo](https://justdataplease.com/db/medium-articles-analysis.html) (version 1)
or [demo](https://justdataplease.com/db/medium-articles-analysis-2.html) (version 2)

## How to Use

To use, you need to do the following actions:

1) You need to subscribe to medium.com api [rapidapi](https://rapidapi.com/nishujain199719-vgIfuFHZxVZ/api/medium2) (you
   get 150 requests per month for free - this app will work for free if you have less than 148 articles)
2) Copy paste .env_sample to .env and paste you X-RapidAPI-Key that you will
   find [here](https://rapidapi.com/nishujain199719-vgIfuFHZxVZ/api/medium2).
3) Install requirements <br>
   `pip install -r requirements.txt`
4) Run <br>
   `python kgraph -u=<username>`
   If you want to use a specific number of articles (10 most recent) run <br>
   `python kgraph -u=<username> -l=10` <br>
   If you want to run a knowledge graph with the connections of each graph isolated (version 2), run <br>
   `python kgraph -u=<username> -l=10 -i`
5) Find the generated HTML in output folder
   <username>_m.html (mixed)
   <username>_i.html (-i : isolated)

## Metrics Documentation

### Network Graph

- Star (node) : This is the main article. The bigger the star the more Voters the article has. Voters are the same as unique claps (that come from different persons)
- Dot or Circle (node) : This is the external website domain. The bigger the dot the more times this domain appeared. Next to domain name there is a number that shows how many times this domain appeared.
- Edge (link) - bidirectional links between stars and dots.

This app provides 2 type of Network Graphs:
1. Isolated (with -i argument) - We focus on the connections between main articles. We can also inspect for each article the domains that were referenced in them. An external website domain can appear more than 1 time in different articles.
2. Mixed (withoun -i argument) - We focus on the connections of both main articles and external website domains. An external website domain can not appear more than 1 time. This allows us to seem the most used domains and how these domains are connected with the articles for all the articles. 

### Profile Section

- **Articles [Number]** : Number of articles that were used for the analysis (not the total number of articles of a user). Next to articles, there is also the total numbers of words.
  To find the total number of words we exclude english stopwords (based on [NTLK](https://www.nltk.org/) package) and words less than 3 characters. 
- **Top article [String]** : Top article is the article with the maximum number of voters. Voters are the same as unique claps (that come from different persons).
- **Publications [List]** : This is a frequency list of the articles based on their publication. If there is no publication the name 'Medium' is used. The format is \<publication\> \(\<articles published\>\)
- **Voters - Followers % (Article AVG) [Number]** : This is the average of the Voters / Followers per article. For an article, Voters are the same as unique claps (that come from different persons). Followers is the actual number of followers at a specific time.
- **Claps per Person (Article AVG) [Number]** : This is the average of Claps / Voters per article. For an article, Voters are the same as unique claps \(that come from different persons\)
- **Preferred Published Time [List]** : This is a frequency list of the preferred publishing time period. This refers to a time period (24h time cluster) inside a day using the following rules
    [00:00 and 05:00) : "night", "early" <br>
    [05:00 and 08:00) : "night", "late" <br>
    [08:00 and 12:00) : "morning", "morning" <br>
    [12:00 and 15:00) : "afternoon", "early" <br>
    [15:00 and 18:00) : "afternoon", "late" <br>
    [18:00 and 21:00) : "evening", "early" <br>
    [21:00 and 00:00) : "evening", "late" <br>
- **Preferred Article Length (stemmed) [Number]** : This is a frequency list of the preferred article's word length. To find the total number of words we exclude english stopwords (based on NTLK package) and words less than 3 characters. This is a cluster that is calculated using the total number of words as follows:
    words < 100 : "very short" <br>
    words < 300 : "short" <br>
    words < 500 : "normal" <br>
    words < 1800 : "large" <br>
    words > 1800 : "very large" <br>

- **Published Frequency (AVG) [Number]** : This is the average of the difference in days between the published dates of 2 consecutive articles. Next to this metric there is also the start date and the end date of the analysis.
- **Last Seen [Number]** : This the difference in days between today and the maximum published date.
- **External Domains per Article [Number]** : For each article we calculate the number of unique domains (unique per article). Then find external domains for the user and we divide with the articles of the analysis (not total articles of the user). 
- **Stemmed words / words [Number]** : This refers to the number of words if we exclude english stop words and words with less than 3 characters. Then we divide with the total number of words.
- **Unique words / words [Number]** : This refers to the unique number of words divided by the total number of words.
- **Unique words / words (stemmed) [Number]** : This refers to the unique number of words, after using Porter Stemming, if we exclude english stopwords and words with less than 3 characters, divided by the number of words if we exclude english stopwords and words with less than 3 characters.
- **Verb / words [Number]** : Using NLTK pos_tagger this the percentage of (recognised) verbs in the text.
- **Adj / words [Number]** : Using NLTK pos_tagger this the percentage of (recognised) adjectives in the text.
- **Noun / words [Number]** : Using NLTK pos_tagger this the percentage of (recognised) nouns in the text.
- **Most Common Words [List]** : This is a frequency list of the most common words after using Porter Stemming (as a representation of stemmed words we used a random original word of the stemmed version.)
- **Most Common Bigrams [List]** : This is a frequency list of the most common bigrams after using Porter Stemming (as a representation of stemmed words we used a random original word of the stemmed version.)
- **Most Common Trigrams [List]** : This is a frequency list of the most common trigrams after using Porter Stemming (as a representation of stemmed words we used a random original word of the stemmed version.)


### Article Section

- **Published At [Date]** : Published Data and publishing time period.
- **Voters - Followers % [Number]** : Voters / Followers, where Voters are the same as unique claps (that come from different persons) and Followers the number of user followers at a specific time.
- **Claps per Person [Number]** : Claps / Voters, where Voters are the same as unique claps (that come from different persons).
- **Responses [Number]** : The number of post comments.
- **Word Count (All) [Number]** : This refers to the number of words.
- **Word Count (Stemmed) [Number]** : This refers to the number of words, if we exclude english stopwords and words with less than 3 characters.
- **Stemmed words / words [Number]** : This refers to the number of words if we exclude english stop words and words with less than 3 characters. Then we divide with the total number of words.
- **Unique words / words [Number]** : This refers to the unique number of words divided by the total number of words.
- **Unique words / words (stemmed) [Number]** : This refers to the unique number of words, after using Porter Stemming, if we exclude english stopwords and words with less than 3 characters, divided by the number of words if we exclude english stopwords and words with less than 3 characters.
- **Verb / words [Number]** : Using NLTK pos_tagger this the percentage of (recognised) verbs in the text.
- **Adj / words [Number]** : Using NLTK pos_tagger this the percentage of (recognised) adjectives in the text.
- **Noun / words [Number]** : Using NLTK pos_tagger this the percentage of (recognised) nouns in the text.
- **Most Common Words [List]** : This is a frequency list of the most common words after using Porter Stemming (as a representation of stemmed words we used a random original word of the stemmed version.)
- **Most Common Bigrams [List]** : This is a frequency list of the most common bigrams after using Porter Stemming (as a representation of stemmed words we used a random original word of the stemmed version.)
- **Most Common Trigrams [List]** : This is a frequency list of the most common trigrams after using Porter Stemming (as a representation of stemmed words we used a random original word of the stemmed version.)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

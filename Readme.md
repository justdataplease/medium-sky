[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

# Analyze your Medium.com articles with Knowledge Graphs and NLP with Medium-Sky

Medium Sky is an HTML app that allows you to explore a Medium.com profile by analyzing the content of each article, as well as the relationship between the articles and
their referenced external website domains.

## Demo

Checkout [demo](https://justdataplease.com/db/medium-articles-analysis.html) (version 1)
or [demo](https://justdataplease.com/db/medium-articles-analysis-2.html) (version 2)

## How to Use

To use, you need to do the following actions

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

### Profile

- Articles :
- Top article :
- Publications :
- Voters - Followers % (Article AVG) :
- Claps per Person (Article AVG) :
- Preferred Published Time :
- Preferred Article Length (stemmed) :
- Published Frequency (AVG) :
- Last Seen :
- External Domains per Article :
- Stemmed words / words :
- Unique words / words :
- Unique words / words (stemmed) :
- Verb / words :
- Adj / words :
- Noun / words :
- Most Common Words :
- Most Common Bigrams :
- Most Common Trigrams :

### Article

- Published At :
- Voters - Followers % :
- Claps per Person :
- Responses :
- Word Count (All) :
- Word Count (Stemmed) :
- Stemmed words / words :
- Unique words / words :
- Unique words / words (stemmed) :
- Verb / words :
- Adj / words :
- Noun / words :
- Most Common Words :
- Most Common Bigrams :
- Most Common Trigrams :

Network

- Star (node) :
- Circle or Dot (node) :
- Edge (link) - links between nodes :

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

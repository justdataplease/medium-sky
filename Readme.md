# Analyze your Medium.com articles with Knowledge Graphs and NLP

We will create an HTML app to explore the content of each article, as well as the relationship between the articles and their referenced external website domains.

To replicate, you need to do the following actions

1) You need to subscribe to medium.com api [rapidapi](https://rapidapi.com/nishujain199719-vgIfuFHZxVZ/api/medium2) (you get 150 requests per month for free - this app will work for free if you have less than 148 articles)
2) Copy paste .env_sample to .env and paste you X-RapidAPI-Key that you will find [here](https://rapidapi.com/nishujain199719-vgIfuFHZxVZ/api/medium2).
3) Install requirements <br>
 `pip install -r requirements.txt`
4) Run <br>
  `python kgraph -u=<username>` 
   If you want to use a specific number of articles (10 most recent) run <br>
  `python kgraph -u=<username> -l=10` <br>
   If you want to run a knowledge graph with the connections of each graph isolated (version 2), run <br>
  `python kgraph -u=<username> -l=10 -i`
5) Find the generated HTML in output folder
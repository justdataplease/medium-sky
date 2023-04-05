from kgraph import render_html

usernames = ['justdataplease', 'umairh', 'frank-andrade', 'nikoskafritsas', 'dima806', 'anne.bonfert', 'coachtony',
             'benjaminsledge', 'kozyrkov', 'dariusforoux', 'barackobama', 'dagster-io', 'MediumStaff', 'towardsdatascience',
             'mccallisaiah']

for username in usernames:
    render_html(username=username, articles_limit=30, use_gpt=True, fixed_last_date='2023-04-05')
    print(f"finished with {username}")

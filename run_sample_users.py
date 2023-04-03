import subprocess

usernames = ['umairh', 'frank-andrade', 'nikoskafritsas', 'dima806', 'anne.bonfert', 'coachtony',
             'justdataplease', 'benjaminsledge', 'kozyrkov', 'dariusforoux', 'barackobama']

for username in usernames:
    command = f'python kgraph.py -u={username} -l=30 -ai'
    subprocess.run(command, shell=True)

    command = f'python kgraph.py -u={username} -l=30 -i -ai'
    subprocess.run(command, shell=True)

    print(f"finished with {username}")

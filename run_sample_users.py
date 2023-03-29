import subprocess

usernames = ['andre-ye', 'umairh', 'frank-andrade', 'lakshmanok', 'BernieSanders', 'nikoskafritsas', 'dima806', 'anne.bonfert', 'ngwaifoong92', 'coachtony',
             'justdataplease', 'benjaminsledge', 'datasculptor', 'kozyrkov', 'dariusforoux', 'christianlauer90', 'ev', 'barackobama', 'profgalloway']

for username in usernames:
    command = f'python kgraph.py -u={username} -l=30'
    subprocess.run(command, shell=True)

    command = f'python kgraph.py -u={username} -l=30 -i'
    subprocess.run(command, shell=True)

    print(f"finished with {username}")

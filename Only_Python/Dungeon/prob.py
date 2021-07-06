import json
import re
i = 5

def start():
    request = int(input('Решай, воин -> '))
    if request <= i:
        print('Молодец!')
    else:
        print('Ещё раз)')
        start()
start()
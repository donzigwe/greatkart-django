from datetime import datetime
from random import randint, choice




def order_id():
    """This function generates product id number (functions.py)"""
    # Convert time to string and remove - . : and " "(empty space)
    time = datetime.now().strftime("%Y%m%d")[2:]
    # Generate 5 random numbers
    random_num = []
    for i in range(4):
        random_num.append(randint(0, 9))

    # Convert the generated number string
    random_str = ""
    for i in random_num:
        random_str += ''.join(str(i))

    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'S', 'T', 'U', 'V', 'W', 'X', 'Z']
    two_letters = []
    for i in range(2):
        two_letters.append(choice(alphabet))



    # Concatenate time string and random number string
    order_num = 'GK' + time + '' + random_str + two_letters[0] + two_letters[1]
    return order_num





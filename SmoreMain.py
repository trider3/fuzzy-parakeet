import sqlite3
from twilio.rest import Client
import barcode
from random import randint
conn = sqlite3.connect('smore2.db')
cur = conn.cursor()
barcode.PROVIDED_BARCODES
['code39', 'code128', 'ean', 'ean13', 'ean8', 'gs1', 'gtin', 'isbn', 'isbn10', 'isbn13', 'issn',
 'jan', 'pzn', 'upc', 'upca']
account_sid = 'AC001e323b6665fca468c738c9a878cf06'  # Found on Twilio Console Dashboard
auth_token = '32c5570f96036f8ac4872de78eafb034'  # Found on Twilio Console Dashboard
myPhone = '8503458948'  # Phone number you used to verify your Twilio account
TwilioNumber = '+12028318212'  # Phone number given to you by Twilio
client = Client(account_sid, auth_token)

def add():
    for i in range(toAdd):
        print('What is the name of the item you want to store?')
        name = input()
        while name.isdigit():
            print('Try Again! We can\'t store a number...')
            print('What is the name of the item you want to store?')
            name = input()
        print('What color is your ' + name + '?')
        color = input()
        while color.isdigit():
            print('Try Again! ' + color + ' isn\'t a color...')
            print('What color is your ' + name + '?')
            color = input()
        print('What brand is your ' + color + ' ' + name + '?')
        brand = input()
        while brand.isdigit():
            print('Try Again! ' + brand + ' isn\'t a brand...')
            print('What brand is your ' + color + ' ' + name + '?')
            brand = input()
        print('And finally, how many ' + color + ' ' + brand + ' ' + name + 's would you like to store today?')
        number = eval(input())
        cur.execute('INSERT INTO items (name, color, brand, number) VALUES(?,?,?,?)', (name, color, brand, number))


def get():
    for i in range(toGet):
        print('What is the name of the item you want to retrieve?')
        name = input()
        while name.isdigit():
            print('Try Again! We can\'t retrieve a number...')
            print('What is the name of the item you want to retrieve?')
            name = input()
        print('What color is your ' + name + '?')
        color = input()
        while color.isdigit():
            print('Try Again! ' + color + ' isn\'t a color...')
            print('What color is your ' + name + '?')
            color = input()
        print('What brand is your ' + color + ' ' + name + '?')
        brand = input()
        while brand.isdigit():
            print('Try Again! ' + brand + ' isn\'t a brand...')
            print('What brand is your ' + color + ' ' + name + '?')
            brand = input()
        print('And finally, how many ' + color + ' ' + brand + ' ' + name + 's would you like to retrieve today?')
        number = eval(input())
        if number == 1:
            for row in cur.execute(("SELECT * FROM items WHERE name = '%s' AND color = '%s' AND brand = '%s' "
                                    "AND number " "== 1") % (name, color, brand)):
                print(row)
                client.messages.create(
                    to=myPhone,
                    from_=TwilioNumber,
                    body='Your ' + color + ' ' + brand + ' ' + name + ' will be available for pickup in '
                                                                      'about 30 minutes!')

        if number == 2:
            for row in cur.execute(("SELECT * FROM items WHERE name = '%s' AND color = '%s' "
                                    "AND brand = '%s' AND number " "== 2") % (name, color, brand)):
                print(row)
                client.messages.create(
                    to=myPhone,
                    from_=TwilioNumber,
                    body='Your ' + color + ' ' + brand + ' ' + name + 's will be available for pickup in '
                                                                      'about 30 minutes!')

        if number == 3:
            for row in cur.execute(("SELECT * FROM items WHERE name = '%s' AND color = '%s' "
                                    "AND brand = '%s' AND number " "== 3") % (name, color, brand)):
                print(row)
                client.messages.create(
                    to=myPhone,
                    from_=TwilioNumber,
                    body='Your ' + color + ' ' + brand + ' ' + name + 's will be available for pickup in '
                                                                      'about 30 minutes!')


def gen_rand(n=12):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return str(randint(range_start, range_end))


def create_code(str_of_qr_code):
    print(str_of_qr_code)
    EAN = barcode.get_barcode_class('ean13')
    EAN
    ean = EAN(str_of_qr_code)
    ean
    fullname = ean.save('ean13_barcode')
    fullname
    'ean13_barcode.svg'


print('Are you a returning user?')
fork = input()

if fork == 'no':
    cur.execute('''DROP TABLE "items";''')
    create_stmt = '''CREATE TABLE IF NOT EXISTS "items" ("name" TEXT,"color" TEXT,"brand" TEXT,"number" INT);'''
    cur.execute(create_stmt)
    print('\nWelcome to Smore!')
    print('Your user ID is:')
    create_code(gen_rand())

print('\nHow many items would you like to store with us today?')
toAdd = eval(input())
add()

if fork == 'no':
    print("\nYour storage barcode has been generated.")
    print("Congrats on making your first storage deposit with Smore! ")
    conn.commit()
    conn.close()

if fork == 'yes':
    print('How many items would you like to retrieve from your storage today?')
    toGet = eval(input())
    get()
    conn.commit()
    conn.close()

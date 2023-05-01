import jwt
import random
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def genAccessToken(items):
    token = jwt.encode(items, config['TOKENSECRET'], config['ACCESS'])
    return token

def genRefreshToken():
    # TODO: change token create method
    token = str(random.randint(0, 2**256))
    return token
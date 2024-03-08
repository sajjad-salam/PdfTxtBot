import os
from dotenv import load_dotenv
TOKEN = "6840053832:AAF17AOSNpOrcFcYnwIlsSW26pm1Mcz5zpM"

def gettoken():
    global TOKEN
    load_dotenv("config.env")
    TOKEN = os.environ.get("TOK")

gettoken()
if TOKEN == None:
    token = input("Please enter the TOKEN\nGenerated from Botfather : ")
    with open("config.env", "w") as f:
        f.write(f"TOK={token}")
    gettoken()
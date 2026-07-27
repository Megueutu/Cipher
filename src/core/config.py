import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.secret = os.getenv("enconding_secret")
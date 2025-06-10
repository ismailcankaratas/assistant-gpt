import requests
import json
import xmltodict
from requests.auth import HTTPBasicAuth
from datetime import datetime

class Function:
    def __init__(self, user) -> None:

    def get_contract(self, arguments)-> str:
        contract_number = arguments.get("contract_number")
        message = "Bu özellik şuan aktif değil!"
        return message


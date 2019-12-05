import json
from web3 import Web3, HTTPProvider

from django.conf import settings


def setup_conection():
    w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))
    abi = json.loads('[{"constant":false,"inputs":[{"internalType":"string","name":"hash","type":"string"}],"name":"addExam","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"studentAddress","type":"address"}],"name":"studentAddExam","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"constant":true,"inputs":[{"internalType":"address","name":"studentAddress","type":"address"}],"name":"checkStudentPassedExam","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getProfessorsExam","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"string","name":"hash","type":"string"}],"name":"isOwner","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"}]')
    w3.eth.defaultAccount = w3.eth.accounts[0]
    exams = w3.eth.contract(
        address=settings.CONTRACT_ADDRESS,
        abi=abi
    )

    # Test the contract
    exam_hash = "9B70ECA3C4BF210264CE44B42DE6A2095C440B857D8F94A44F7440E389A3A1BC"

    # Add an exam to the first address
    # tx_hash = exams.functions.addExam(exam_hash).transact()
    return w3, exams

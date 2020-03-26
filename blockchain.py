import _json
from time import time
import hashlib
from uuid import uuid4
from textwrap import dedent
from flask import Flask,request
from flask.json import jsonify


class Blockchain():
    pass


class blockchain(object):

    #Instantiate node
    app = Flask(__name__)
    node_identifier = str(uuid4()).replace('-','')
    blockchain = Blockchain()

    @app.route('/mine', methods=['GET'])
    def mine(self):
        last_block = blockchain.last_block
        last_proof = last_block['proof']
        proof = blockchain.proof_of_work(last_proof)

        blockchain.new_transaction(sender="0",
                                   recipient= node_identifier,
                                   amount=1)

        previous_hash = blockchain.__hash__(last_block)
        block = blockchain.new_block(proof,previous_hash)

        response = {'message': "block forged",
                    'index' : block['index'],
                    'transactions' : block['transactions'],
                    'proof' : block['proof'],
                    'previous_hash' : block['previous_hash']}

        return jsonify(response),200

    @app.route('/transactions/new',methods=['POST'])
    def new_transaction(self):
        values = request.get_json()

        required = ['sender',
                    'recipient',
                    'amount']

        if not all(k in values for k in required):
            return "Missing values",400
        blockchain.new_transaction(values['sender'],
                                   values['recipient'],
                                   values['amount'])
        block = blockchain.last_block
        index = block['index']

        response ={'message': f'new transaction will be added to block {index}'}
        return jsonify(response),201


    @app.route('/chain',methods=['GET'])
    def full_chain(self):
        response = {'chain' : blockchain.chain,
                    'Length': len(blockchain.chain)}
        return jsonify(response),200

    if __name__=='__main__':
        app.run(host='127.0.0.1', port=5000)

    def __init__(self):
        self.chain = []
        self.current_transaction = []

        # creating genesis block
        self.new_block(previous_hash=1, proof=100)

    def proof_of_work(self, last_proof):
        proof = 0

        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    def new_block(self, proof, previous_hash=None):
        block = {'index': len(self.chain) + 1,
                 'timestamp': time(),
                 'transactions': self.current_transaction,
                 'proof': proof,
                 'previous_hash': previous_hash or self.__hash__(self.chain[-1])
                 }
        self.current_transaction = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transaction.append({'sender': sender,
                                         'recipient': recipient,
                                         'Amount': amount})
        return self.last_block['index'] + 1

    @staticmethod
    def __hash__(block):
        pass

    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @property
    def last_block(self):
        # to jump to the last block
        return self.chain[-1]

import _json
from time import time
import hashlib
from uuid import uuid4
from textwrap import dedent
from flask import Flask,request
from flask.json import jsonify



class blockchain(object):

    #Instantiate node
    app = Flask(__name__)
    node_identifier = str(uuid4()).replace('-','')
    blockchain = Blockchain()

    @app.route('/mine', methods=['GET'])
    def mine(self):
        return "We will mine a new block"

    @app.route('/transactions/new',methods=['POST'])
    def new_transaction(self):

        return "we will add a new transaction"

    @app.route('/chain',methods=['GET'])
    def full_chain(self):
        response = {'chain' : blockchain.chain,
                    'Length': len(blockchain.chain)}
        return jsonify(response),200

    if __name__=='__main__':
        app.run(host='0.0.0.0', port=5000)

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
        block = {'Index': len(self.chain) + 1,
                 'Timestamp': time(),
                 'Transactions': self.current_transaction,
                 'Proof': proof,
                 'Previous Hash': previous_hash or self.__hash__(self.chain[-1])
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

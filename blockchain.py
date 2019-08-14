#!/usr/bin/env python3

import argparse
import collections
import hashlib
import json
import time
from uuid import uuid4

class Blockchain(object):

    def __init__(self):
        self.blockchain = []
        self.transactions = []

        self.genesis_block()

    def __repr__(self):
        return f'Create simple {__class__.__name__}'

    def genesis_block(self):
        """
        Calculates first block in blockchain
        """
        return self.new_block(proof=1, prev_hash=1)

    def new_block(self, proof, prev_hash=None):
        block = {
            'index': len(self.blockchain) + 1,
            'timestamp': time.time(),
            'prev_hash': prev_hash or self.hash(self.blockchain[:-1]),
            'proof': proof,
            'transaction': [] if not self.transactions else self.transactions[-1]
        }
        self.blockchain.append(block)
        return self.blockchain

    def show_blockchain(self):
        return self.blockchain

    @staticmethod
    def hash(block):
        # keep the dict ordered to avoid difference in hashes
        ordered_block = json.dumps(collections.OrderedDict(block))
        return hashlib.sha256(ordered_block.encode()).hexdigest()

    def add_transaction(self, sender, receipent, amount):
        transaction = {
            'sender': sender,
            'receipent': receipent,
            'amount': amount
        }
        self.transactions.append(transaction)
        return len(self.transactions)

    def proof_of_work(self, prev_proof):
        """
        Find a proof of work that prev_proof * proof gives hash that
        has '1111' at the end
        """
        proof = 0

        while True:
            try_ = f'{prev_proof}{proof}'.encode('utf-8')
            try_hash = hashlib.sha256(try_).hexdigest()
            if try_hash[:4] == '1111':
                break
            else:
                proof += 1
        return proof


if __name__ == '__main__':

    blockchain = Blockchain()
    node = str(uuid4())

    while True:
        print(f'What do you want to do? \n1. Add transaction. \n2. Mine new block. \n3. Finish.')
        choice = int(input('>> '))


        if choice == 1:
            sender, receipent, amount = [str(x).strip() for x in input('Provide sender, receipent and amount separated by comma\n').split(',')]
            print(f'Adding new transaction from {sender} to {receipent} of amount: {amount}')
            index = blockchain.add_transaction(sender, receipent, int(amount))
            print(f'Transaction number: {index}')
        elif choice == 2:
            print(f'Mine new block')
            last_block = blockchain.show_blockchain()[-1]
            print(f'Prev proof: {last_block["proof"]}')
            proof = blockchain.proof_of_work(last_block['proof'])
            print(f'Current proof: {proof}')
            # Add reward 
            blockchain.add_transaction("1", node, 1)
            # Add new block
            prev_hash = blockchain.hash(last_block)
            blockchain_ = blockchain.new_block(proof, prev_hash)
            print(f'{blockchain_}')
        elif choice == 3:
            break
        else:
            print('Wrong argument!')

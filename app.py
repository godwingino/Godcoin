import hashlib
import json
import time
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Simple Blockchain Implementation
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash="1", proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []  # Reset current transactions list
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"  # Difficulty level

    def create_wallet(self):
        private_key = str(hashlib.sha256(str(time.time()).encode()).hexdigest())
        public_key = hashlib.sha256(private_key.encode()).hexdigest()
        return private_key, public_key

# Initialize blockchain
blockchain = Blockchain()

# Global variable for storing wallets
wallets = {}

@app.route('/')
def home():
    return render_template('index.html', wallets=wallets)

@app.route('/wallet/<address>', methods=['GET'])
def wallet_details(address):
    balance_response = get_balance(address)
    balance = balance_response.get_json()['balance']  # Extract the 'balance' value from the response

    # Retrieve public key and private key for the wallet
    wallet = wallets.get(address)
    if not wallet:
        return jsonify({"message": "Wallet not found"}), 404

    return render_template('wallet_details.html', wallet=wallet, balance=balance)

@app.route('/wallet/new', methods=['GET'])
def generate_new_wallet():
    private_key, public_key = blockchain.create_wallet()
    wallets[public_key] = (private_key, public_key)
    return jsonify({"public_key": public_key, "private_key": private_key})

@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    balance = 0
    for block in blockchain.chain:
        for tx in block['transactions']:
            if tx['recipient'] == address:
                balance += int(tx['amount'])  # Ensure amount is treated as an integer
            if tx['sender'] == address:
                balance -= int(tx['amount'])  # Ensure amount is treated as an integer
    return jsonify({"address": address, "balance": balance})

@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    values = request.get_json()  # Get JSON data from the request

    # If no data is provided, return an error message
    if not values:
        return jsonify({"message": "No data provided"}), 400

    required_fields = ['sender', 'recipient', 'amount']

    # Check if all required fields are present in the request
    if not all(field in values for field in required_fields):
        return jsonify({"message": f"Missing values. Expected fields: {', '.join(required_fields)}"}), 400

    # Process the new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    return jsonify({"message": f"Transaction will be added to block {index}"}), 201

@app.route('/mine', methods=['GET'])
def mine():
    miner_address = request.args.get('miner_address')
    
    if not miner_address:
        return jsonify({"message": "Miner address is required"}), 400
    
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    
    # Increased reward to 50 Godcoins
    blockchain.new_transaction(
        sender="0",
        recipient=miner_address,  # Use the miner's public address as the recipient
        amount=50  # Increased from 1 to 50
    )
    
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    
    return jsonify({
        "message": "New Block Forged",
        "index": block['index'],
        "transactions": block['transactions'],
        "proof": block['proof'],
        "previous_hash": block['previous_hash'],
        "miner_address": miner_address  # Include the miner's public address in the response
    })

@app.route('/chain', methods=['GET'])
def view_chain():
    return render_template('blockchain.html', chain=blockchain.chain)


if __name__ == '__main__':
    app.run(debug=True)

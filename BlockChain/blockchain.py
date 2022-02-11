from typing import List, Optional, Dict, Union
from flask import Flask, jsonify, request
from uuid import uuid4
import hashlib
import json
import time


class Transaction(object):

    def __init__(self, sender: str, recipient: str, amount: float):
        self.sender: str = sender
        self.recipient: str = recipient
        self.amount: float = amount

    def to_dict(self):
        return self.__dict__


class Block(object):

    def __init__(self, index: int, timestamp: float, proof: int, previous_hash: str, transactions: List[Transaction]):
        self.index: int = index
        self.timestamp: float = timestamp
        self.proof: int = proof
        self.previous_hash: str = previous_hash
        self.transactions: List[Transaction] = transactions

    def to_dict(self) -> Dict[str, object]:
        ret = dict(self.__dict__)
        _t = []
        for transaction in self.transactions:
            _t.append(transaction.to_dict())
        ret["transactions"] = _t
        return ret


class BlockChain(object):

    def __init__(self):
        self.chains: List[Block] = list()
        self.current_transactions: List[Transaction] = []
        self.new_block(proof=100, pre_hash="1")

    def new_block(self, proof: int, pre_hash: str = "") -> Block:
        if not pre_hash:
            pre_hash = self.hash(self.last_block)
        block = Block(index=len(self.chains) + 1,
                      timestamp=time.time(),
                      proof=proof,
                      previous_hash=pre_hash,
                      transactions=self.current_transactions)
        self.chains.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: float) -> int:
        transaction = Transaction(sender, recipient, amount)
        self.current_transactions.append(transaction)
        return self.last_block.index + 1

    @property
    def last_block(self) -> Block:
        return self.chains[-1]

    @classmethod
    def hash(cls, block: Block) -> str:
        block_string = json.dumps(block.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof: int) -> int:
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @classmethod
    def valid_proof(cls, last_proof, proof) -> bool:
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


app = Flask(__name__)
node_identifier = str(uuid4()).replace("-", "")
block_chain = BlockChain()


@app.route("/mine", methods=["GET"])
def mine():
    last_block = block_chain.last_block
    last_proof = last_block.proof
    proof = block_chain.proof_of_work(last_proof)

    block_chain.new_transaction(sender="0", recipient=node_identifier, amount=1)
    pre_hash = block_chain.hash(last_block)
    block = block_chain.new_block(proof, pre_hash)
    response = block.to_dict()
    response["message"] = "new block forged"
    return jsonify(response), 200


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    req: Dict[str, str] = request.get_json()
    requires = ["sender", "recipient", "amount"]
    if not all(param in requires for param in req):
        return "missing param", 400
    index = block_chain.new_transaction(req["sender"], req["recipient"], float(req["amount"]))
    response = {"message": f"transaction will be add to block {index}"}
    return jsonify(response), 200


@app.route("/chain", methods=["GET"])
def full_chain():
    chains = []
    for block in block_chain.chains:
        chains.append(block.to_dict())
    response = {
        "chain:": chains,
        "length": len(chains)
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


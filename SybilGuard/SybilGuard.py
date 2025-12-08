### --- SybilGuard PoW --- ###

import hashlib
import random
import time

# Generate a deterministic target based on public key bytes
def gen_target(pubkey_bytes: bytes, target_length: int = 6) -> list:
    # Hash the public key to create a seed for the PRNG
    seed_hash = hashlib.sha256(pubkey_bytes).hexdigest()
    
    # Initialize a pseudo-random number generator with the seed
    prng = random.Random(seed_hash) 
    
    # Define the vocabulary for target generation
    vocabulary = [i for i in '0123456789abcdef'] 
    max_index = 63 # Maximum index for SHA-256 hex characters
    
    target = []
    used_indexs = set()
    
    while len(target) < target_length:
        # Generate deterministic index and value pairs
        i = prng.randint(0, max_index)
        x = prng.choice(vocabulary)
        
        if i not in used_indexs:
            used_indexs.add(i)
            target.append((i, x))
            
    return target

# Perform Proof of Work to find a valid nonce
def proof_of_work(pubkey_bytes: bytes, timestamp: int, target: list):
    nonce = 0
    while True:
        # Compute hash using public key, nonce, and timestamp
        hash = hashlib.sha256((pubkey_bytes + str(nonce).encode('utf-8') + str(timestamp).encode('utf-8'))).hexdigest()
        matches = 0
        for i, x in target:
            if hash[i] == x:
                matches += 1
        # Exit loop when all target conditions are met
        if matches == len(target):
            break
        nonce += 1
    # Generate a unique node ID based on the final hash
    node_id = hashlib.sha256(hash.encode('utf-8')).hexdigest()
    return node_id, nonce

# Verify the validity of a Proof of Work
def verify_proof_of_work(node_id: str, pubkey_bytes: bytes, nonce: int, timestamp: int) -> bool:
    # Regenerate the target using the public key
    target = gen_target(pubkey_bytes, target_length=6)  # assuming target length is known
    # Recompute the hash with the provided nonce and timestamp
    hash = hashlib.sha256((pubkey_bytes + str(nonce).encode('utf-8') + str(timestamp).encode('utf-8'))).hexdigest()
    for i, x in target:
        if hash[i] != x:
            return False
    # Verify the node ID matches the hash
    hash = hashlib.sha256(hash.encode('utf-8')).hexdigest()
    return node_id == hash


if __name__ == '__main__':

    # Example public key bytes for testing
    PUBKEY_BYTES = b'example_public_key_bytes'
    timestamp = int(time.time())

    # Generate the target for the Proof of Work
    target  = gen_target(PUBKEY_BYTES, target_length=6)
    print('Target:', target)

    # Measure the time taken to find a valid nonce
    start = time.time()
    node_id, nonce = proof_of_work(PUBKEY_BYTES, timestamp, target)

    print('Time taken:', time.time() - start)
    print('Nonce found:', nonce)
    print('Node ID:', node_id)

    # Verify the validity of the computed Proof of Work
    is_valid = verify_proof_of_work(node_id, PUBKEY_BYTES, nonce, timestamp)
    print('Proof of Work valid:', is_valid)
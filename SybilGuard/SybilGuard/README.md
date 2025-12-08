# SybilGuard Proof of Work (PoW)

## Overview
SybilGuard is a Python implementation of a Proof of Work (PoW) mechanism designed to mitigate Sybil attacks in distributed systems. This implementation ensures that nodes cannot arbitrarily choose their positions in a Distributed Hash Table (DHT) by requiring computational work to determine their node ID.

## Features
- **Target Generation**: Generates a deterministic target based on public key bytes.
- **Proof of Work**: Computes a valid nonce that satisfies the target conditions.
- **Verification**: Validates the computed Proof of Work to ensure its correctness.
- **Deterministic and Secure**: Uses SHA-256 for hashing and a pseudo-random number generator (PRNG) for deterministic target generation.

## How It Works
1. **Target Generation**:
   - A target is generated based on the public key bytes using a PRNG seeded with the SHA-256 hash of the public key.
   - The target consists of index-value pairs that the computed hash must satisfy.

2. **Proof of Work**:
   - The PoW function iteratively computes hashes using the public key, nonce, and timestamp until the hash satisfies the target conditions.
   - Once a valid nonce is found, a unique node ID is generated based on the final hash.

3. **Verification**:
   - The verification function regenerates the target and recomputes the hash to ensure the node ID and nonce are valid.

## Usage
### Prerequisites
- Python 3.6 or higher

### Running the Script
1. Clone the repository or copy the `SybilGuard.py` file to your project directory.
2. Run the script using Python:
   ```bash
   python SybilGuard.py
   ```
3. The script will:
   - Generate a target based on example public key bytes.
   - Perform the Proof of Work to find a valid nonce.
   - Verify the validity of the computed Proof of Work.

### Example Output
```
Target: [(index1, value1), (index2, value2), ...]
Time taken: X.XX seconds
Nonce found: 12345
Node ID: abcdef123456...
Proof of Work valid: True
```

## File Structure
- `SybilGuard.py`: Main script containing the implementation of the SybilGuard PoW mechanism.

## Functions
- `gen_target(pubkey_bytes: bytes, target_length: int = 6) -> list`
  - Generates a deterministic target based on public key bytes.
- `proof_of_work(pubkey_bytes: bytes, timestamp: int, target: list) -> tuple`
  - Computes a valid nonce and generates a unique node ID.
- `verify_proof_of_work(node_id: str, pubkey_bytes: bytes, nonce: int, timestamp: int) -> bool`
  - Verifies the validity of the computed Proof of Work.

## Security Considerations
- The difficulty of the PoW can be adjusted by modifying the `target_length` parameter.
- The use of SHA-256 ensures cryptographic security and resistance to preimage attacks.
- Deterministic target generation prevents nodes from manipulating their positions in the DHT.

## License
This project is licensed under the GPL License. See the LICENSE file for details.

For any questions or contributions, feel free to contact the author.
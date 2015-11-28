UC-3: Sign transaction stub
---------------------------

  To prepare the lock of tokens, the seller creates a modifiable and
  extendable dummy transaction, spending the output directed to the
  script locked destination, and requests the oracle to sign this
  transaction.

  Note: because the oracle will only sign one single transaction from
  the script locked destination, the seller requests the oracle to sign
  a blank transaction spending the output with the signature hash flags
  `NONE|ANYONECANPAY`. This transaction then serves as wildcard, and
  due to the flags it becomes possible to to add additional inputs or
  outputs. This way the seller can create an arbitrary number of
  transactions spending this one locked output, but the seller can't
  create any other transaction spending from the locked destination.

  This use-case describes the process of preparing a blank wildcard
  transaction, which is signed by the oracle.

##### Scope:

- Swap client

##### Level:

- User-goal

##### Primary actor:

- Seller

##### Supporting actor:

- Oracle

##### Preconditions:

  1. The seller configured the system's settings to connect to a running Bitcoin or Omni Core RPC server
  2. The seller configured the system's settings to connect to a running oracle server
  3. The seller generated a script locked destination (UC-1)
  4. The seller prepared a funding transaction (UC-2)

##### Main success scenario:

  1. The seller requests to create a signed transaction stub
  2. The seller provides the hash of the signed funding transaction, the index of the funding output to the target destination, the corresponding scriptPubKey, the redeemScript for the locked destination, and the public key of the oracle, which was used to create the lock
  3. The sytem creates a blank raw transaction, which has no outputs and only has one input: the locked output, spending from the locked destination
  4. The system requests the oracle to sign the transaction stub with `NONE|ANYONECANPAY`
  5. The oracle returns the signed transaction stub
  6. The system returns the signed transaction stub

##### Extensions:

5a. The oracle refuses to sign the transaction stub, because it previously signed a transaction, spending the locked output

  1. The system indicates the failure
  2. The use-case ends

5b. The oracle refuses to sign the transaction stub, because the data provided by the seller doesn't refer to a previously generated locked destination

  1. The system indicates the failure
  2. The use-case ends

##### Success guarantee:

  1. The system generated a modifiable and extendable transaction stub, spending the locked output
  2. The oracle will refuse to sign any further transactions, spending the locked output

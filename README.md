Guarded Atomic Swaps
====================

1. Introduction
---------------

For users, who want to buy or sell tokens for bitcoins, guarded atomic swaps provide an alternative to the multi-step process of offering, reserving and paying for tokens via the traditional distributed exchange.

Most notably, atomic swaps resolve the following issues of the traditional distributed exchange in particular:

-	a buyer may accept a traditional offer, but has to wait until the transaction confirms, and only then he or she can continue with the payment - the actual success rate is low, and less than 20 % of accepted offers were finalized in the past

-	a buyer can accept offers, but never finalize the trade, and intentionally or not, this locks tokens for time periods of usually 10 blocks or more, which can be abused to black out the market, by targeting or shutting down sellers or offers

-	the traditional exchange requires fees to pay for accepting an offer, to make abuse expensive, but at the same time it's not certain, whether an offer is really going to be reserved, or if it might be taken by someone else in the meantime

To overcome these issues, the actual swap of tokens for bitcoins is an atomic one-step process, which either succeeds or fails: if a buyer makes a successful payment, then it is guaranteed he or she receives the tokens in exchange, and if an offer was already taken, then the payment transaction is rejected right from the start, removing the need of reserving tokens, which may, or may not be purchased by the accepting party.

Balance based systems, such as Omni or Counterparty, in contrast to output based systems, such as Open Assets, face the challenge that tokens to be sold may be double-spent via a second transaction, which is unrelated to the swap transaction. As mitigation tokens are temporarily guarded and locked by a m-of-m multi signature script, which is signed off by one or multiple oracles and the seller of the tokens, to simulate the properties of an output based system.

Combining the concept of locking tokens and atomic swaps, the minimum number of blockchain confirmations can be reduced from two (for offering and reserving tokens) to one (for locking tokens), without the need for fancy fees or a multi-step purchase process.

While oracles introduce third-party dependencies, it is thinkable to embed the behavior of oracles into the Omni protocol at in the future, although the author believes this initial trade-off provides a good chance to test atomic swaps in the context balance based systems, before introducing new consensus rules.

2. Use cases
------------

##### 2.1. Swap client:

  1. [UC-Client-1: Create destination](doc/uc-client-1_create_destination.md)
  2. [UC-Client-2: Prepare funding](doc/uc-client-2_prepare_funding.md)
  3. [UC-Client-3: Sign transaction stub](doc/uc-client-3_sign_transaction_stub.md)
  4. [UC-Client-4: Send funding transaction](doc/uc-client-4_send_funding_transaction.md)
  5. [UC-Client-5: Unlock tokens](doc/uc-client-5_unlock_tokens.md)
  6. [UC-Client-6: Create swap offer](doc/uc-client-6_create_swap_offer.md)
  7. [UC-Client-7: Accept swap offer](doc/uc-client-7_accept_swap_offer.md)

##### 2.2. Oracle server:

  1. [UC-Oracle-1: Create new and unique key-pair](doc/uc-oracle-1_create_key_pair.md)
  2. [UC-Oracle-2: Sign transaction stub](doc/uc-oracle-2_sign_transaction_stub.md)

##### 2.3. Order server:

  1. [UC-Order-1: Publish swap offer](doc/uc-order-1_publish_order.md)
  2. [UC-Order-2: Revoke swap offer](doc/uc-order-2_revoke_order.md)
  3. [UC-Order-3: List swap offers](doc/uc-order-3_list_orders.md)

3. API
------

##### 3.1. Oracle server:

  1. [API-Oracle-1: Get new and unique public key](doc/api-oracle-1_get_getpubkey.md)
  2. [API-Oracle-2: Sign transaction stub](doc/api-oracle-2_post_sign.md)

##### 3.2. Order server:

  1. [API-Order-1: Publish a swap offer](#)
  2. [API-Order-2: Revoke a swap offer](#)
  3. [API-Order-3: List available swap offers](#)

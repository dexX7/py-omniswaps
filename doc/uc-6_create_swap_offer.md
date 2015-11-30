UC-6: Create swap offer
-----------------------

  To prepare an atomic swap, the seller extends the transaction stub
  with a transaction output to a desired destination, and the payment
  amount. This output is the payment output to the seller.

  The  transaction is then signed with the signature hash flags
  `"SINGLE|ANYONECANPAY"`, which "seals" the payment output, while
  still allowing to add further inputs or outputs. However, a potential
  buyer can't remove the payout output, which ensures the seller
  receives the desired coins in exchange, if the swap is finalized.

  This use-case describes the process of creating an atomic swap offer.

##### Scope:

- Swap client

##### Level:

- User-goal

##### Primary actor:

- Seller

##### Supporting actors:

- *None*

##### Preconditions:

1. TODO
2. TODO

##### Main success scenario:

1. TODO
2. TODO

##### Extensions:

Xa. TODO

  1. TODO
  2. TODO

##### Success guarantee:

  1. TODO
  2. TODO

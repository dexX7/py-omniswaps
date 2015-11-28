For users, who want to buy or sell tokens for bitcoins, atomic swaps using hash-locks provide an alternative to the multi-step process of offering, reserving and paying for tokens via the traditional distributed exchange.

Unlike the traditional distributed exchange, atomic swaps address the following issues in particular:

-	a buyer may accept a traditional offer, but has to wait until the transaction confirms, and only then he or she can continue with the payment - the actual success rate is low, and less than 20 % of accepted offers were finalized in the past

-	buyers can accept offers, but never finalize the trade, and intentionally or not, this locks tokens for time periods of usually 10 blocks or more, which can be abused to black out the market, by targeting or shutting down sellers or offers

-	as mitigation the traditional exchange requires fees to pay for accepting an offer, to make abuse expensive, but at the same time it's not certain, whether an offer is really going to be reserved, or if it might be taken by someone else in the meantime

To overcome these issues, the actual exchange of tokens for bitcoins is an atomic one-step process, which either succeeds or fails: if a buyer makes a successful payment, then it is guaranteed he or she receives the tokens in exchange, and if an offer was already taken, then the payment transaction is rejected right from the start, removing the need of reserving tokens, which may, or may not be purchased by the accepting party.

Balance based systems, such as Omni or Counterparty, in contrast to output based systems, such as Open Assets, face the challenge that tokens to be sold may be double-spent via a second transaction, which is unrelated to the swap transaction. As mitigation tokens are temporarily guarded and locked by a m-of-m multi signature script, which is signed off by one or multiple oracles and the seller of the tokens, to simulate the behavior of an output based system.

Combining the concept of locking tokens and atomic swaps, the minimum number of blockchain confirmations can be reduced from two (for offering and reserving tokens) to one (for hash-locking tokens), without the need for fancy fees or a multi-step purchase process.

While oracles introduce third-party dependencies, it is thinkable to embed the behavior of oracles into the Omni protocol at in the future, although the author believes this initial trade-off provides a good chance to test atomic swaps in the context balance based systems, before introducing new consensus rules.

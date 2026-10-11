---
title: Dynamic programming state and transitions
slug: dp-state-and-transition
order: 63
status: present
module: bitsandbytes.dynamic_programming.classic
---

## The idea

A dynamic-programming state is the smallest subproblem you are willing to store. The transition says how that state is computed from earlier states. For coin change, the state is the minimum number of coins that sum to an amount. min_coin_change on coins 1, 3, 4 and amount 6 returns 2, for example 3 + 3. The transition tries each coin that does not exceed the amount and adds one to the answer for the remaining amount. Amount 0 takes zero coins. A knapsack state needs two indexes. knapsack_01 on weights 1, 3, values 2, 4, and capacity 4 returns 6. Both items fit, and their values sum to 6. The transition either skips the item or takes it when the remaining capacity allows. Taking it is allowed once, which is why the item index moves forward.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Coins | coins = 2 | Amount 6 needs two coins from 1, 3, and 4. |

## Why it is correct

The coin table is correct by induction on the amount. The base amount is 0. If every smaller amount is correct, trying each coin reads a correct smaller answer and the minimum plus one is the best for this amount. Order matters. You fill smaller amounts first. The knapsack table is correct by induction on the item index and the capacity. The skip choice copies the previous item's answer. The take choice adds the value to a smaller capacity of the previous item. Both choices are available, so the cell keeps the larger one.

## What it costs

Coin change fills one cell per amount, and each cell tries every coin, so the time is the amount times the number of coins. Extra memory can be the full table or just the previous amounts. The 0-1 knapsack is items times capacity, and a rolling row brings the memory down to the capacity. Count states, then count the work inside one transition, then say whether you store every state. Those are three different numbers.

## Run it

```python
from bitsandbytes.dynamic_programming.classic import min_coin_change
print(min_coin_change([1, 3, 4], 6))
# prints: 2
```

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.

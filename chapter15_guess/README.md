# Guess (Puzzle Type #22)

This is a dedicated solver for Guess


* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/guess.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/guess.html#guess)

**Rules**

> You have a set of coloured pegs, and have to reproduce a predetermined sequence of them (chosen by the computer) within a certain number of guesses.
>
> Each guess gets marked with the number of correctly-coloured pegs in the correct places (in black), and also the number of correctly-coloured pegs in the wrong places (in white). 

Unlike most other puzzles in this repo, 'Guess' is very different. Similar to minesweeper, Guess is a limited information dynamic puzzle where the next best move depends on information revealed by previous moves (The similarities to minesweeper stop here).

The solver is designed to take the state of the board at any timestep and always gives the next optimal guess. This might seem like an impossible task at first but it's actually not too bad. The optimal guess is defined to be the one that maximizes the Shannon entropy (i.e. maximizes the expected information gain).

The steps below formaly describe the algorithm that is also used in [this 3Blue1Brown video](https://www.youtube.com/watch?v=v68zYyaEmEA) on solving Wordle using information theory. Where 3Blue1Browne describes the same steps below but for a slightly harder problem to solve wordle (a very similar game). The video intuitively justifies this algorithm and builds it from scratch using basic intuition.

To formalize the algorithm, let's first define our three inputs as
- $N :=$ the number of pegs (the length of every guess) 
  - must have $N \geq 1$ and by default $N = 4$ in the game
- $C :=$ the set of possible colors 
  - what actually matters is $|C|$, the number of possible choices for each peg, i.e. the number of colors
  - by default in the game, $C = \{R,Y,G,B,O,P\}$ (six distinct symbols; only $|C|$ matters) for Red, Yellow, Green, Blue, Orange, and Purple.
- $\mathrm{MR} := ((m_1, r_1), (m_2, r_2), ..., (m_k, r_k))$ be the sequence of previous guesses and results where $(m_i, r_i)$ is the previous guess and result at round $i$ and $k\geq 0$ is the number of previous guesses the player has made 
  - Note that $m_i$ has length $N$ and each element is $\in C$ by definition
  - $r_i$ is a triplet of non-negative integers that sum to $N$ by definition. This corresponds to counts of exact-match positions, color-only matches, and non-matches (visualized as black, white, and grey dots)

The algorithm is as follows

1. Define $G$ as the set of every possible guess that can be made

   $$G := \{(c_1, \dots, c_N) \mid \forall i \in \{1, \dots, N\},\ c_i \in C \}$$

    1. Note that $|G| = |C|^N$

    2. Note that $m_i \in G$ for all $i \in \{1, 2, ..., k\}$ by definition.

2. Define $T$ as the set of every possible result triplet 

    $$T := \{(t_1, t_2, t_3) \in \mathbb{N}_0^3 : t_1 + t_2 + t_3 = N\}$$

    1. Note that $r_i \in T$ for all $i \in \{1, 2, ..., k\}$ by definition.
    2. Note that $|T|=\binom{N+2}{2}$ (stars-and-bars)
    3. By default, $N = 4$ in the game so $|T|=15$

3. Define $f : G \times G \to T$ by $f(g_{\text{guess}}, g_{\text{truth}}) = t$ as the result triplet $(t_1, t_2, t_3)$ obtained when guessing $g_{\text{guess}}$ against ground truth $g_{\text{truth}}$. It is trivial to algorithmically make this function which simply counts from $g_1$ and $g_2.$ Look at the function `get_triplets` for a naive implementation of this.

4. Define $S$ as the subset of $G$ that is consistent with the previous guesses $m_i$ and results $r_i$

    $$
    S := \{g \in G : \forall i \in \{1, 2, ..., k\}, f(m_i, g) = r_i\}
    $$
    1. Note that if there aren't previous guesses ($\mathrm{MR} = \emptyset$) then $S = G$
    2. Note that if $S = \emptyset$ then something is wrong with the previous guesses $\mathrm{MR}$ and there is no possible solution to the puzzle. The algorithm stops here and informs the user that the puzzle is unsolvable with the given guesses $\mathrm{MR}$ and that this should never happen unless there is a typo in the guesses $\mathrm{MR}$ (which is usually the case).

5. For each possible guess $g \in G$ and each triplet $t \in T$, count the number of possible solutions $s \in S$ that result in the triplet $t$ when guessing $g$. i.e.

    $$D(g, t) := |\{s \in S: f(g, s) = t\}|$$

6. Calculate the entropy for each possible guess $g \in G$ as the sum of probability times the self-information for every triplet $t \in T$. i.e.

    $$H : G \to \mathbb{R}, \quad H(g) = -\sum_{t \in T} P(t \mid g) \log_2 P(t \mid g)$$

   1. where $P(t \mid g) = \frac{D(g, t)}{|S|}$
   2. By convention, terms with $P(t \mid g)=0$ contribute $0$ to the sum (interpreting $0\log 0 := 0)$.

7. Return the guess $g \in G$ that maximizes the entropy $H(g)$ (to break ties, choose $g$ that is also in $S$ such that it's possibly the correct solution as well, break further ties arbitrarily).
   1. i.e. return any $g^*\in (\operatorname*{argmax}_{g\in G} H(g) \cap S)$ if exists, otherwise return any $g\in \operatorname*{argmax}_{g\in G} H(g)$.


If you are at all interested in the above steps and want to understand more, 
I highly recommend watching [This 3Blue1Brown video](https://www.youtube.com/watch?v=v68zYyaEmEA) on solving Wordle using information theory where he describes the same steps but a bits more complicated problem to solve Wordle (a very similar game).

Below is an example of how to utilize the solver while in the middle of a puzzle.

(This is the only solver that under the hood does not utilize any packages besides numpy)

**Unsolved puzzle**

Let's say we start and made two guesses to end up with the following puzzle:

<img src="../images/guess_1.png" alt="Guess Pre Move" width="500">

Code to utilize this package and solve the puzzle:

We encode the puzzle as a Board object then retreive the optimal next guess:
```python
from . import solver
binst = solver.Board()
binst.add_guess(('R', 'Y', 'G', 'B'), (1, 1, 2))  # 1 black dot, 1 white dot, 2 grey dots
binst.add_guess(('R', 'G', 'O', 'P'), (0, 2, 2))  # 0 black dots, 2 white dots, 2 grey dots
binst.best_next_guess()
```

Note: the three numbers in each guess is the result of the guess: (# of black dots, # of white dots, # of grey dots)

Note: by default, the board will have 4 circles and 6 possible colors (R: Red, Y: Yellow, G: Green, B: Blue, O: Orange, P: Purple) but both of these are optional parameters to the Board to change behavior.

**Script Output 1/2**

Note that the output is next optimal guess that has the maximum Shannon entropy.
```
out of 1296 possible ground truths, only 57 are still possible.
max entropy guess is: ['P', 'Y', 'Y', 'G'] with entropy 3.4511
```

So we make our next guess as (Purple, Yellow, Yellow, Green) and let's say we get this result: (2 black, 1 white, 1 grey)

<img src="../images/guess_2.png" alt="Guess Post 1 Move" width="500">

So we input that again to the solver to retreive the next optimal guess:

```python
from . import solver
binst = solver.Board()
binst.add_guess(('R', 'Y', 'G', 'B'), (1, 1, 2))  # 1 black dot, 1 white dot, 2 grey dots
binst.add_guess(('R', 'G', 'O', 'P'), (0, 2, 2))  # 0 black dots, 2 white dots, 2 grey dots
binst.add_guess(('P', 'Y', 'Y', 'G'), (2, 1, 1))  # 2 black dots, 1 white dot, 1 grey dot
binst.best_next_guess()
```

**Script Output 2/2**

```
out of 1296 possible ground truths, only 3 are still possible.
max entropy guess is: ['G', 'Y', 'Y', 'O'] with entropy 1.5850
```

So we make our fourth guess as (Green, Yellow, Yellow, Orange) 

When we input the guess, we see that we correctly solve the puzzle!

<img src="../images/guess_3.png" alt="Guess Post 2 Moves" width="500">

Note that in this case, the correct guess was among multiple possible guesses

In the case when there's only one possible choice left, the solver will inform you that it's the garunteed solution.

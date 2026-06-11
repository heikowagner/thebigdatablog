---
categories:
- All Articles
- Coding
- JavaScript
date: '2019-06-10'
slug: teaching-a-computer-gamerules
status: publish
tags: []
title: Teaching a Computer Gamerules
wp_id: 1699
wp_modified: '2023-10-01T10:11:57'
---

## Sequential games with perfect information

### 1. A very short course in Game Theory

In the twenties people start to describe games using math. Since then Game Theory becomes an important technique in economy and and nowadays, with artificial intelligence becoming more important, even computer silence. We want to follow the usual notation but only give a very short repetition of the most important parts. For a deeper intro into the topic i recommend [A primer in Game Theory by Robert Gibbons](https://www.amazon.de/Primer-Game-Theory-Robert-Gibbons/dp/0745011594?SubscriptionId=AKIAILSHYYTFIVPWUY6Q&linkCode=xm2&camp=2025&creative=165953&creativeASIN=0745011594).
To describe a game at first we need a description of the players playing the game, in particular let ![N=\{1,\dots,n\}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-54b6b174f0ddbecf9c158f0949cfd3aa_l3.png "Rendered by QuickLaTeX.com") be the set of players. The second important information is which rules apply to the game. This is described by
![H](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-379db1fc1f84b7ce56b92463183097f9_l3.png "Rendered by QuickLaTeX.com") which is a set of all possible sequences (finite or infinite), ![h^0=\emptyset \in H](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-263a09fb2aef3cb604dde82e20aa09b4_l3.png "Rendered by QuickLaTeX.com") is the initial history and ![Z \subset H](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c74f74f93857cb832e07db52ca0c25b0_l3.png "Rendered by QuickLaTeX.com") the terminal history. To describe the histories in between we introduce the concept of actions. At each stage ![K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ea9c87a513e4a72624155d392fae86e2_l3.png "Rendered by QuickLaTeX.com") of the game the players, say ![i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-695d9d59bd04859c6c99e7feb11daab6_l3.png "Rendered by QuickLaTeX.com"), have to choose an action ![a^K_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-1581cefc7c9422278a328f631dc56c91_l3.png "Rendered by QuickLaTeX.com") from the set ![A^K_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-31e16e5f8f1691c1d4fa695bc1c2d32d_l3.png "Rendered by QuickLaTeX.com") which is the set of actions or strategies available to player ![i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-695d9d59bd04859c6c99e7feb11daab6_l3.png "Rendered by QuickLaTeX.com"). Accordingly, ![a^K \in A^K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-c70b7af17242b0bdeafe00ee5abbffee_l3.png "Rendered by QuickLaTeX.com") with ![A^K= \prod_i A^K_i](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-03cbadfa9765bd7e5f82dfe4f8643d62_l3.png "Rendered by QuickLaTeX.com"). Then a history at stage ![K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ea9c87a513e4a72624155d392fae86e2_l3.png "Rendered by QuickLaTeX.com") is described by ![h^{K+1}=(a^k)_{k=1,\dots K} \in H](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-4e37eb36e9f61795b37fb6d47637af72_l3.png "Rendered by QuickLaTeX.com") with ![a^0](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-47d04bb81ecc4ddcf4e2a9fcc846119c_l3.png "Rendered by QuickLaTeX.com") being the action profile stage 0. Accordingly for ![L<K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-0c6ccf6f60909e56a069f065f55daae7_l3.png "Rendered by QuickLaTeX.com"), ![(a^k)_{k=1,\dots L} \in H](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-dfa2342defe9c3e3f4b276d7cea36546_l3.png "Rendered by QuickLaTeX.com"),![(a^k)_{k=1}^\infty \in H](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2caf82cf8d361dda4ec79c04c3b3b946_l3.png "Rendered by QuickLaTeX.com") if ![(a^k)_{k=1,\dots K} \in H](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-66aab0f91fbe1bf5d8f6e173f52a8f06_l3.png "Rendered by QuickLaTeX.com") for all positive ![L](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-66a9f474fc3c52efdfb0ba6a70199ee8_l3.png "Rendered by QuickLaTeX.com"). We also need to determine which players turn is at a certain stage. Let ![P](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-650eb7688af6737ac325425b5c9a5982_l3.png "Rendered by QuickLaTeX.com") the player function that determines who is next to the respective sequence, ![P : H\Z \rightarrow N](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d194aae01c27014ea446563f0794736b_l3.png "Rendered by QuickLaTeX.com").
Finally we need to determine the outcomes of the game by ![u_i: Z \rightarrow \mathbb{R}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e28384b65af7d5396da1406ea524dd97_l3.png "Rendered by QuickLaTeX.com") is the set of utility functions ![u=\{u_1,\dots,u_n\}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ae4089908a28d9b6a09d80aabab49012_l3.png "Rendered by QuickLaTeX.com").
With these information we can now describe a perfect-information extensive-form game as ![G = (N,H, P, u)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7f388b74a3c85dd59741f717c20ba1e4_l3.png "Rendered by QuickLaTeX.com").

### 2. Example: Tic-Tac-Toe

[Tic-Tac-Toe](https://en.wikipedia.org/wiki/Tic-tac-toe) is a sequential two player game, who take turns marking the spaces in a ![3\times3](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-2a370987e1361a1ac63f2308c813e8a9_l3.png "Rendered by QuickLaTeX.com") grid with either ![X](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d4ee28752517d6062a3ca0314890342d_l3.png "Rendered by QuickLaTeX.com") or ![O](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-41136ed7463f7254f4e6df131f8be490_l3.png "Rendered by QuickLaTeX.com"). The player who succeeds in placing three of their marks in a horizontal, vertical, or diagonal row wins the game. If we consider a board with the nine positions numbered as follows:

|  |  |  |
| --- | --- | --- |
| 1 | 2 | 3 |
| 4 | 5 | 6 |
| 7 | 8 | 9 |

We can define the Game by ![N=\{1,2\}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-cf316ed38666aefd3b977e372d97679d_l3.png "Rendered by QuickLaTeX.com") where 1 is the Player who plays ![X](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-d4ee28752517d6062a3ca0314890342d_l3.png "Rendered by QuickLaTeX.com") and 2 the player who plays ![O](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-41136ed7463f7254f4e6df131f8be490_l3.png "Rendered by QuickLaTeX.com"). The set of all sequences ![H](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-379db1fc1f84b7ce56b92463183097f9_l3.png "Rendered by QuickLaTeX.com") is then given by ![H= \{ \emptyset, (X,1), (X,2), \dots, (X,9), ( (X,1),  (O,2) ),\dots, ( (X,2), (O,1) ), \dots,( ((X,9),(O,1)), ((X,9),(O,2)), \dots, ((X,9),(O,8)), \dots \}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e08c879fd6c01f01036a76aeed3d91ce_l3.png "Rendered by QuickLaTeX.com") where ![(X,2)](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e0cf961c06aeed95f86d10f43f5a79e9_l3.png "Rendered by QuickLaTeX.com") is a possible move of Player 1 where the second field is marked and ![( (X,2), (O,1) )](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-7ec9f87f98786ebe008624871bbe52ab_l3.png "Rendered by QuickLaTeX.com") a possible move after by Player 2 and so on. Accordingly for example ![P(\emptyset)=1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3ade47974f648ca8ac49573a1385458d_l3.png "Rendered by QuickLaTeX.com"), ![P((X,2))=2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e845db042c0499934a7c47ea10c1e4b3_l3.png "Rendered by QuickLaTeX.com"). Let ![h_{1,win}\in Z](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-e6e1e49f152653b39db03d3c828c2c06_l3.png "Rendered by QuickLaTeX.com") (draw, lost) a history where Player 1 wins the game, a possible payout function one can for example define ![u_1(h_{1,win}) = 1, u_2(h_{1,draw})=u_1(h_{1,draw}) = 0, u_1(h_{1,lost}) = -1, u_2(h_{1,win}) = -1, u_2(h_{1,lost}) = 1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-bc63fee7a028a48cc0b2ee9a9445c43b_l3.png "Rendered by QuickLaTeX.com").

### 3. Implementing a game

In the following we want “teach” a computer how to play a game. In particular this requires to let the computer know which moves ![A^K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-9d044602316c8c7c4d0765f6d87761c7_l3.png "Rendered by QuickLaTeX.com") at particular stage ![K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ea9c87a513e4a72624155d392fae86e2_l3.png "Rendered by QuickLaTeX.com") are allowed. As the reader might recognize this information is included in ![H](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-379db1fc1f84b7ce56b92463183097f9_l3.png "Rendered by QuickLaTeX.com"). Even though for simple games like [Tic-Tac-Toe](https://en.wikipedia.org/wiki/Tic-tac-toe) it is not difficult for a computer to write down (and therefore implement) ![H](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-379db1fc1f84b7ce56b92463183097f9_l3.png "Rendered by QuickLaTeX.com") in particular (in case of Tic-Tac-Toe we are dealing with 255.168 games), for more complicated games like [chess](https://en.wikipedia.org/wiki/Chess) or [GO](https://en.wikipedia.org/wiki/Go_(game)) it turns out that (at the current level of computer power) this task is impossible. This information is for example required to let the computer play the [best strategy](https://en.wikipedia.org/wiki/Subgame_perfect_equilibrium). However, this is not what we want to achieve today. At the moment we only want to construct a computer that understands and plays by the rules without a certain strategy (or more precise: a random strategy). \
To let the computer “know” the allowed actions at stage ![K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ea9c87a513e4a72624155d392fae86e2_l3.png "Rendered by QuickLaTeX.com") we introduce a new function ![\mathcal{H}: H \rightarrow A](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-02437fabcf990fc708d3444fbb192010_l3.png "Rendered by QuickLaTeX.com") which map a given history to all possible actions, ![A = \bigcup_k A^k](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-946e989b3373008dcdb111fde0b3010d_l3.png "Rendered by QuickLaTeX.com"). For example ![\mathcal{H}((X,2)) = \{ ((X,2),  (O,1)), ((X,2),  (O,3)), \dots, ((X,2),  (O,9))  \}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-3bef6f59c0bd249a15b961500fc61ebe_l3.png "Rendered by QuickLaTeX.com"). We will make another simplification here. For many games, including Tic-Tac-Toe, Chess or GO, the knowledge of the history is not necessary to make the next move. The only necessary information is the current state of the game. Games where the history is unknown are called “games with complete information” in contrast to “games with perfect information” which describes games where the history is known to each player at each stage. In the following we present a Javascript example where the computer plays [Tic-Tac-Toe](https://en.wikipedia.org/wiki/Tic-tac-toe) against himself by randomly choosing cells. The “gamerule()” maps ![\mathcal{H}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-173d4d318ade4e23f184a26004cc3766_l3.png "Rendered by QuickLaTeX.com") with “f”, ![u](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-43fe27dc3e528266a619764d90fce60b_l3.png "Rendered by QuickLaTeX.com") with “reward” and ![P](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-650eb7688af6737ac325425b5c9a5982_l3.png "Rendered by QuickLaTeX.com") with “turn”.

### 4. Final comments

At a first look the outcome of running 10.000 random games was surprising. In Table we see a clear first mover advantage. Intuitively I suspected the chances of winning the game to be equal, however after a second thought this result is not surprising because the first mover gets 5 moves as compared to 4 moves for the second player. In particular, according to [Wikipedia](https://de.wikipedia.org/wiki/Tic-Tac-Toe), there are 255.168 possible games, in 131.184 of these games the first player wins while in 77.904 the second player wins and in 46.080 the game ends with a draw. In the Table we can see that this differs from our estimation. The reason are the very special rules of the Tic-Tac\_Toe Game. In fact the game could end earlier if one player succeeds in making the row before the last turn. There are 5328 possibilities for games ending in a win on the sixth move, 47952 possibilities for games ending in a win on the seventh move, 72576 possibilities for games ending in a win on the eighth move and 81792 possibilities for games ending in a win on the ninth move.\
Since we play the Game sequentially, a path where the game ends earlier will be reached more often then path where the game ends later. To see this we take a look at a history ![h^K_1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-66273b3c2f93898714d89ca0b000095b_l3.png "Rendered by QuickLaTeX.com") that ends after ![K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ea9c87a513e4a72624155d392fae86e2_l3.png "Rendered by QuickLaTeX.com") turns and a path with a history ![h^{K+3}_2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-b53fc03367c5e752f39a087eaa9bc4a1_l3.png "Rendered by QuickLaTeX.com") that ends after ![K+3](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-45a64ff36f34be52d370037a8d8e320f_l3.png "Rendered by QuickLaTeX.com") turns. Let’s say we reach the path of each history after ![K](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-ea9c87a513e4a72624155d392fae86e2_l3.png "Rendered by QuickLaTeX.com") turns 2 times. Since for ![h^K_1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-66273b3c2f93898714d89ca0b000095b_l3.png "Rendered by QuickLaTeX.com") this is the final knot, this will count two times for ![h^K_1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-66273b3c2f93898714d89ca0b000095b_l3.png "Rendered by QuickLaTeX.com"). For ![h^K_2 \subset h^{K+3}_2](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-f3bd6fe45217b762f5f7bbb6f34152fb_l3.png "Rendered by QuickLaTeX.com") there are at least two further histories to reach in the next turn and therefore the chance to reach ![h_2^{K+3}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-07bc0054fb8bb8fbba4903fab0f57d60_l3.png "Rendered by QuickLaTeX.com") is ![\leq 0.5](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-648047d62357d70b39f181d08b301772_l3.png "Rendered by QuickLaTeX.com") which means that we will reach ![h_2^{K+3}](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-07bc0054fb8bb8fbba4903fab0f57d60_l3.png "Rendered by QuickLaTeX.com") only half as much as ![h^K_1](https://www.thebigdatablog.com/wp-content/ql-cache/quicklatex.com-66273b3c2f93898714d89ca0b000095b_l3.png "Rendered by QuickLaTeX.com"). However, doing a quick Google I was able to find some results ( [here](http://kevingong.com/Math/TicTacToe.html), [here](https://blog.ostermiller.org/tic-tac-toe-strategy) ) that supports my results.

| Outcome | Estimated probability | Wikipedia probability |
| --- | --- | --- |
| Player 1 wins | 0.5859 | 0.5141 |
| Player 2 wins | 0.2874 | 0.3053 |
| Draw | 0.1267 | 0.1806 |

```
```
/*
--Heiko Wagner 2019
*/

class Matrix {
    constructor(data, ncols) {
        //reshape the data
        this.ncols = ncols;
        var ncols = ncols;
        var data = data;
        this.matrix = []
        for (var m = 0; m &lt; data.length / ncols; m++) {
            var row = []
            for (var n = 1; n &lt;= ncols; n++) {
                row.push(data[n + (m * ncols) - 1])
            }
            this.matrix.push(row)
        }
    }
    transpose() {
        return new Matrix(this.matrix.map((_, c) =&gt; this.matrix.map(r =&gt; r[c])).flatMap(x =&gt; x), this.ncols)

    }
    trace() {
        return this.matrix.map((x, i) =&gt; x[i]).reduce((a, b) =&gt; (a === null || b == null) ? null : a + b)
    }
    rowsums() {
        return this.matrix.map((x) =&gt; x.reduce((a, b) =&gt; (a === null || b == null) ? null : a + b))
    }
    flip() {
        var nrows = this.matrix.length
        return new Matrix(this.matrix.map((x) =&gt; x.reverse().flatMap(x =&gt; x)).flatMap(x =&gt; x), nrows)
    }
}

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

function gamerules(state, turn, player) {
    //check for win else
    //win if any rowsum is 3 or 0, trace or flip.trace is 3 or 0
    var has_won = [state.rowsums(),
        state.transpose().rowsums(),
        state.trace(),
        state.flip().trace(),
    ].flatMap(x =&gt; x)

    var reward = null;

    if (has_won.includes(0)) {
        //console.log("0 has won")
        if (player == 0) {
            reward = 1
        } else {
            reward = -1
        }
    }
    
	if (has_won.includes(3)) {
        //console.log("1 has won")
        if (player == 1) {
            reward = 1
        } else {
            reward = -1
        }
    }

    var state_init = state.matrix.flatMap((x)=&gt;x)

    f = []
    for (var l = 0; l &lt; state_init.length; l++) 
    {
        var state_l = state_init.slice(0);
        if (state_init[l] == null) {
            state_l[l] = turn
            f.push(new Matrix(state_l,3) )
        }
    }
    
    //check if no free field are left ==&gt; draw
    if (f.length==0 &amp;&amp; reward == null) {
        reward = 0
    }
    return { f: f, reward: reward, turn: (turn + 1) % 2 }
}

//run trough all states of a game until an reward is reached
//play a random game starting from state with gamerules

function random_game(state) {
    //play initial turn
    var choices = gamerules(state, 1)
    while (choices.reward === null) {
        var K = choices.f.length
        var decision = getRandomInt(K)
        choices = gamerules(choices.f[decision], choices.turn, 0)
    }
    return choices
}


//Intial state of the game
var state = [null, null, null, null, null, null, null, null, null]
test = new Matrix(state, 3)
//Example of \mathcal{H}:
//gamerules(test, 1)

//Play a single random game
random_game(test)

//Play 10000 random games and make a histogram
M=10000
var win =0
var loss = 0
var draw = 0 

for (var i=0; i &lt; M; i++)
{
var outcome = random_game(test).reward

	switch(outcome) {
	  case 1:
	    win++;
	    break;
	  case -1:
	    loss++;
	    break;
	  case 0:
	  	draw++;
	} 
}

var M2=draw+win+loss
console.log("prop of player 1 winning: "+loss/M)
console.log("prop of player 2 winning: "+win/M)
console.log("prop of draw: "+draw/M)
```
```
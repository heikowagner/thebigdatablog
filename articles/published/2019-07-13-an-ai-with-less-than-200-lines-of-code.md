---
categories:
- All Articles
- Coding
- Introduction
- JavaScript
date: '2019-07-13'
slug: an-ai-with-less-than-200-lines-of-code
status: publish
tags: []
title: An AI with less than 200 lines of code
wp_id: 1824
wp_modified: '2026-06-11T18:47:43'
---

In the last two articles we covered the topics [“How to teach a computer gamerules”](https://www.thebigdatablog.com/teaching-a-computer-gamerules/) and [“The Multiarmed Bandit Problem”.](https://www.thebigdatablog.com/solving-the-multiarmed-bandit-problem-with-javascript/)  Indeed these two articles where intended to be an introduction to create a very basic AI. Some people might remember the 1984 movie [WarGames](https://en.wikipedia.org/wiki/WarGames). (Spoiler Alert) In WarGames a supercomputer gone mad and intend to nuke the world. In the end David Lightman can saved the world by teaching the computer the concept of a zero sum game, in particular due to the tic-tac-toe game which was covered in a previous [article](http://thebigdatablog.com/solving-the-multiarmed-bandit-problem-with-javascript/(opens in a new tab)). Therefore this post is about creating an AI, using JavaScript, that can play tic-tac-toe. However our AI is not limited to tic-tac-toe, by replacing the *gamerules* function by any other game, like chess or go, our AI will also be able to compete in these games.

## Montecarlo Tree Search

The technique we use is commonly known as Montecarlo Tree Search. Each round of Monte Carlo tree search consists of four steps:

- *Selection*: start from root *R* and select successive child nodes until a leaf node *L* is reached. The root is the current game state and a leaf is any node from which no simulation (playout) has yet been initiated.
- *Expansion*: unless *L* ends the game decisively (e.g. win/loss/draw) for either player, create one (or more) child nodes and choose node *C* from one of them. Child nodes are any valid moves from the game position defined by *L*. As a decision to choose C we use UCB1 which was described in the [“The Multiarmed Bandit Problem”](https://www.thebigdatablog.com/solving-the-multiarmed-bandit-problem-with-javascript/) article.
- *Simulation*: complete one random playout from node *C*.
- *Backpropagation*: use the result of the playout to update information in the nodes on the path from *C* to *R*.

\
The whole code to implement an tic-tac-toe game (less than 200 lines) is presented above. Feel free to modify the code (in the “Vue” Tab), for example modify the utility function. Changing *u={win:1,lose:-1,draw:0}* to *u={win:10,lose:-1,draw:0}* which will make the AI greedy. As an result the AI will no longer play any good and perform much riskier moves. Indeed, considering these kind of AI the only way to implement what by politicians is often called an “ethic AI” is due to the the utility function.
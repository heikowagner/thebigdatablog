/*
--Bandit.js
-This Program computes an optimal lever and average return of the multiarmed bandit problem
--Input
f=[f_1(x),...,f_K(x)]       -An Array of size K containing functions given a certain reward r eg. binomial or a normal distribution with different means
T                           -Runs to retrieve the decision (the first, t or  N  will terminate the algorithm)
--Output
sum \mu                     -the average revenue
x_out
--Heiko Wagner 2019
*/

function bandit(f, T) {
    //pull each lever once
    var x_out = f.map((x) => [x(), 1])
    var a;
    for (var t = 0; t < T; t++) {
        //determine the position with the highest value
        var j = x_out.map((x) => x[0] / x[1] + Math.sqrt((2 * Math.log(t)) / x[1]))
        a = j.reduce((iMax, x, i, arr) => x > arr[iMax] ? i : iMax, 0)
        //pull maximum lever
        x_out[a] = [x_out[a][0] + f[a](), x_out[a][1] + 1]
    }
    return [x_out.map((x) => x[0]).reduce((a, b) => a + b) / T, x_out]
}

/*
function gamerules(state, decision) {
//maybe state and decision can be collapsed to just state


//can be all possible states
return options
}
*/

//Suppose a m times m go board (matrix)
//initalize the matrix where every field is null
//if there is a black stone then the field is 0 if white then 1

//init the 3x3 xo palyfield

var state = [null, null, null, null, null, null, null, null, null]


//state.map((x,i)=> x[i] ).reduce( (a,b) => (a===null || b==null) ? null : a+b)
//turn is a boolean x:true y:false

class Matrix {
    constructor(data, ncols) {
        //check for valid matrix rows and cols
        //reshape the data
        this.ncols = ncols;
        var ncols = ncols;
        var data = data;
        this.matrix = []
        for (var m = 0; m < data.length / ncols; m++) {
            var row = []
            for (var n = 1; n <= ncols; n++) {
                row.push(data[n + (m * ncols) - 1])
            }
            this.matrix.push(row)
        }
    }
    transpose() {
        return new Matrix(this.matrix.map((_, c) => this.matrix.map(r => r[c])).flatMap(x => x), this.ncols)

    }
    trace() {
        return this.matrix.map((x, i) => x[i]).reduce((a, b) => (a === null || b == null) ? null : a + b)
    }
    rowsums() {
        return this.matrix.map((x) => x.reduce((a, b) => (a === null || b == null) ? null : a + b))
    }
    flip() {
        var nrows = this.matrix.length
        return new Matrix(this.matrix.map((x) => x.reverse().flatMap(x => x)).flatMap(x => x), nrows)
    }
}

//var state = [1, 2, 3, 4, 5, 6, 7, 8, 9]
test = new Matrix(state, 3)
test.transpose().rowsums()

function gamerules(state, player) {

    //check if there are free fields

    //if not determine who won the game (or draw)

    // reward is either 0 (lose), 1 (draw), 3 (win) or null (game ongoing)
    //options are all possible states that can be reached from the input state


    //check for win else
    //win if any rowsum is 3 or 0, trace or flip.trace is 3 or 0
    var has_won = [state.rowsums(),
        state.transpose().rowsums(),
        state.trace(),
        state.flip().trace(),
    ].flatMap(x => x)

    if (has_won.includes(3)) {
        console.log("1 has won")
        if (player == 1) {
            return 3
        } else {
            return 0
        }
    }

    if (has_won.includes(0)) {
        console.log("0 has won")
        if (player == 0) {
            return 3
        } else {
            return 0
        }
    }

    //check if no free field are left ==> draw

    if (!state.matrix.flatMap(x => x).includes(null)) {
        //draw 
        console.log("draw")
        return 1
    }

    var reward = null;
    //var turn = state[1]

    var state_init = state.matrix.flatMap((x)=>x)

    f = []
    for (var l = 0; l < state_init.length; l++) 
    {
        var state_l = state_init.slice(0);
        if (state[l] == null) {
            state_l[l] = player
            f.push(new Matrix(state_l,3) )
        }
    }
    return { f: f, reward: reward, turn: (player + 1) % 2 }
}

test = new Matrix(state, 3)
gamerules(test, 1)

//run trough all states of a game until an reward is reached

//play a random game starting from state with gamerules
function random_game(state) {
    //play initial turn
    var choices = gamerules(state, 1)
    while (choices.reward === null) {
        var K = choices.f.length
        var decision = Math.floor(Math.random() * K)
        console.log(choices.f[decision])
        choices = gamerules(choices.f[decision], choices.turn)
    }
    //return [choices.reward]
}

random_game(test)

bandit(state, 1000)

//Example
var K = 10

var f = []
for (var k = 0; k < K; k++) {
    f.push(eval('() => Math.random()*' + k))
}

bandit(f, 10000)

//Let's define a Casino Class
class Casino {
    constructor(K, m) {
        this.K = K;
        this.m = m;
    }
    levers() {
        var f = []
        for (var k = 0; k < this.K; k++) {
            f.push(eval('() => Math.random()*' + k * this.m))
        }
        return f
    }
}

var K_dash = 5
var K = 10

//To build a two stage bandit problem we build 

var f_2 = []
for (var k = 1; k <= K_dash; k++) {
    f_2.push(eval('() => { return bandit(new Casino(' + K + ',' + k + ').levers() ,1000)[0] }'))
}

bandit(f_2, 1000)
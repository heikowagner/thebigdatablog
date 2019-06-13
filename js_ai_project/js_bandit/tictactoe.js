class Matrix {
    constructor(data, ncols) {
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
    ].flatMap(x => x)

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

    var state_init = state.matrix.flatMap((x)=>x)

    f = []
    for (var l = 0; l < state_init.length; l++) 
    {
        var state_l = state_init.slice(0);
        if (state_init[l] == null) {
            state_l[l] = turn
            f.push(new Matrix(state_l,3) )
        }
    }
    
    //check if no free field are left ==> draw
    if (f.length==0 && reward == null) {
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

for (var i=0; i < M; i++)
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
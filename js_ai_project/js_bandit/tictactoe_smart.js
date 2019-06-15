
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


class bandit_turn {
    constructor(omega) {
        this.f = omega;
        this.x_out = new Array(omega.length);
        this.t=0;
    }
    pull_lever() {
        //check if each lever is at least pulled once
        for (var l=0; l<this.x_out.length; l++)
        {
            if (typeof this.x_out[l]=='undefined') {
                var reward = this.f[l]();
                this.x_out[l]= [reward, 1];
                return reward;
            }
        }

        //console.log(this.x_out)

        //if not pull the "best" layer
        var j = this.x_out.map((x) => x[0] / x[1] + Math.sqrt((2 * Math.log(this.t)) / x[1]));
        this.t=this.t+1;
        var a = j.reduce((iMax, x, i, arr) => x > arr[iMax] ? i : iMax, 0);
        //pull maximum lever
        var reward_2 =this.f[a]();
        this.x_out[a] = [this.x_out[a][0] + reward_2, this.x_out[a][1] + 1];
        return reward_2;
    }
    return_strategy() {
        return [this.x_out.map((x)=>x[0]).reduce( (a,b) =>a+b)/this.t, this.x_out];
    }
}

//A class might be good to introduce long term and short hand memory
/*
bandit = function(f, T) {
    //pull each lever once
    var band= new bandit_turn(f);

    for (var t = 0; t < T; t++) {
        band.pull_lever();
    }
    return band.return_strategy()
}
*/
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


function random_game(state) {
    //play initial turn
    //console.log('playing random')
    var choices = gamerules(state, 1)
    while (choices.reward === null) {
        var K = choices.f.length
        var decision = getRandomInt(K)
        choices = gamerules(choices.f[decision], choices.turn, 0)
    }
    return choices
}

//Use the Bandit to determine the best turn
function bandit_game(state) {
    //play initial turn
    var choices = gamerules(state, 1)
    
    //HERE COMES THE BANDIT
    while (typeof choices.reward === null) {
        var K = choices.f.length
        //console.log(choices.f[decision])
        //choices = new bandit_turn( choices.f[0] )
        choices =  new bandit_turn( choices.f.map(choice => random_game(choice, choices.turn, 0)) )

    }
    //console.log(choices)
    return choices
}

//Intial state of the game
var state = [null, null, null, null, null, null, null, null, null]
test = new Matrix(state, 3)
//Example of \mathcal{H}:
//gamerules(test, 1)

//Play a single bandit game
//var result= bandit_game(test)
//console.log(result)

var state = new Matrix(state, 3)
var choices = gamerules(state, 1)
console.log('the choice')
    console.log(choices)
    //Das muss funktional sein, hier wird es direkt ausgewertet, das ist das Problem.
    var band =  new bandit_turn( choices.f.map(choice => function() { return random_game(choice, choices.turn, 0).reward })  )
    // var test = choices.f.map(choice => '() => random_game('+choice+','+ choices.turn +', 0).reward')
    console.log(band)
   var T=15000;
   for (var t = 0; t < T; t++) {
        band.pull_lever();
    }
   console.log(band.return_strategy() )  
   //Determine the best strategy
   console.log(band.return_strategy()[1].map( x => x[0]/x[1]).reduce((iMax, x, i, arr) => x > arr[iMax] ? i : iMax, 0) )
   
   

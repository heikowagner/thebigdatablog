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

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

function gamerules(state, turn, player, u={win:1,lose:-1,draw:0}) {
    //check for win else
    //win if any rowsum is 3 or 0, trace or flip.trace is 3 or 0
    var has_won = [state.rowsums(),
        state.transpose().rowsums(),
        state.trace(),
        state.flip().trace(),
    ].flatMap(x => x)
        state.flip()
    var reward = null;

    if (has_won.includes(0)) {
        //console.log("0 has won")
        if (player == 0) {
            reward = u.win
        } else {
            reward = u.lose
        }
    }
    
    if (has_won.includes(3)) {
        //console.log("1 has won")
        if (player == 1) {
            reward = u.win
        } else {
            reward = u.lose
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
    if (f.length==1 && reward == null) {
        reward = u.draw
    }
    
    return { f: f, reward: reward, turn: (turn + 1) % 2 }
}

function random_game(state, turn, player) {
    //play initial turn
    var choices = gamerules(state, turn, player)
    while (choices.reward === null) {
        var K = choices.f.length
        var decision = getRandomInt(K)
        choices = gamerules(choices.f[decision], choices.turn, player)
    }
    return choices
}

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}



function random_game_recursive(state, turn, player) {
    //play initial turn
    var choices = gamerules(state, turn, player)
    if (choices.reward != null) {
        return choices
    } else {
        var K = choices.f.length
        var decision = getRandomInt(K)
        choices = random_game_recursive(choices.f[decision], choices.turn, player)
        return choices
    }
}


var memory = [] //should be a class

function searchStringInArray(str, strArray) {
    //console.log(strArray)
    for (var j = 0; j < strArray.length; j++) {
        //console.log(strArray[j])
        if (strArray[j][0].match(str)) return j;
    }
    return -1;
}


function getBestResponse(state, choices, turn, player) {
    //if no info is present play a random game
    var memory_pos = searchStringInArray(state.matrix.toString(), memory)
    if (memory_pos == -1) {
        console.log('Noch keine Erinnerung')
        //var K = choices.f.length
        //add state to memory
        //Pull leaver, return pulled lever
        //return getRandomInt(K)
        var games = new bandit_turn(choices.f.map(choice => function() {
            //return perfect_game_recursive(choice, choices.turn, (player + 1) % 2)
            return perfect_game_recursive(choice, choices.turn, player) //player muss natürlich gleich bleiben sonst wird der reward flasch brechnet
        }))
        memory.push([state.matrix.toString(), games, 0 ])
        memory_pos = memory.length - 1
        memory[memory_pos][3] = games.pull_lever()
        return memory[memory_pos][3].decision
    } else {
        //Pull lever return pulled lever...
        console.log('Erinnerung vorhanden')
        console.log(memory[memory_pos])
        memory[memory_pos][2]++
        memory[memory_pos][3] = memory[memory_pos][1].pull_lever()
        return memory[memory_pos][3].decision
    }
}


function perfect_game_recursive(state, turn, player) {
    //play initial turn
    var choices = gamerules(state, turn, player)
    if (choices.reward != null) {
        return choices
    } else {
        var decision = getBestResponse(state, choices, turn, player)
        choices = perfect_game_recursive(choices.f[decision], choices.turn, player)
        return choices
    }
}

/*
function perfect_game(state,turn, player) {
//console.log(state.matrix.toString())
                var choices = gamerules(state, turn, player)
        if(choices.reward != null )
            {
            console.log(choices)
            return choices 
            }
            else
            {
              var memory_pos= searchStringInArray(state.matrix.toString(),memory)
              if(searchStringInArray(state.matrix.toString(),memory) == -1)
              {
                  memory.push([state.matrix.toString(),
                  new bandit_turn( choices.f.map(choice => function() {
                    return perfect_game(choice,choices.turn, (player+1) %2 )      
                  })  ),0])
                  memory_pos= memory.length-1
                  //console.log(memory_pos)
                  //console.log(  memory )
                //pull once
                }
        
          //memory[memory_pos][1].pull_lever()
          memory[memory_pos][2]++
          memory[memory_pos][3]= memory[memory_pos][1].pull_lever()
          //make best choice
           var best_strat= memory[memory_pos][1].return_strategy()[1].map( x => x[0]/x[1]).reduce((iMax, x, i, arr) => x > arr[iMax] ? i : iMax, 0) 
         choices = gamerules(state, turn, player) // perfect_game(choices.f[best_strat], choices.turn , player )
         return choices.f[best_strat]
}
}
*/

function best_response(state, player) {
    var choices = gamerules(state, player, player)
    var band = new bandit_turn(choices.f.map(choice => function() {
        return perfect_game_recursive(choice, choices.turn, player).reward
    }))
    //return random_game_recursive(choice, choices.turn, player ).reward })  )
    //console.log(band)
    var T = 1000;
    for (var t = 0; t < T; t++) {
        band.pull_lever();
    }
    //Determine the best strategy
    console.log(memory)
    console.log(band)
    var best_strat = band.return_strategy()[1].map(x => x[0] / x[1]).reduce((iMax, x, i, arr) => x > arr[iMax] ? i : iMax, 0)
    //console.log('the best strategy is:' + best_strat)
    return choices.f[best_strat]
}

var state = [1, 0, 1, 1, 0, 1, 0, null, null]

var state_mat = new Matrix(state, 3)

//best_response(state_mat, 1)
//console.log(gamerules(state_mat, 1, 1))
console.log( getBestResponse(state_mat, gamerules(state_mat, 1, 1) , 3, 1) )
console.log( getBestResponse(state_mat, gamerules(state_mat, 1, 1) , 3, 1) )
console.log( getBestResponse(state_mat, gamerules(state_mat, 1, 1) , 3, 1) )
console.log( getBestResponse(state_mat, gamerules(state_mat, 1, 1) , 3, 1) )

console.log('Best reponse')
console.log(best_response(state_mat, 1) )
// //reward wird falsch berechnet...

// var state = [1, 0, 1, 1, 0, 1, 0, 1, 0]
// var state_mat = new Matrix(state, 3)
// console.log('warum?')
// console.log( gamerules(state_mat,1,0) )

// state=state_mat
//     var has_won = [state.rowsums(),
//         state.transpose().rowsums(),
//         state.trace(),
//         state.flip().trace(),
//     ].flatMap(x => x)

//     console.log(has_won)
//     console.log(state.transpose())


//var matrixN = math.matrix([[0, 1], [2, 3]]);

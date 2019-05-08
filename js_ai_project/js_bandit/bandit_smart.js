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
 

//Each time a Bandit of a Bandit class is executet it just runs one iteration and stores the result

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


bandit = function(f, T) {
    //pull each lever once
    var band= new bandit_turn(f);

    for (var t = 0; t < T; t++) {
        band.pull_lever();
    }
    return band.return_strategy()
}
 
//Example
var K = 10
 
var f = []
for (var k = 0; k < K; k++) {
    f.push(eval('() => Math.random()*' + k))
}
 
bandit(f, 1200)


//Example of a 2 stage Bandit
//f has to be a a set of bandits

f= [new bandit_turn(f[0]), new bandit_turn(f[1]), ... etc ]

bandit_2stages = function(f, T) {
    //pull each lever once
    var band= new bandit_turn(f.reward);

    for (var t = 0; t < T; t++) {
        band.pull_lever();
    }
    return band.return_strategy()
}
 
//this strategiy requires to evaluate all game path a priori 
//can i modify the random game that only a few are evaluated

//The algorithm should only build f if the corresponding stage is reached...
//problem we have to know where we "are"

//We can go n-stages and then play random first...

//A function that generates the f vector is needed

create_paths = function(stage)
{
    var f = []
    for (var k = 0; k < K; k++) {
        f.push(eval('() => Math.random()*' + k))
    }
}

//add the creation of states here

function random_bandit_game(state) {
    //play initial turn
    var choices = gamerules(state, 1)
    while (typeof choices.reward === null) {
        var K = choices.f.length
        //console.log(choices.f[decision])
        choices = new bandit_turn( gamerules(choices.f[0], choices.turn, 0), gamerules(choices.f[1], choices.turn, 0), ... )
    }
    //console.log(choices)
    return choices
}





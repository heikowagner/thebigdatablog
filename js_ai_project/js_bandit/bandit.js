/*
--Bandit.js
-This Program computes an decision in the multiarmed bandit problem

--Input
f=[f_1(x),...,f_K(x)]       -An Array of size K containig functions given a cetrain reward r eg. binomial or a normal distribution with different means
T                           -Runs to retrieve the decison (the first, t or  N  will terminate the algorithm)

--Output
d                           -A number d=(1,...,K) given the estimated best leaver
r                           -the average reward from that leaver

--Heiko Wagner 2019
*/

bandit = function(f, T) {
    var K = f.length;
    //pull each lever once
    var x_out = f.map((x) => [x(), 1])
    var a;
    for (var t = 0; t < T; t++) {
        //determine the position with the highest value
        var j = x_out.map((x) => x[0] / x[1] + Math.sqrt((2 * Math.log(t)) / x[1]))
        a = j.reduce((iMax, x, i, arr) => x > arr[iMax] ? i : iMax, 0);
        //pull maximum lever
        x_out[a] = [x_out[a][0] + f[a](), x_out[a][1] + 1]
    }
    return [a, x_out[a][0] / x_out[a][1]]
}



//Example
var K = 10

var f = []
for (var k = 0; k < K; k++) {
    f.push(eval('() => Math.random()*' + k))
}

//The Bandit should return a=9 and an average return of approx 4.5
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
    f_2.push(eval('() => { return bandit(new Casino(' + K + ',' + k + ').levers() ,1000)[1] }'))
}

//The Bandit should return a=4  and an average return of approx 20
bandit(f_2, 1000)
/*
--Bandit.js
-This Program computes an decision in the multiarmed bandit problem

--Input
f=[f_1(x),...,f_K(x)]       -An Array of size K containig functions given a cetrain reward r eg. binomial or a normal distribution with different means
p=[p_1,...,p_K]             -An Array of posterior probabilitys to sample from the densities above, p_i= 1/K by default
t                           -In seconds, Time to retrieve the decision
T                           -Runs to retrieve the decison (the first, t or  N  will terminate the algorithm)

--Output
d                           -A number d=(1,...,K) given the estimated best leaver
p_out=[p_1,...,p_K]         -An Array of (damn, baysian after posterior ) probabilitys to sample from the densities above


--Heiko Wagner 2019
*/

bandit = function(f, p, t, T)
{
    var that=this;
    //If p is not predifined create an array of size K with values 1/K
    var K= f.length;

    if (p == 'undefined')
    {
        p = new Array(K).fill(1/K);
    }

    var d =0;
    var p_out =p;
    //set timeout
    //setTimeout(() => {var out=[d, p_out]; console.log(out); that.return out}, t);

    var i = 0;

    for(i = 0; i < T; i++) { 
      p_out= 
    }
    
}



/*
--Bandit.js
-This Program computes an decision in the multiarmed bandit problem

--Input
f=[f_1(x),...,f_K(x)]       -An Array of size K containig functions given a cetrain reward r eg. binomial or a normal distribution with different means
p=[p_1,...,p_K]             -An Array of posterior probabilitys to sample from the densities above, p_i= 1/K by default
t                           -In seconds, Time to retrieve the decision
T                           -Runs to retrieve the decison (the first, t or  N  will terminate the algorithm)

--Output
d                           -A number d=(1,...,K) given the estimated best leaver
p_out=[p_1,...,p_K]         -An Array of (damn, baysian after posterior ) probabilitys to sample from the densities above


--Heiko Wagner 2019
*/

bandit = function(f, T, timeout)
{
    var K= f.length;
    
    //pull each lever once 
    var x_out =[]
    for(var k = 0; k < K; k++) { 
        x_out.push([f[k](), 1])
      }
    
    var a;

    for(var t = 0; t < T; t++) { 
      //determine the position with the highest value
      var j= x_out.map( (x) => x[0]/x[1] + Math.sqrt((2*Math.log(t))/x[1] ) )
      a = j.reduce((iMax, x, i, arr) => x > arr[iMax] ? i : iMax, 0);
      //pull maximum leaver
      x_out[a]=[x_out[a][0]+f[a]() ,x_out[a][1]+1]
    } 
    return [a,x_out[a][0]/x_out[a][1]]
}

//Example
var K=10

var f =[]
    for(var k = 0; k < K; k++) { 
        f.push( eval('() => Math.random()*'+k)  )
      }

//The Bandit should return 9
bandit(f,10000)



//Let's define a Casino Class
class Casino {
  constructor(K,m) {
    this.K = K;
    this.m = m;
    }
    leavers() {
        var f=[]
        for(var k = 0; k < this.K; k++) { 
            f.push( eval('() => Math.random()*'+k*this.m)  )
          }
        return f
    }
}

var K_dash=5
var K=10

//To build a two stage bandit problem we build 

var f_2 =[]
    for(var k = 1; k <= K_dash; k++) { 
        f_2.push( eval('() => { return bandit(new Casino('+K+','+k+').leavers() ,1000)[1] }')  )
      }

//The Bandit should return 4
bandit( f_2 , 1000)






class ThompsonSampler(BaseSampler):

    def __init__(self, env):
        super().__init__(env)
        
    def choose_k(self):
        # sample from posterior (this is the thompson sampling approach)
        # this leads to more exploration because machines with > uncertainty can then be selected as the machine
        self.theta = np.random.beta(self.a, self.b)
        # select machine with highest posterior p of payout
        self.k = self.variants[np.argmax(self.theta)]
        return self.k
    
    def update(self):
       
        #update dist (a, b) = (a, b) + (r, 1 - r) 
        self.a[self.k] += self.reward
        self.b[self.k] += 1 - self.reward # i.e. only increment b when it's a swing and a miss. 1 - 0 = 1, 1 - 1 = 0

        self.thetas[self.i] = self.theta[self.k]
        self.thetaregret[self.i] = np.max(self.thetas) - self.theta[self.k]

        self.ad_i[self.i] = self.k
        self.r_i[self.i] = self.reward
        */



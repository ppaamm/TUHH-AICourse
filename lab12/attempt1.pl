s(Z) :- np(X), vp(Y), append(X, Y, Z). 

vp(X) :- v(X). 

np(Z) :- determiner(X), n(Y), append(X, Y, Z).

determiner([the]).
determiner([this]). 

n([woman]).
n([man]).
n([dog]).

properNoun([eliza]).
properNoun([bob]).

v([walks]). 
v([sings]).
v([vanishes]).

adjective([big]).
adjective([hungry]).

pronoun([she]).
pronoun([he]).

wh([who]).
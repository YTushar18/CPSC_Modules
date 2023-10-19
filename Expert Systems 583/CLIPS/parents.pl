parent( pam, bob).
parent( tom, bob).
parent( tom, liz).
parent( bob, ann).
parent( bob, pat).
parent( pat, jim).


female(pam).
female(liz).
female(ann).
female(pat).
male(tom).
male(bob).
male(jim).

child(Y,X) :- parent(X,Y).

mother(X,Y) :- female(X), parent(X,Y).

grandparent(X,Z) :- parent(X,Y), parent(Y,Z).

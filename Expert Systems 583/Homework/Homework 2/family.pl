parent( pam, bob).       % Pam is a parent of Bob
parent( tom, bob).
parent( tom, liz).
parent( bob, ann).
parent( bob, pat).
parent( pat, jim).

female( pam).    % Pam is female
female( liz).
female( ann).
female( pat).
male( tom).        % Tom is male
male( bob).
male( jim).

child( Y, X) :- parent( X, Y).

mother( X, Y) :- parent( X, Y), female(X).

grandparent( X, Z) :- parent( X, Y), parent( Y, Z).

ancestor( X, Z):- parent( X, Z).
ancestor( X, Z):- parent( X, Y), ancestor( Y, Z).

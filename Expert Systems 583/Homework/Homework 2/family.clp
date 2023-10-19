(deffacts gandhis "some members of the Gandhi family"
  (parent Rajeev Indira)
  (parent Sanjay Indira)
  (parent Rahul Rajeev)
  (parent Priyanka Rajeev)
  (parent Rahul Sonia)
  (parent Priyanka Sonia)
  (parent Varun Sanjay)
)

(defrule sibling
  (parent ?x ?y)
  (parent ?z&~?x ?y)
  (not (sibling ?z ?x))
  (not (sibling ?x ?z))
=>
  (assert (sibling ?x ?z))
  (printout t ?x " and " ?z " are siblings" crlf )
)

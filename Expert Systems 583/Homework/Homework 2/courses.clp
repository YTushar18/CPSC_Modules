(deffacts courses "some courses and their prerequisites"
  (course CPSC131)
  (course CPSC335)
  (course CPSC375)
  (course CPSC481)
  (course CPSC483)
  (course MATH338)
  (prereq CPSC375 CPSC131) ; CPSC375 has CPSC131 as a prerequisite
  (prereq CPSC375 MATH338)
  (prereq CPSC481 CPSC335)
  (prereq CPSC481 MATH338)
  (prereq CPSC483 CPSC375)  
)

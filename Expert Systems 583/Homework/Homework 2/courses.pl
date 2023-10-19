course(cpsc131).
course(cpsc335).
course(cpsc375).
course(cpsc481).
course(cpsc483).
course(math338).
prereq(cpsc375, cpsc131).   % cpsc375 has cpsc131 as a prerequisite
prereq(cpsc375, math338).
prereq(cpsc481, cpsc335).
prereq(cpsc481, math338).
prereq(cpsc483, cpsc375).

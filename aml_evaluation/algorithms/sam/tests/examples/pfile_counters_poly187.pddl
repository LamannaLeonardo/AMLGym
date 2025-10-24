;; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
(define (problem instance_6_100)
	(:domain fo-counters-rnd)
	(:objects
		c0 c1 c2 c3 c4 c5 - counter
	)
  (:init
		(= (value c0) 46)
	(= (value c1) 72)
	(= (value c2) 69)
	(= (value c3) 61)
	(= (value c4) 48)
	(= (value c5) 22)

		(= (max_int) 100)
	)
	(:goal
		(and
			(= (* (value c0) (value c4)) (value c5))
	(= (value c1) 84)
	(= (value c2) 52)
	(= (value c3) 33)
		)
	)
)


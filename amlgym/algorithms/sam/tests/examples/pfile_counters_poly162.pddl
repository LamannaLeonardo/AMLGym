;; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
(define (problem instance_5_100)
	(:domain fo-counters-rnd)
	(:objects
		c0 c1 c2 c3 c4 - counter
	)
  (:init
		(= (value c0) 21)
	(= (value c1) 1)
	(= (value c2) 86)
	(= (value c3) 89)
	(= (value c4) 51)

		(= (max_int) 100)
	)
	(:goal
		(and
			(= (* (value c4) (value c3)) (value c1))
	(= (value c0) 100)
	(= (value c2) 71)
		)
	)
)


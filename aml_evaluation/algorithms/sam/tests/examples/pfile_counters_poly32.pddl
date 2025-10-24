;; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
(define (problem instance_9_100)
	(:domain fo-counters-rnd)
	(:objects
		c0 c1 c2 c3 c4 c5 c6 c7 c8 - counter
	)
  (:init
		(= (value c0) 72)
	(= (value c1) 93)
	(= (value c2) 56)
	(= (value c3) 45)
	(= (value c4) 77)
	(= (value c5) 99)
	(= (value c6) 13)
	(= (value c7) 99)
	(= (value c8) 40)

		(= (max_int) 100)
	)
	(:goal
		(and
			(= (* (value c3) (value c2)) (value c5))
	(= (value c0) 86)
	(= (value c1) 77)
	(= (value c4) 47)
	(= (value c6) 60)
	(= (value c7) 3)
	(= (value c8) 8)
		)
	)
)


;; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
(define (problem instance_3_15)
	(:domain farmland)
	(:objects
		farm0  farm1  farm2  - farm
	)
  (:init
        (= (cost) 0)
		(= (x farm0) 15)
		(= (x farm1) 1)
		(= (x farm2) 1)
		
		(adj farm0 farm1)
		(adj farm0 farm2)
		(adj farm1 farm0)
		(adj farm2 farm0)
		
	)
	(:goal
		(and
			(>= (x farm0) 1)
			(>= (x farm1) 1)
			(>= (x farm2) 1)
			
			(>= (+ (* 1.0 (x farm0))(+ (* 1.7 (x farm1))(+ (* 1.7 (x farm2)) 0))) 21.0)
		)
	)
)


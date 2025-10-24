;; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
(define (problem instance_8_7)
	(:domain farmland)
	(:objects
		farm0  farm1  farm2  farm3  farm4  farm5  farm6  farm7  - farm
	)
  (:init
        (= (cost) 0)
		(= (x farm0) 1)
		(= (x farm1) 1)
		(= (x farm2) 7)
		(= (x farm3) 0)
		(= (x farm4) 1)
		(= (x farm5) 0)
		(= (x farm6) 1)
		(= (x farm7) 1)
		
		(adj farm0 farm1)
		(adj farm0 farm2)
		(adj farm0 farm3)
		(adj farm0 farm4)
		(adj farm0 farm5)
		(adj farm0 farm6)
		(adj farm0 farm7)
		(adj farm1 farm0)
		(adj farm2 farm0)
		(adj farm3 farm0)
		(adj farm4 farm0)
		(adj farm5 farm0)
		(adj farm6 farm0)
		(adj farm7 farm0)
		
	)
	(:goal
		(and
			(>= (x farm0) 1)
			(>= (x farm1) 1)
			(>= (x farm2) 1)
			(>= (x farm3) 1)
			(>= (x farm4) 1)
			(>= (x farm5) 1)
			(>= (x farm6) 1)
			(>= (x farm7) 1)
			
			(>= (+ (* 1.7 (x farm0))(+ (* 1.2 (x farm1))(+ (* 1.0 (x farm2))(+ (* 2.0 (x farm3))(+ (* 1.4 (x farm4))(+ (* 1.5 (x farm5))(+ (* 1.5 (x farm6))(+ (* 1.6 (x farm7)) 0)))))))) 9.799999999999999)
		)
	)
)


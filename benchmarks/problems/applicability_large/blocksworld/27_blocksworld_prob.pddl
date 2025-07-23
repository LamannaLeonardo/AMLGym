

(define (problem bw_rand_10)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b1)
(on b3 b9)
(on b4 b10)
(ontable b5)
(on b6 b3)
(on b7 b2)
(on b8 b4)
(ontable b9)
(ontable b10)
(clear b5)
(clear b6)
(clear b7)
)
(:goal
(and
(on b2 b3)
(on b3 b4)
(on b4 b6)
(on b5 b10)
(on b7 b2)
(on b8 b9)
(on b9 b5))
)
)



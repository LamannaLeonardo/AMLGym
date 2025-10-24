

(define (problem bw_rand_10)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b6)
(on b3 b5)
(ontable b4)
(ontable b5)
(ontable b6)
(on b7 b8)
(on b8 b9)
(on b9 b10)
(on b10 b3)
(clear b1)
(clear b2)
(clear b7)
)
(:goal
(and
(on b1 b9)
(on b2 b6)
(on b4 b7)
(on b5 b2)
(on b9 b8)
(on b10 b3))
)
)





(define (problem bw_rand_10)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b10)
(on b2 b5)
(ontable b3)
(on b4 b6)
(on b5 b8)
(ontable b6)
(on b7 b4)
(ontable b8)
(ontable b9)
(on b10 b9)
(clear b1)
(clear b2)
(clear b3)
(clear b7)
)
(:goal
(and
(on b1 b2)
(on b4 b8)
(on b5 b10)
(on b6 b3)
(on b7 b9)
(on b9 b5))
)
)





(define (problem bw_rand_9)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b4)
(on b4 b1)
(ontable b5)
(ontable b6)
(ontable b7)
(ontable b8)
(on b9 b6)
(clear b2)
(clear b3)
(clear b5)
(clear b7)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b4)
(on b3 b1)
(on b4 b6)
(on b5 b9)
(on b6 b7)
(on b7 b5)
(on b9 b8))
)
)



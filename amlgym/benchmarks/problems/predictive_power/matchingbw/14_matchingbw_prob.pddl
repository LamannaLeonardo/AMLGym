

(define (problem matching_bw_typed_n5)
(:domain matching_bw_typed)
(:requirements :typing)
(:objects h1 h2 - hand b1 b2 b3 b4 b5  - block)
(:init
 (empty h1)
 (empty h2)
 (hand_positive h1)
 (hand_negative h2)
 (solid b1)
 (block_positive b1)
 (on_table b1)
 (solid b2)
 (block_positive b2)
 (on_table b2)
 (solid b3)
 (block_negative b3)
 (on_table b3)
 (solid b4)
 (block_negative b4)
 (on b4 b5)
 (solid b5)
 (block_negative b5)
 (on_table b5)
 (clear b1)
 (clear b2)
 (clear b3)
 (clear b4)
)
(:goal
(and
 (on b1 b5)
 (on b5 b3))
)
)



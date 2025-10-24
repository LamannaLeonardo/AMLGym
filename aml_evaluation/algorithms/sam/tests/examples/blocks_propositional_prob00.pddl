(define (problem pb0)
  (:domain blocksworld)
  (:objects
        a - block
        b - block
        c - block
        d - block
        e - block
  )
  (:init (arm-empty) (clear b) (clear c) (on-table d) (on-table e) (on a d) (on b e) (on c a))
  (:goal (and (arm-empty) (clear c) (clear d) (on-table a) (on-table b) (on c e) (on d a) (on e b))))
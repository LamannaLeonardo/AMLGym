(define (domain blocksworld)
    (:requirements :typing :strips :equality)
    (:types
        block
    )
    (:predicates
        (arm-empty)
        (clear ?a - block)
        (on-table ?a - block)
        (holding ?a - block)
        (on ?a - block ?b - block)
    )

    (:action pickup
        :parameters (?a - block)
        :precondition (and (arm-empty) (clear ?a) (on-table ?a))
        :effect (and (holding ?a) (not (arm-empty)) (not (clear ?a)) (not (on-table ?a)))
    )

    (:action putdown
        :parameters (?a - block)
        :precondition (and (holding ?a))
        :effect (and (arm-empty) (clear ?a) (on-table ?a) (not (holding ?a)))
    )

    (:action stack
        :parameters (?a - block ?b - block)
        :precondition (and (clear ?b) (holding ?a))
        :effect (and (arm-empty) (clear ?a) (on ?a ?b) (not (clear ?b)) (not (holding ?a)))
    )

    (:action unstack
        :parameters (?a - block ?b - block)
        :precondition (and (arm-empty) (clear ?a) (on ?a ?b))
        :effect (and (clear ?b) (holding ?a) (not (arm-empty)) (not (clear ?a)) (not (on ?a ?b)))
    )

)
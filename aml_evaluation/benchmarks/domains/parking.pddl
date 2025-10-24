(define (domain parking)
 (:requirements :strips :typing)
 (:types car curb)
 (:predicates
    (at_curb ?car - car)
    (at_curb_num ?car - car ?curb - curb)
    (behind_car ?car ?front_car - car)
    (car_clear ?car - car)
    (curb_clear ?curb - curb)
 )


	(:action move_curb_to_curb
		:parameters (?car - car ?curbsrc ?curbdest - curb)
		:precondition (and
			(car_clear ?car)
			(curb_clear ?curbdest)
			(at_curb_num ?car ?curbsrc)
		)
		:effect (and
			(not (curb_clear ?curbdest))
			(curb_clear ?curbsrc)
			(at_curb_num ?car ?curbdest)
			(not (at_curb_num ?car ?curbsrc))
		)
	)

	(:action move_curb_to_car
		:parameters (?car - car ?curbsrc - curb ?cardest - car)
		:precondition (and
			(car_clear ?car)
			(car_clear ?cardest)
			(at_curb_num ?car ?curbsrc)
			(at_curb ?cardest)
		)
		:effect (and
			(not (car_clear ?cardest))
			(curb_clear ?curbsrc)
			(behind_car ?car ?cardest)
			(not (at_curb_num ?car ?curbsrc))
			(not (at_curb ?car))
		)
	)

	(:action move_car_to_curb
		:parameters (?car - car ?carsrc - car ?curbdest - curb)
		:precondition (and
			(car_clear ?car)
			(curb_clear ?curbdest)
			(behind_car ?car ?carsrc)
		)
		:effect (and
			(not (curb_clear ?curbdest))
			(car_clear ?carsrc)
			(at_curb_num ?car ?curbdest)
			(not (behind_car ?car ?carsrc))
			(at_curb ?car)
		)
	)

	(:action move_car_to_car
		:parameters (?car - car ?carsrc - car ?cardest - car)
		:precondition (and
			(car_clear ?car)
			(car_clear ?cardest)
			(behind_car ?car ?carsrc)
			(at_curb ?cardest)
		)
		:effect (and
			(not (car_clear ?cardest))
			(car_clear ?carsrc)
			(behind_car ?car ?cardest)
			(not (behind_car ?car ?carsrc))
		)
	)
)

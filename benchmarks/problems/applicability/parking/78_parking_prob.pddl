(define   (problem parking)
  (:domain parking)
  (:objects
     car_0  car_1  car_2 - car
     curb_0 curb_1 curb_2 - curb
  )
  (:init
    (at_curb car_2)
    (at_curb_num car_2 curb_0)
    (car_clear car_2)
    (at_curb car_0)
    (at_curb_num car_0 curb_1)
    (car_clear car_0)
    (at_curb car_1)
    (at_curb_num car_1 curb_2)
    (car_clear car_1)
  )
  (:goal
    (and
      (at_curb_num car_0 curb_0)
      (at_curb_num car_1 curb_1)
      (at_curb_num car_2 curb_2)
    )
  )
)


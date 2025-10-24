(define   (problem parking)
  (:domain parking)
  (:objects
     car_0  car_1  car_2  car_3  car_4  car_5 - car
     curb_0 curb_1 curb_2 curb_3 curb_4 - curb
  )
  (:init
    (at_curb car_2)
    (at_curb_num car_2 curb_0)
    (behind_car car_4 car_2)
    (car_clear car_4)
    (at_curb car_3)
    (at_curb_num car_3 curb_1)
    (behind_car car_5 car_3)
    (car_clear car_5)
    (at_curb car_1)
    (at_curb_num car_1 curb_2)
    (car_clear car_1)
    (at_curb car_0)
    (at_curb_num car_0 curb_3)
    (car_clear car_0)
    (curb_clear curb_4)
  )
  (:goal
    (and
      (at_curb_num car_0 curb_0)
      (behind_car car_5 car_0)
      (at_curb_num car_1 curb_1)
      (at_curb_num car_2 curb_2)
      (at_curb_num car_3 curb_3)
      (at_curb_num car_4 curb_4)
    )
  )
)


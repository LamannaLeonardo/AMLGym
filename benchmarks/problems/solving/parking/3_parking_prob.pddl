(define   (problem parking)
  (:domain parking)
  (:objects
     car_0  car_1  car_2  car_3  car_4  car_5 - car
     curb_0 curb_1 curb_2 curb_3 - curb
  )
  (:init
    (at_curb car_3)
    (at_curb_num car_3 curb_0)
    (behind_car car_0 car_3)
    (car_clear car_0)
    (at_curb car_4)
    (at_curb_num car_4 curb_1)
    (behind_car car_1 car_4)
    (car_clear car_1)
    (at_curb car_2)
    (at_curb_num car_2 curb_2)
    (behind_car car_5 car_2)
    (car_clear car_5)
    (curb_clear curb_3)
  )
  (:goal
    (and
      (at_curb_num car_0 curb_0)
      (behind_car car_4 car_0)
      (at_curb_num car_1 curb_1)
      (behind_car car_5 car_1)
      (at_curb_num car_2 curb_2)
      (at_curb_num car_3 curb_3)
    )
  )
)


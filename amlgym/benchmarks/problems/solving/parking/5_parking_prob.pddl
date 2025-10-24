(define   (problem parking)
  (:domain parking)
  (:objects
     car_0  car_1  car_2  car_3  car_4  car_5  car_6  car_7 - car
     curb_0 curb_1 curb_2 curb_3 curb_4 - curb
  )
  (:init
    (at_curb car_5)
    (at_curb_num car_5 curb_0)
    (behind_car car_1 car_5)
    (car_clear car_1)
    (at_curb car_2)
    (at_curb_num car_2 curb_1)
    (behind_car car_7 car_2)
    (car_clear car_7)
    (at_curb car_3)
    (at_curb_num car_3 curb_2)
    (behind_car car_0 car_3)
    (car_clear car_0)
    (at_curb car_6)
    (at_curb_num car_6 curb_3)
    (behind_car car_4 car_6)
    (car_clear car_4)
    (curb_clear curb_4)
  )
  (:goal
    (and
      (at_curb_num car_0 curb_0)
      (behind_car car_5 car_0)
      (at_curb_num car_1 curb_1)
      (behind_car car_6 car_1)
      (at_curb_num car_2 curb_2)
      (behind_car car_7 car_2)
      (at_curb_num car_3 curb_3)
      (at_curb_num car_4 curb_4)
    )
  )
)


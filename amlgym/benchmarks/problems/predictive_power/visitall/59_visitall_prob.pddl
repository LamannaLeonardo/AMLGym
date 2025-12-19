(define (problem grid_4)
(:domain grid_visit_all)
(:objects 
	loc_x0_y1
	loc_x1_y0
	loc_x1_y1
	loc_x2_y1
	loc_x2_y2
	loc_x3_y0
- place 
        
)
(:init
	(at_robot loc_x2_y1)
	(visited loc_x2_y1)
	(connected loc_x0_y1 loc_x1_y1)
 	(connected loc_x1_y0 loc_x1_y1)
 	(connected loc_x1_y1 loc_x0_y1)
 	(connected loc_x1_y1 loc_x2_y1)
 	(connected loc_x1_y1 loc_x1_y0)
 	(connected loc_x2_y1 loc_x1_y1)
 	(connected loc_x2_y1 loc_x2_y2)
 	(connected loc_x2_y2 loc_x2_y1)
 
)
(:goal
(and 
	(visited loc_x1_y0)
	(visited loc_x2_y1)
	(visited loc_x2_y2)
)
)
)

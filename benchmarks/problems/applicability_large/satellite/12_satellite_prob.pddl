(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	satellite3 - satellite
	instrument3 - instrument
	infrared1 - mode
	thermograph0 - mode
	star1 - direction
	groundstation0 - direction
	groundstation2 - direction
	phenomenon3 - direction
	planet4 - direction
	star5 - direction
	star6 - direction
	phenomenon7 - direction
)
(:init
	(supports instrument0 infrared1)
	(supports instrument0 thermograph0)
	(calibration_target instrument0 star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation2)
	(supports instrument1 thermograph0)
	(calibration_target instrument1 groundstation2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star6)
	(supports instrument2 infrared1)
	(supports instrument2 thermograph0)
	(calibration_target instrument2 groundstation0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet4)
	(supports instrument3 infrared1)
	(calibration_target instrument3 groundstation2)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon7)
)
(:goal (and
	(pointing satellite3 phenomenon3)
	(have_image phenomenon3 thermograph0)
	(have_image planet4 infrared1)
	(have_image star5 infrared1)
	(have_image star6 infrared1)
	(have_image phenomenon7 infrared1)
))

)

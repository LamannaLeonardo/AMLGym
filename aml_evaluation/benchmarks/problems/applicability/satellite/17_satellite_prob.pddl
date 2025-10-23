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
	thermograph1 - mode
	image0 - mode
	groundstation0 - direction
	groundstation2 - direction
	groundstation1 - direction
	star3 - direction
	phenomenon4 - direction
	planet5 - direction
	planet6 - direction
	phenomenon7 - direction
)
(:init
	(supports instrument0 thermograph1)
	(calibration_target instrument0 groundstation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon4)
	(supports instrument1 image0)
	(supports instrument1 thermograph1)
	(calibration_target instrument1 groundstation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon7)
	(supports instrument2 image0)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 groundstation2)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation1)
	(supports instrument3 image0)
	(calibration_target instrument3 groundstation1)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation0)
)
(:goal (and
	(pointing satellite0 groundstation1)
	(pointing satellite2 phenomenon4)
	(have_image star3 image0)
	(have_image phenomenon4 thermograph1)
	(have_image planet5 image0)
	(have_image planet6 image0)
	(have_image phenomenon7 image0)
))

)

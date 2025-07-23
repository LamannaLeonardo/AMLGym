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
	satellite4 - satellite
	instrument4 - instrument
	instrument5 - instrument
	infrared0 - mode
	thermograph1 - mode
	image2 - mode
	groundstation2 - direction
	star3 - direction
	groundstation1 - direction
	star0 - direction
	planet4 - direction
	star5 - direction
	star6 - direction
	star7 - direction
	phenomenon8 - direction
	planet9 - direction
)
(:init
	(supports instrument0 image2)
	(supports instrument0 infrared0)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star6)
	(supports instrument1 thermograph1)
	(supports instrument1 infrared0)
	(supports instrument1 image2)
	(calibration_target instrument1 star0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star0)
	(supports instrument2 thermograph1)
	(supports instrument2 infrared0)
	(calibration_target instrument2 star3)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star3)
	(supports instrument3 image2)
	(supports instrument3 thermograph1)
	(calibration_target instrument3 star3)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star7)
	(supports instrument4 thermograph1)
	(calibration_target instrument4 groundstation1)
	(supports instrument5 thermograph1)
	(supports instrument5 infrared0)
	(supports instrument5 image2)
	(calibration_target instrument5 star0)
	(on_board instrument4 satellite4)
	(on_board instrument5 satellite4)
	(power_avail satellite4)
	(pointing satellite4 groundstation1)
)
(:goal (and
	(pointing satellite1 phenomenon8)
	(have_image planet4 image2)
	(have_image star5 thermograph1)
	(have_image star6 infrared0)
	(have_image star7 thermograph1)
	(have_image phenomenon8 thermograph1)
	(have_image planet9 image2)
))

)

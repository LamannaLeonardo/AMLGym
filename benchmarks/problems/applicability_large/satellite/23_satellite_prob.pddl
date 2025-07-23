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
	infrared0 - mode
	infrared2 - mode
	thermograph1 - mode
	groundstation2 - direction
	groundstation0 - direction
	star1 - direction
	planet3 - direction
	star4 - direction
	phenomenon5 - direction
	phenomenon6 - direction
	star7 - direction
)
(:init
	(supports instrument0 thermograph1)
	(supports instrument0 infrared2)
	(supports instrument0 infrared0)
	(calibration_target instrument0 groundstation2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation0)
	(supports instrument1 thermograph1)
	(supports instrument1 infrared2)
	(calibration_target instrument1 groundstation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet3)
	(supports instrument2 infrared2)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 star1)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet3)
	(supports instrument3 infrared2)
	(calibration_target instrument3 star1)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation2)
)
(:goal (and
	(pointing satellite2 star7)
	(pointing satellite3 planet3)
	(have_image planet3 infrared2)
	(have_image star4 infrared0)
	(have_image phenomenon5 thermograph1)
	(have_image phenomenon6 thermograph1)
	(have_image star7 infrared2)
))

)

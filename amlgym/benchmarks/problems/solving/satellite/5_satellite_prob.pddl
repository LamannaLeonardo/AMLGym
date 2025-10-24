(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	instrument3 - instrument
	satellite2 - satellite
	instrument4 - instrument
	instrument5 - instrument
	satellite3 - satellite
	instrument6 - instrument
	satellite4 - satellite
	instrument7 - instrument
	thermograph3 - mode
	infrared1 - mode
	infrared2 - mode
	thermograph0 - mode
	groundstation3 - direction
	groundstation1 - direction
	star2 - direction
	groundstation0 - direction
	star4 - direction
	planet5 - direction
	star6 - direction
	phenomenon7 - direction
	planet8 - direction
	star9 - direction
)
(:init
	(supports instrument0 infrared1)
	(supports instrument0 infrared2)
	(calibration_target instrument0 star2)
	(supports instrument1 infrared1)
	(calibration_target instrument1 groundstation1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation3)
	(supports instrument2 thermograph0)
	(supports instrument2 thermograph3)
	(calibration_target instrument2 groundstation0)
	(supports instrument3 thermograph0)
	(calibration_target instrument3 groundstation1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation1)
	(supports instrument4 infrared1)
	(supports instrument4 thermograph3)
	(calibration_target instrument4 groundstation0)
	(supports instrument5 thermograph0)
	(calibration_target instrument5 groundstation0)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation0)
	(supports instrument6 thermograph0)
	(supports instrument6 infrared2)
	(supports instrument6 infrared1)
	(calibration_target instrument6 star2)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet8)
	(supports instrument7 thermograph3)
	(supports instrument7 infrared1)
	(calibration_target instrument7 groundstation0)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star2)
)
(:goal (and
	(pointing satellite0 phenomenon7)
	(pointing satellite4 star9)
	(have_image star4 thermograph0)
	(have_image planet5 thermograph0)
	(have_image star6 infrared1)
	(have_image phenomenon7 infrared2)
	(have_image planet8 thermograph3)
	(have_image star9 thermograph0)
))

)

(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	satellite2 - satellite
	instrument3 - instrument
	instrument4 - instrument
	satellite3 - satellite
	instrument5 - instrument
	satellite4 - satellite
	instrument6 - instrument
	thermograph1 - mode
	thermograph2 - mode
	spectrograph0 - mode
	groundstation1 - direction
	star2 - direction
	star0 - direction
	star3 - direction
	phenomenon4 - direction
	star5 - direction
	star6 - direction
	planet7 - direction
	planet8 - direction
	planet9 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 star0)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 star3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star0)
	(supports instrument2 thermograph2)
	(calibration_target instrument2 star3)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star2)
	(supports instrument3 thermograph1)
	(supports instrument3 spectrograph0)
	(supports instrument3 thermograph2)
	(calibration_target instrument3 star0)
	(supports instrument4 spectrograph0)
	(calibration_target instrument4 star3)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon4)
	(supports instrument5 thermograph2)
	(supports instrument5 thermograph1)
	(supports instrument5 spectrograph0)
	(calibration_target instrument5 star0)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star5)
	(supports instrument6 thermograph1)
	(calibration_target instrument6 star3)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 groundstation1)
)
(:goal (and
	(pointing satellite1 star6)
	(pointing satellite2 star6)
	(have_image phenomenon4 thermograph1)
	(have_image star5 spectrograph0)
	(have_image star6 spectrograph0)
	(have_image planet7 thermograph1)
	(have_image planet8 thermograph1)
	(have_image planet9 spectrograph0)
))

)

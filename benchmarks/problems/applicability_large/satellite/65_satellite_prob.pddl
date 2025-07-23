(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	instrument3 - instrument
	satellite3 - satellite
	instrument4 - instrument
	instrument5 - instrument
	satellite4 - satellite
	instrument6 - instrument
	spectrograph3 - mode
	spectrograph0 - mode
	image2 - mode
	thermograph1 - mode
	star0 - direction
	star2 - direction
	groundstation3 - direction
	star1 - direction
	planet4 - direction
	star5 - direction
	star6 - direction
	star7 - direction
	phenomenon8 - direction
	star9 - direction
)
(:init
	(supports instrument0 image2)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star0)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 star1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star2)
	(supports instrument2 spectrograph0)
	(calibration_target instrument2 star1)
	(supports instrument3 image2)
	(supports instrument3 thermograph1)
	(supports instrument3 spectrograph3)
	(calibration_target instrument3 star1)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star2)
	(supports instrument4 thermograph1)
	(calibration_target instrument4 star1)
	(supports instrument5 spectrograph3)
	(calibration_target instrument5 groundstation3)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star0)
	(supports instrument6 spectrograph3)
	(calibration_target instrument6 star1)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star7)
)
(:goal (and
	(pointing satellite3 groundstation3)
	(pointing satellite4 phenomenon8)
	(have_image planet4 image2)
	(have_image star5 spectrograph3)
	(have_image star6 thermograph1)
	(have_image star7 thermograph1)
	(have_image phenomenon8 spectrograph3)
	(have_image star9 image2)
))

)

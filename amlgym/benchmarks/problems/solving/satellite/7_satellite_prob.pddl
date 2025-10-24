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
	satellite4 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite5 - satellite
	instrument7 - instrument
	thermograph2 - mode
	image4 - mode
	spectrograph1 - mode
	thermograph3 - mode
	spectrograph0 - mode
	groundstation0 - direction
	star2 - direction
	star3 - direction
	groundstation4 - direction
	star1 - direction
	planet5 - direction
	star6 - direction
	phenomenon7 - direction
	star8 - direction
	star9 - direction
	star10 - direction
	phenomenon11 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(supports instrument0 thermograph3)
	(supports instrument0 image4)
	(calibration_target instrument0 star2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star10)
	(supports instrument1 image4)
	(supports instrument1 spectrograph0)
	(supports instrument1 thermograph2)
	(calibration_target instrument1 star1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star6)
	(supports instrument2 image4)
	(supports instrument2 spectrograph1)
	(calibration_target instrument2 star3)
	(supports instrument3 thermograph2)
	(supports instrument3 image4)
	(calibration_target instrument3 star1)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star10)
	(supports instrument4 thermograph3)
	(supports instrument4 thermograph2)
	(calibration_target instrument4 groundstation4)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star3)
	(supports instrument5 thermograph2)
	(supports instrument5 spectrograph0)
	(calibration_target instrument5 groundstation4)
	(supports instrument6 thermograph2)
	(supports instrument6 spectrograph0)
	(supports instrument6 thermograph3)
	(calibration_target instrument6 groundstation4)
	(on_board instrument5 satellite4)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star9)
	(supports instrument7 spectrograph0)
	(calibration_target instrument7 star1)
	(on_board instrument7 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star2)
)
(:goal (and
	(pointing satellite1 star10)
	(have_image planet5 spectrograph0)
	(have_image star6 spectrograph0)
	(have_image phenomenon7 thermograph3)
	(have_image star8 thermograph3)
	(have_image star9 spectrograph1)
	(have_image star10 spectrograph1)
	(have_image phenomenon11 thermograph2)
))

)

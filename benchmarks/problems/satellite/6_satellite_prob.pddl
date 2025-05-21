(define (problem strips-sat-x-1)
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
	instrument5 - instrument
	satellite3 - satellite
	instrument6 - instrument
	instrument7 - instrument
	instrument8 - instrument
	instrument9 - instrument
	satellite4 - satellite
	instrument10 - instrument
	instrument11 - instrument
	instrument12 - instrument
	instrument13 - instrument
	satellite5 - satellite
	instrument14 - instrument
	instrument15 - instrument
	spectrograph2 - mode
	image1 - mode
	thermograph0 - mode
	spectrograph3 - mode
	groundstation1 - direction
	groundstation4 - direction
	star0 - direction
	groundstation2 - direction
	groundstation3 - direction
	phenomenon5 - direction
	planet6 - direction
	phenomenon7 - direction
	star8 - direction
	star9 - direction
	phenomenon10 - direction
	planet11 - direction
)
(:init
	(supports instrument0 thermograph0)
	(supports instrument0 spectrograph2)
	(calibration_target instrument0 groundstation1)
	(supports instrument1 image1)
	(calibration_target instrument1 groundstation2)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star9)
	(supports instrument2 spectrograph3)
	(supports instrument2 spectrograph2)
	(calibration_target instrument2 groundstation1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation2)
	(supports instrument3 thermograph0)
	(supports instrument3 spectrograph3)
	(supports instrument3 image1)
	(calibration_target instrument3 groundstation3)
	(supports instrument4 spectrograph3)
	(supports instrument4 spectrograph2)
	(supports instrument4 image1)
	(calibration_target instrument4 star0)
	(supports instrument5 spectrograph3)
	(supports instrument5 image1)
	(supports instrument5 spectrograph2)
	(calibration_target instrument5 groundstation1)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon7)
	(supports instrument6 spectrograph2)
	(supports instrument6 image1)
	(supports instrument6 spectrograph3)
	(calibration_target instrument6 groundstation2)
	(supports instrument7 image1)
	(calibration_target instrument7 groundstation1)
	(supports instrument8 image1)
	(calibration_target instrument8 groundstation4)
	(supports instrument9 image1)
	(supports instrument9 spectrograph2)
	(supports instrument9 spectrograph3)
	(calibration_target instrument9 star0)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(on_board instrument9 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet6)
	(supports instrument10 spectrograph2)
	(calibration_target instrument10 groundstation4)
	(supports instrument11 spectrograph2)
	(supports instrument11 thermograph0)
	(supports instrument11 spectrograph3)
	(calibration_target instrument11 groundstation3)
	(supports instrument12 spectrograph2)
	(supports instrument12 spectrograph3)
	(supports instrument12 thermograph0)
	(calibration_target instrument12 star0)
	(supports instrument13 thermograph0)
	(supports instrument13 image1)
	(supports instrument13 spectrograph3)
	(calibration_target instrument13 star0)
	(on_board instrument10 satellite4)
	(on_board instrument11 satellite4)
	(on_board instrument12 satellite4)
	(on_board instrument13 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star8)
	(supports instrument14 spectrograph3)
	(calibration_target instrument14 groundstation2)
	(supports instrument15 image1)
	(supports instrument15 spectrograph3)
	(supports instrument15 thermograph0)
	(calibration_target instrument15 groundstation3)
	(on_board instrument14 satellite5)
	(on_board instrument15 satellite5)
	(power_avail satellite5)
	(pointing satellite5 planet11)
)
(:goal (and
	(pointing satellite0 groundstation2)
	(pointing satellite2 star8)
	(pointing satellite4 groundstation3)
	(have_image phenomenon5 thermograph0)
	(have_image planet6 spectrograph2)
	(have_image phenomenon7 spectrograph2)
	(have_image star8 thermograph0)
	(have_image star9 spectrograph3)
	(have_image phenomenon10 thermograph0)
	(have_image planet11 image1)
))

)

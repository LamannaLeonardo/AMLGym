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
	satellite3 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite4 - satellite
	instrument7 - instrument
	satellite5 - satellite
	instrument8 - instrument
	instrument9 - instrument
	thermograph1 - mode
	image3 - mode
	spectrograph0 - mode
	infrared4 - mode
	thermograph2 - mode
	groundstation2 - direction
	star1 - direction
	groundstation0 - direction
	groundstation3 - direction
	groundstation4 - direction
	planet5 - direction
	planet6 - direction
	star7 - direction
	phenomenon8 - direction
	star9 - direction
	phenomenon10 - direction
	phenomenon11 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(calibration_target instrument0 groundstation0)
	(supports instrument1 image3)
	(supports instrument1 infrared4)
	(calibration_target instrument1 groundstation4)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet6)
	(supports instrument2 image3)
	(supports instrument2 spectrograph0)
	(calibration_target instrument2 groundstation3)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon11)
	(supports instrument3 infrared4)
	(supports instrument3 spectrograph0)
	(supports instrument3 image3)
	(calibration_target instrument3 groundstation2)
	(supports instrument4 infrared4)
	(supports instrument4 image3)
	(calibration_target instrument4 groundstation3)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation4)
	(supports instrument5 image3)
	(calibration_target instrument5 star1)
	(supports instrument6 image3)
	(supports instrument6 infrared4)
	(supports instrument6 thermograph1)
	(calibration_target instrument6 groundstation0)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star7)
	(supports instrument7 infrared4)
	(supports instrument7 thermograph2)
	(supports instrument7 thermograph1)
	(calibration_target instrument7 groundstation3)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon10)
	(supports instrument8 thermograph2)
	(supports instrument8 spectrograph0)
	(supports instrument8 thermograph1)
	(calibration_target instrument8 groundstation3)
	(supports instrument9 thermograph2)
	(supports instrument9 image3)
	(supports instrument9 spectrograph0)
	(calibration_target instrument9 groundstation4)
	(on_board instrument8 satellite5)
	(on_board instrument9 satellite5)
	(power_avail satellite5)
	(pointing satellite5 planet6)
)
(:goal (and
	(pointing satellite0 phenomenon11)
	(pointing satellite4 groundstation3)
	(have_image planet5 thermograph2)
	(have_image planet6 thermograph1)
	(have_image star7 thermograph2)
	(have_image phenomenon8 thermograph1)
	(have_image star9 thermograph1)
	(have_image phenomenon10 spectrograph0)
	(have_image phenomenon11 spectrograph0)
))

)

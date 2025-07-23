(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	instrument2 - instrument
	satellite1 - satellite
	instrument3 - instrument
	satellite2 - satellite
	instrument4 - instrument
	instrument5 - instrument
	satellite3 - satellite
	instrument6 - instrument
	satellite4 - satellite
	instrument7 - instrument
	instrument8 - instrument
	satellite5 - satellite
	instrument9 - instrument
	instrument10 - instrument
	satellite6 - satellite
	instrument11 - instrument
	instrument12 - instrument
	infrared4 - mode
	image3 - mode
	thermograph2 - mode
	spectrograph0 - mode
	thermograph1 - mode
	groundstation3 - direction
	groundstation2 - direction
	groundstation5 - direction
	groundstation0 - direction
	groundstation4 - direction
	star1 - direction
	planet6 - direction
	phenomenon7 - direction
	phenomenon8 - direction
	phenomenon9 - direction
	planet10 - direction
	phenomenon11 - direction
	star12 - direction
	phenomenon13 - direction
)
(:init
	(supports instrument0 thermograph2)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 groundstation5)
	(supports instrument1 infrared4)
	(calibration_target instrument1 groundstation0)
	(supports instrument2 thermograph2)
	(supports instrument2 spectrograph0)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 groundstation4)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon13)
	(supports instrument3 spectrograph0)
	(supports instrument3 image3)
	(supports instrument3 thermograph1)
	(calibration_target instrument3 groundstation4)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon7)
	(supports instrument4 infrared4)
	(supports instrument4 image3)
	(supports instrument4 spectrograph0)
	(calibration_target instrument4 groundstation5)
	(calibration_target instrument4 groundstation2)
	(supports instrument5 spectrograph0)
	(calibration_target instrument5 groundstation4)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon13)
	(supports instrument6 image3)
	(supports instrument6 spectrograph0)
	(calibration_target instrument6 groundstation0)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation3)
	(supports instrument7 thermograph2)
	(supports instrument7 thermograph1)
	(calibration_target instrument7 star1)
	(calibration_target instrument7 groundstation2)
	(supports instrument8 image3)
	(supports instrument8 thermograph2)
	(calibration_target instrument8 groundstation2)
	(calibration_target instrument8 groundstation5)
	(on_board instrument7 satellite4)
	(on_board instrument8 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star1)
	(supports instrument9 image3)
	(supports instrument9 thermograph1)
	(calibration_target instrument9 groundstation5)
	(calibration_target instrument9 star1)
	(supports instrument10 spectrograph0)
	(supports instrument10 thermograph2)
	(calibration_target instrument10 groundstation0)
	(on_board instrument9 satellite5)
	(on_board instrument10 satellite5)
	(power_avail satellite5)
	(pointing satellite5 planet10)
	(supports instrument11 image3)
	(calibration_target instrument11 groundstation0)
	(supports instrument12 infrared4)
	(supports instrument12 spectrograph0)
	(calibration_target instrument12 star1)
	(calibration_target instrument12 groundstation4)
	(on_board instrument11 satellite6)
	(on_board instrument12 satellite6)
	(power_avail satellite6)
	(pointing satellite6 groundstation3)
)
(:goal (and
	(have_image planet6 thermograph2)
	(have_image phenomenon7 thermograph2)
	(have_image phenomenon8 spectrograph0)
	(have_image phenomenon9 spectrograph0)
	(have_image planet10 thermograph2)
	(have_image phenomenon11 image3)
	(have_image star12 image3)
	(have_image phenomenon13 infrared4)
))

)

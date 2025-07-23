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
	satellite3 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite4 - satellite
	instrument7 - instrument
	instrument8 - instrument
	instrument9 - instrument
	satellite5 - satellite
	instrument10 - instrument
	instrument11 - instrument
	satellite6 - satellite
	instrument12 - instrument
	instrument13 - instrument
	spectrograph0 - mode
	infrared4 - mode
	spectrograph3 - mode
	thermograph1 - mode
	thermograph2 - mode
	groundstation5 - direction
	star1 - direction
	star3 - direction
	star0 - direction
	groundstation4 - direction
	groundstation2 - direction
	phenomenon6 - direction
	planet7 - direction
	planet8 - direction
	phenomenon9 - direction
	star10 - direction
	phenomenon11 - direction
	star12 - direction
	phenomenon13 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(supports instrument0 infrared4)
	(calibration_target instrument0 groundstation5)
	(supports instrument1 thermograph2)
	(supports instrument1 spectrograph3)
	(calibration_target instrument1 groundstation4)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star0)
	(supports instrument2 infrared4)
	(supports instrument2 spectrograph0)
	(calibration_target instrument2 groundstation5)
	(calibration_target instrument2 groundstation4)
	(supports instrument3 thermograph2)
	(supports instrument3 thermograph1)
	(calibration_target instrument3 star0)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon6)
	(supports instrument4 thermograph2)
	(supports instrument4 infrared4)
	(supports instrument4 spectrograph0)
	(calibration_target instrument4 groundstation2)
	(calibration_target instrument4 groundstation5)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon6)
	(supports instrument5 thermograph2)
	(calibration_target instrument5 groundstation5)
	(calibration_target instrument5 star1)
	(supports instrument6 thermograph2)
	(supports instrument6 infrared4)
	(supports instrument6 thermograph1)
	(calibration_target instrument6 groundstation4)
	(calibration_target instrument6 groundstation2)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation2)
	(supports instrument7 spectrograph3)
	(supports instrument7 thermograph2)
	(calibration_target instrument7 groundstation4)
	(calibration_target instrument7 star0)
	(supports instrument8 infrared4)
	(supports instrument8 thermograph1)
	(calibration_target instrument8 groundstation5)
	(supports instrument9 thermograph2)
	(supports instrument9 spectrograph0)
	(supports instrument9 thermograph1)
	(calibration_target instrument9 star0)
	(calibration_target instrument9 groundstation5)
	(on_board instrument7 satellite4)
	(on_board instrument8 satellite4)
	(on_board instrument9 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet8)
	(supports instrument10 thermograph1)
	(calibration_target instrument10 star3)
	(calibration_target instrument10 star1)
	(supports instrument11 thermograph1)
	(supports instrument11 spectrograph0)
	(calibration_target instrument11 groundstation2)
	(on_board instrument10 satellite5)
	(on_board instrument11 satellite5)
	(power_avail satellite5)
	(pointing satellite5 phenomenon11)
	(supports instrument12 spectrograph3)
	(supports instrument12 spectrograph0)
	(supports instrument12 infrared4)
	(calibration_target instrument12 star0)
	(supports instrument13 infrared4)
	(supports instrument13 spectrograph0)
	(calibration_target instrument13 groundstation2)
	(calibration_target instrument13 groundstation4)
	(on_board instrument12 satellite6)
	(on_board instrument13 satellite6)
	(power_avail satellite6)
	(pointing satellite6 planet8)
)
(:goal (and
	(pointing satellite5 phenomenon9)
	(have_image phenomenon6 infrared4)
	(have_image planet7 spectrograph0)
	(have_image planet8 thermograph2)
	(have_image phenomenon9 spectrograph3)
	(have_image star10 thermograph2)
	(have_image phenomenon11 thermograph2)
	(have_image star12 spectrograph0)
	(have_image phenomenon13 infrared4)
))

)

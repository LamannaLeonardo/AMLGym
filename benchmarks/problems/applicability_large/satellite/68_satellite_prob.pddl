(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	instrument2 - instrument
	satellite1 - satellite
	instrument3 - instrument
	instrument4 - instrument
	satellite2 - satellite
	instrument5 - instrument
	satellite3 - satellite
	instrument6 - instrument
	instrument7 - instrument
	instrument8 - instrument
	satellite4 - satellite
	instrument9 - instrument
	instrument10 - instrument
	satellite5 - satellite
	instrument11 - instrument
	instrument12 - instrument
	satellite6 - satellite
	instrument13 - instrument
	instrument14 - instrument
	spectrograph2 - mode
	spectrograph1 - mode
	thermograph3 - mode
	spectrograph4 - mode
	thermograph0 - mode
	groundstation4 - direction
	star2 - direction
	groundstation3 - direction
	groundstation0 - direction
	groundstation1 - direction
	groundstation5 - direction
	phenomenon6 - direction
	star7 - direction
	planet8 - direction
	star9 - direction
	star10 - direction
	planet11 - direction
	phenomenon12 - direction
	star13 - direction
)
(:init
	(supports instrument0 thermograph3)
	(supports instrument0 spectrograph2)
	(supports instrument0 thermograph0)
	(calibration_target instrument0 groundstation3)
	(supports instrument1 spectrograph4)
	(calibration_target instrument1 groundstation3)
	(calibration_target instrument1 groundstation1)
	(supports instrument2 thermograph0)
	(calibration_target instrument2 groundstation1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet8)
	(supports instrument3 spectrograph4)
	(supports instrument3 spectrograph1)
	(supports instrument3 thermograph3)
	(calibration_target instrument3 groundstation0)
	(supports instrument4 thermograph0)
	(calibration_target instrument4 groundstation0)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star2)
	(supports instrument5 spectrograph2)
	(supports instrument5 spectrograph1)
	(supports instrument5 spectrograph4)
	(calibration_target instrument5 groundstation5)
	(calibration_target instrument5 groundstation1)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation4)
	(supports instrument6 thermograph3)
	(calibration_target instrument6 groundstation3)
	(calibration_target instrument6 groundstation0)
	(supports instrument7 spectrograph4)
	(calibration_target instrument7 groundstation1)
	(supports instrument8 thermograph0)
	(supports instrument8 spectrograph4)
	(supports instrument8 thermograph3)
	(calibration_target instrument8 groundstation4)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation5)
	(supports instrument9 thermograph0)
	(calibration_target instrument9 star2)
	(calibration_target instrument9 groundstation1)
	(supports instrument10 thermograph3)
	(supports instrument10 thermograph0)
	(calibration_target instrument10 groundstation1)
	(calibration_target instrument10 star2)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet11)
	(supports instrument11 spectrograph2)
	(supports instrument11 spectrograph4)
	(calibration_target instrument11 groundstation3)
	(supports instrument12 spectrograph2)
	(supports instrument12 spectrograph1)
	(calibration_target instrument12 groundstation1)
	(on_board instrument11 satellite5)
	(on_board instrument12 satellite5)
	(power_avail satellite5)
	(pointing satellite5 groundstation4)
	(supports instrument13 spectrograph4)
	(supports instrument13 spectrograph1)
	(supports instrument13 spectrograph2)
	(calibration_target instrument13 groundstation1)
	(calibration_target instrument13 groundstation0)
	(supports instrument14 thermograph0)
	(supports instrument14 spectrograph4)
	(supports instrument14 thermograph3)
	(calibration_target instrument14 groundstation5)
	(on_board instrument13 satellite6)
	(on_board instrument14 satellite6)
	(power_avail satellite6)
	(pointing satellite6 star10)
)
(:goal (and
	(pointing satellite4 groundstation0)
	(pointing satellite5 groundstation3)
	(pointing satellite6 groundstation1)
	(have_image phenomenon6 spectrograph4)
	(have_image star7 thermograph3)
	(have_image planet8 spectrograph4)
	(have_image star9 spectrograph4)
	(have_image star10 spectrograph1)
	(have_image planet11 spectrograph4)
	(have_image phenomenon12 spectrograph4)
	(have_image star13 spectrograph2)
))

)

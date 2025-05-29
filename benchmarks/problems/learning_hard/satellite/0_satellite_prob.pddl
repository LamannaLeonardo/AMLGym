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
	instrument4 - instrument
	satellite3 - satellite
	instrument5 - instrument
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
	instrument13 - instrument
	spectrograph1 - mode
	spectrograph0 - mode
	thermograph4 - mode
	infrared2 - mode
	spectrograph3 - mode
	groundstation0 - direction
	groundstation3 - direction
	star5 - direction
	star2 - direction
	groundstation4 - direction
	groundstation1 - direction
	star6 - direction
	phenomenon7 - direction
	planet8 - direction
	phenomenon9 - direction
	planet10 - direction
	phenomenon11 - direction
	phenomenon12 - direction
	planet13 - direction
)
(:init
	(supports instrument0 spectrograph1)
	(supports instrument0 spectrograph0)
	(supports instrument0 spectrograph3)
	(calibration_target instrument0 groundstation4)
	(calibration_target instrument0 groundstation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star2)
	(supports instrument1 infrared2)
	(calibration_target instrument1 groundstation4)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation3)
	(supports instrument2 infrared2)
	(supports instrument2 thermograph4)
	(supports instrument2 spectrograph1)
	(calibration_target instrument2 groundstation4)
	(calibration_target instrument2 groundstation3)
	(supports instrument3 thermograph4)
	(supports instrument3 infrared2)
	(calibration_target instrument3 groundstation1)
	(calibration_target instrument3 star5)
	(supports instrument4 spectrograph1)
	(supports instrument4 thermograph4)
	(calibration_target instrument4 groundstation4)
	(calibration_target instrument4 groundstation1)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon7)
	(supports instrument5 spectrograph1)
	(supports instrument5 spectrograph0)
	(supports instrument5 thermograph4)
	(calibration_target instrument5 groundstation1)
	(calibration_target instrument5 groundstation0)
	(supports instrument6 thermograph4)
	(calibration_target instrument6 groundstation3)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star2)
	(supports instrument7 spectrograph3)
	(supports instrument7 thermograph4)
	(supports instrument7 spectrograph1)
	(calibration_target instrument7 groundstation3)
	(supports instrument8 spectrograph3)
	(calibration_target instrument8 star2)
	(on_board instrument7 satellite4)
	(on_board instrument8 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon12)
	(supports instrument9 spectrograph3)
	(calibration_target instrument9 groundstation4)
	(calibration_target instrument9 groundstation3)
	(supports instrument10 spectrograph1)
	(calibration_target instrument10 groundstation1)
	(calibration_target instrument10 star5)
	(on_board instrument9 satellite5)
	(on_board instrument10 satellite5)
	(power_avail satellite5)
	(pointing satellite5 phenomenon11)
	(supports instrument11 thermograph4)
	(supports instrument11 spectrograph3)
	(calibration_target instrument11 star2)
	(supports instrument12 spectrograph0)
	(supports instrument12 thermograph4)
	(calibration_target instrument12 groundstation4)
	(supports instrument13 thermograph4)
	(calibration_target instrument13 groundstation1)
	(on_board instrument11 satellite6)
	(on_board instrument12 satellite6)
	(on_board instrument13 satellite6)
	(power_avail satellite6)
	(pointing satellite6 planet10)
)
(:goal (and
	(pointing satellite0 phenomenon12)
	(pointing satellite5 planet8)
	(pointing satellite6 planet13)
	(have_image star6 infrared2)
	(have_image phenomenon7 spectrograph3)
	(have_image planet8 spectrograph3)
	(have_image phenomenon9 spectrograph3)
	(have_image planet10 spectrograph0)
	(have_image phenomenon11 spectrograph1)
	(have_image phenomenon12 spectrograph0)
	(have_image planet13 spectrograph0)
))

)

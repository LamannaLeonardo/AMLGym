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
	satellite3 - satellite
	instrument4 - instrument
	satellite4 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite5 - satellite
	instrument7 - instrument
	instrument8 - instrument
	infrared2 - mode
	spectrograph1 - mode
	thermograph3 - mode
	infrared4 - mode
	thermograph0 - mode
	groundstation2 - direction
	star4 - direction
	star3 - direction
	groundstation0 - direction
	star1 - direction
	planet5 - direction
	phenomenon6 - direction
	planet7 - direction
	phenomenon8 - direction
	phenomenon9 - direction
	phenomenon10 - direction
	star11 - direction
)
(:init
	(supports instrument0 infrared4)
	(calibration_target instrument0 star4)
	(supports instrument1 spectrograph1)
	(supports instrument1 thermograph3)
	(calibration_target instrument1 groundstation0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star3)
	(supports instrument2 thermograph0)
	(supports instrument2 infrared2)
	(calibration_target instrument2 groundstation2)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation2)
	(supports instrument3 thermograph0)
	(supports instrument3 spectrograph1)
	(calibration_target instrument3 groundstation2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet5)
	(supports instrument4 infrared4)
	(calibration_target instrument4 star4)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet7)
	(supports instrument5 spectrograph1)
	(supports instrument5 infrared2)
	(supports instrument5 thermograph0)
	(calibration_target instrument5 star3)
	(supports instrument6 spectrograph1)
	(supports instrument6 infrared4)
	(supports instrument6 thermograph0)
	(calibration_target instrument6 groundstation0)
	(on_board instrument5 satellite4)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon9)
	(supports instrument7 spectrograph1)
	(calibration_target instrument7 groundstation0)
	(supports instrument8 spectrograph1)
	(calibration_target instrument8 star1)
	(on_board instrument7 satellite5)
	(on_board instrument8 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star1)
)
(:goal (and
	(pointing satellite3 groundstation2)
	(pointing satellite5 star3)
	(have_image planet5 infrared2)
	(have_image phenomenon6 infrared4)
	(have_image planet7 thermograph3)
	(have_image phenomenon8 thermograph3)
	(have_image phenomenon9 infrared4)
	(have_image phenomenon10 infrared2)
	(have_image star11 infrared4)
))

)

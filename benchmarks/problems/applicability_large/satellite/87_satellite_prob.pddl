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
	instrument5 - instrument
	satellite4 - satellite
	instrument6 - instrument
	satellite5 - satellite
	instrument7 - instrument
	instrument8 - instrument
	spectrograph1 - mode
	spectrograph4 - mode
	thermograph0 - mode
	thermograph2 - mode
	spectrograph3 - mode
	groundstation4 - direction
	star1 - direction
	star3 - direction
	groundstation2 - direction
	star0 - direction
	star5 - direction
	planet6 - direction
	planet7 - direction
	planet8 - direction
	planet9 - direction
	phenomenon10 - direction
	phenomenon11 - direction
)
(:init
	(supports instrument0 spectrograph3)
	(supports instrument0 thermograph2)
	(supports instrument0 spectrograph4)
	(calibration_target instrument0 groundstation2)
	(supports instrument1 thermograph0)
	(supports instrument1 spectrograph3)
	(calibration_target instrument1 star3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation4)
	(supports instrument2 spectrograph4)
	(supports instrument2 spectrograph1)
	(supports instrument2 spectrograph3)
	(calibration_target instrument2 star3)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star1)
	(supports instrument3 spectrograph3)
	(calibration_target instrument3 star3)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon11)
	(supports instrument4 thermograph0)
	(calibration_target instrument4 star1)
	(supports instrument5 spectrograph4)
	(calibration_target instrument5 star3)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon10)
	(supports instrument6 spectrograph4)
	(supports instrument6 spectrograph1)
	(calibration_target instrument6 groundstation2)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet6)
	(supports instrument7 spectrograph4)
	(supports instrument7 spectrograph1)
	(calibration_target instrument7 star0)
	(supports instrument8 thermograph0)
	(calibration_target instrument8 star0)
	(on_board instrument7 satellite5)
	(on_board instrument8 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star1)
)
(:goal (and
	(pointing satellite4 planet9)
	(have_image star5 spectrograph3)
	(have_image planet6 spectrograph4)
	(have_image planet7 spectrograph3)
	(have_image planet8 thermograph0)
	(have_image planet9 spectrograph3)
	(have_image phenomenon10 thermograph2)
	(have_image phenomenon11 thermograph2)
))

)

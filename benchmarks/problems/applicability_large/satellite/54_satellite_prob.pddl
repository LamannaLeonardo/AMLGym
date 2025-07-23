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
	instrument7 - instrument
	spectrograph0 - mode
	spectrograph1 - mode
	spectrograph2 - mode
	groundstation0 - direction
	groundstation2 - direction
	star3 - direction
	star1 - direction
	star4 - direction
	planet5 - direction
	phenomenon6 - direction
	phenomenon7 - direction
	star8 - direction
	planet9 - direction
)
(:init
	(supports instrument0 spectrograph2)
	(calibration_target instrument0 star3)
	(supports instrument1 spectrograph2)
	(supports instrument1 spectrograph1)
	(calibration_target instrument1 groundstation0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation2)
	(supports instrument2 spectrograph0)
	(supports instrument2 spectrograph1)
	(calibration_target instrument2 star3)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation2)
	(supports instrument3 spectrograph2)
	(supports instrument3 spectrograph0)
	(calibration_target instrument3 star1)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star4)
	(supports instrument4 spectrograph0)
	(calibration_target instrument4 groundstation2)
	(supports instrument5 spectrograph1)
	(supports instrument5 spectrograph0)
	(supports instrument5 spectrograph2)
	(calibration_target instrument5 star1)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star3)
	(supports instrument6 spectrograph0)
	(calibration_target instrument6 star3)
	(supports instrument7 spectrograph0)
	(calibration_target instrument7 star1)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star4)
)
(:goal (and
	(pointing satellite0 star3)
	(pointing satellite2 groundstation0)
	(pointing satellite4 star4)
	(have_image star4 spectrograph1)
	(have_image planet5 spectrograph0)
	(have_image phenomenon6 spectrograph1)
	(have_image phenomenon7 spectrograph0)
	(have_image star8 spectrograph0)
	(have_image planet9 spectrograph0)
))

)

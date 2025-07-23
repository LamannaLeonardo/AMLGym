(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	satellite3 - satellite
	instrument3 - instrument
	infrared2 - mode
	spectrograph0 - mode
	infrared1 - mode
	star1 - direction
	groundstation2 - direction
	groundstation0 - direction
	planet3 - direction
	star4 - direction
	star5 - direction
	phenomenon6 - direction
	star7 - direction
)
(:init
	(supports instrument0 infrared2)
	(supports instrument0 infrared1)
	(calibration_target instrument0 groundstation2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star1)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 groundstation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation0)
	(supports instrument2 infrared1)
	(calibration_target instrument2 groundstation2)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation0)
	(supports instrument3 spectrograph0)
	(supports instrument3 infrared1)
	(calibration_target instrument3 groundstation0)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation2)
)
(:goal (and
	(pointing satellite1 groundstation2)
	(pointing satellite3 star1)
	(have_image planet3 infrared1)
	(have_image star4 infrared2)
	(have_image star5 spectrograph0)
	(have_image phenomenon6 spectrograph0)
	(have_image star7 spectrograph0)
))

)

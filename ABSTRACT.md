Research on autonomous vehicles has been a key focus in recent years, leading to the rise of increasingly autonomous vehicles operating on roadways. For example, in 2019 it was reported that over 1,400 roadway autonomous vehicles across over [80 companies were in the testing stages](https://techcrunch.com/2019/06/11/over-1400-self-driving-vehicles-are-now-in-testing-by-80-companies-across-the-u-s/) in the U.S. alone. However, it is also crucial that researchers explore autonomous vehicles in off-road environments. The passenger-carrying autonomous vehicle industry eventually seeks to achieve ”Level 5” autonomy, which enables entirely [autonomous operation in all conditions](https://www.nhtsa.gov/technology-innovation/automated-vehicles). Therefore, if a vehicle ends up in an unexpected situation or on a route containing unmarked or unpaved terrain, the vehicle should be equipped to traverse it safely.

Authors research provides an extensive **Off-Road Terrain** dataset including over 12,000 images from a monocular camera and sensor readings from a GPS, IMUs, and a wheel rotation speed sensor. Authors also derive eight potential measures of terrain roughness from the IMU z-axis acceleration readings that can be used to label images and evaluate their effectiveness.

This section first describes the following three challenges involved in preparing an off-road terrain dataset:

- Lack of relevant off-road terrain data. Data collection at scale for roadway autonomous vehicles is relatively feasible due to the vast network of roads on which humans driving vehicles equipped with sensors can travel to collect data. In contrast, there is a much smaller network of relevant off-road drivable terrain.

- Traversing rough off-road terrain can cause an unsteady camera, which yields images where any drivable terrain ahead is not clearly visible. Moreover, trees surround most of the drivable portions of off-road terrain. Images are therefore susceptible to poor lighting and uneven sunlight that may obstruct the image view.

- Labeling images of upcoming drivable terrain with a single quantative roughness metric derived from IMU z-axis acceleration readings is hard because the length of terrain visible in an image may be unknown. As a result, determining the z-axis acceleration readings corresponding to the upcoming drivable terrain in the image is challenging. Validating that a given roughness metric effectively labels the images in the dataset is also hard because a human may not have intuitive insight as to how the vehicle’s motion will be affected by traversing this terrain, even though certain visual cues may be indicative of terrain roughness.

The Off-Road Terrain data was collected in Percy Warner Park in Nashville, Tennessee, USA via a mountain bike equipped with the following sensors: dual GPS receivers (Garmin 830), dual-high resolution IMU’s (Garmin Virb Ultra), a 4k 30fps camera time synchronized to both accelerometers (Garmin Virb Ultra), and a wheel rotation speed sensor (Garmin Bike Speed Sensor 2). Data was collected on five different dates between late July and early October 2020.

The dataset contains two forms of data: sensor data and image frames extracted from video data. The videos were taken by a single monocular camera attached to the bike’s handlebars. Image frames were extracted at one second intervals to minimize overlap between frames. The frame rate of authors camera was ∼29.97 frames per second. It therefore was not possible to extract image frames at exactly one second intervals, so instead authors found the image frame most closely corresponding to each second interval.

Image frames are named by their UTC timestamps in seconds and milliseconds (e.g., “1000s100ms”). Authors generated 12,982 images over nearly 44 miles of off-road terrain. Authors then excluded all images containing sensitive information (e.g., pictures of other bikers and license plates) and images taken before or after the bike traveled the off-road trail, resulting in 12,730 images included in authors public dataset.

These images are not filtered by whether they contain a path, optimal lighting, or sufficient visible terrain for terrain learning so that researchers have access to the entire range of images collected by the vehicle. The size of each image is 3,840 x 2,160 pixels. Sensor data is store in a format called a “fit file.” Authors converted fit files to comma-separated-value (CSV) files using tools provided by [Garmin](https://developer.garmin.com/fit/fitcsvtool/). Authors then formatted each CSV to a state-based representation where each row contains the readings at a single timestamp and add UTC timestamps to each reading so the data can be used alongside the image frames. This dataset contains the information described below:

1. Formatted sensor data. There is a folder for each data collection session with the following CSVs.
- accelerometer_calibrated split.csv which contains the calibrated and uncalibrated acceleration readings from the accelerometer, taken ∼10 ms apart.
- gyroscope_calibrated split.csv which contains the calibrated and uncalibrated readings from the gyroscope, taken ∼10 ms apart.
- magnetometer_split.csv, which contains the uncalibrated magnetometer readings.
- gps.csv, which contains the vehicle’s latitute, longitude, altitude, speed, heading, and velocity, taken ∼100 ms apart.
- record.csv, which contains the vehicle’s latitude, longitude, distance traveled, speed, and altitude, taken 1 second apart.

2. Roughness labels for images. CSVs of the eight potential roughness labels for the subset of images valid for these labeling schemas are included, as described in Section V in source.
- labels_tsm1.csv contains Labels 1–4.
- labels_tsm2.csv contians Labels 5–8.

The accelerometer, gyroscope, magnetometer, and GPS CSV files contain system timestamps that represent the relative time since the start of the data collection session, and calculated UTC timestamps. The GPS CSV file also contains a UTC timestamp recorded by the sensor, which may not always align with the calculated UTC timestamp due to sensor lags at certain parts in the forest. Calibrated readings correspond directly to the x-, y-, and z-axes and are in the conventionally understood units. Authors data did not contain the calibration factor necessary to calibrate the magnetometer CSV, meaning that the x-, y-, and z-axis readings may not correspond directly to these axes. The speed and velocity readings in the GPS CSV file are GPS estimates and are significantly less accurate than the speed readings in the record CSV file, which are recorded from the wheel rotation speed sensor.

## Roughness Metric

Many studies have used [z-axis acceleration to examine terrain roughness](https://www.ri.cmu.edu/publications/semantic-segmentation-for-terrain-roughness-estimation-using-data-autolabeled-with-a-custom-roughness-metric/). This measure provides insight about how the vehicle’s motion will be affected b traversing the upcoming terrain. Although [Stavens et al.](https://arxiv.org/abs/1206.6872) standardized their measure of roughness by speed, authors used a different approach with their roughness metrics since their data did not exhibit a linear relationship between z-axis acceleration and speed, likely because the speeds of their vehicle (i.e., a bicycle) were significantly slower than the vehicle (i.e., a car) used by Stavens et al. Their roughness metric takes the standard deviation of a 1 second window of z-axis acceleration readings. This metric is a comprehensive measure of the terrain in the sample and is stable when the sample’s mean is nonzero (such as traveling down a hill with increasing acceleration). While authors samples could reflect between 1–7 meters since the vehicle’s speed was typically between 1–7 m/s, a standard sample size was important to avoid certain samples being more susceptible to outliers than others.

Authors then determined which 1-second window of z-axis acceleration readings should be used to label each image. The bike traveled along particularly rough terrain, causing the angle and position of the camera to vary. The amount of upcoming terrain and its distance from the vehicle was therefore not constant across all images. For this reason, they decided to examine two terrain sampling approaches:

1. Terrain Sampling Method 1 (TSM 1), which used a 1 second sampling of z-axis acceleration readings centered around the timestamp corresponding to 5 meters ahead of the image.
2. Terrain Sampling Method 2 (TSM 2), which used a 1 second sampling of z-axis acceleration readings directly ahead of the image’s timestamp.

Authors discretized the continuous roughness metric using each of four methods: data visualization (examining the data distribution and z-axis acceleration readings alongside the continuous roughness metric), k-means clustering with k = 2, k-means clustering with k = 3, and k-means clustering with k = 4. These methods will be referred to as original groups, k = 2 groups, k = 3 groups, and k = 4 groups, respectively. In calculating the 1 second sample for TSM 1, only 0.99 seconds of readings were included.

## Labeling Images

Each image was assigned eight labels, one for each possible
combination of the two methods of sampling the terrain and
the four methods of discretizing the roughness metric:
1. Label 1: TSM 1, original groups.
2. Label 2: TSM 1, k = 2 groups.
3. Label 3: TSM 1, k = 3 groups.
4. Label 4: TSM 1, k = 4 groups.
5. Label 5: TSM 2, original groups.
6. Label 6: TSM 2, k = 2 groups.
7. Label 7: TSM 2, k = 3 groups.
8. Label 8: TSM 2, k = 4 groups.

Authors filtered the 12,982 images in their dataset based on sensor and visual criteria, which resulted in 7,070 images valid for Labels 1–4. To compare Labels 1–4 and Labels 5–8, authors filtered the images valid for Labels 5–8 to include only images also valid for Labels 1–4, resulting in 7,061 images valid for Labels 5–8. The labeling CSVs included in the dataset do not contain two of the images used in this experiment since these images included other bikers.

Authors performed sensor validation to confirm that the sensor readings either 5 meters or 3 seconds ahead of each image met the following criteria: the vehicle should not be stopped, sensor readings should be continuous, and the calculated UTC timestamp should be within 1 second of the reported UTC timestamp. In sensor validation for Labels 1–4, they included the third criterion and GPS continuity in case other sensor readings were also affected. Authors did not consider these criteria for Labels 5–8 because significantly less sensor data was used to calculate these labels.

<table>
  <tr>
    <th></th>
    <th colspan="2">TSM1</th>
    <th colspan="2">TSM2</th>
    <th colspan="2">Difference (TSM2-TSM1)</th>
  </tr>
  <tr>
    <th></th>
    <th>Overall accuracy</th>
    <th>Avg class accuracy</th>
    <th>Overall accuracy</th>
    <th>Avg class accuracy</th>
    <th>Overall accuracy</th>
    <th>Avg class accuracy</th>
  </tr>
  <tr>
    <td>Original groups</td>
    <td>34.75%</td>
    <td>36.48%</td>
    <td>45.48%</td>
    <td>47.72%</td>
    <td>10.73%</td>
    <td>11.24%</td>
  </tr>
  <tr>
    <td>k = 2 groups</td>
    <td>71.19%</td>
    <td>71.33%</td>
    <td>73.45%</td>
    <td>75.06%</td>
    <td>2.26%</td>
    <td>3.73%</td>
  </tr>
  <tr>
    <td>k = 3 groups</td>
    <td>55.65%</td>
    <td>46.20%</td>
    <td>60.17%</td>
    <td>52.30%</td>
    <td>4.52%</td>
    <td>6.10%</td>
  </tr>
  <tr>
    <td>k = 4 groups</td>
    <td>45.76%</td>
    <td>35.72%</td>
    <td>50.00%</td>
    <td>46.27%</td>
    <td>4.24%</td>
    <td>10.55%</td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td><b>Average</b></td>
    <td>5.44%</td>
    <td>7.91%</td>
  </tr>
</table>

<i>Selection set performance of labeling schemas</i>

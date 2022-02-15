# Twist-n-Sync. Time synchronization algorithm that employs IMU gyroscope data

Imagine that you want to synchronize [two smartphones](https://www.mdpi.com/1424-8220/21/1/68)<sup>1</sup> for stereoscopic (or multiscopic) photo or video shutting with _microseconds accuracy and precision_.
Or you need to synchronize Azure Kinect DK [depth frames](https://arxiv.org/abs/2111.03552)<sup>2</sup> with smartphone frames.

Twist-n-Sync is a time synchronization algorithm that can solve the time sync issues by employing gyroscope chips widely available in millions of comsumer gadgets.

Another benefical usage of the package is synchronization of diverse motion capture (mocap) systems (OptiTrack, Vicon) that provide ground truth data for robot navigation and state estimation algorithms (Wheeled, Visual, Visual-Inertial Odometry and SLAM).

## Installation

`pip install twistnsync`

## Usage examples

WIP: The python notebook examples in [`examples`](https://github.com/MobileRoboticsSkoltech/twistnsync-python/examples) folder provide comprehensive mini-tutorials how to use the code:
- [two systems sync by gyroscope data](https://github.com/MobileRoboticsSkoltech/twistnsync-python/blob/master/examples/Smartphone_and_MCU-board_data_sync.ipynb);
- TODO mocap data (position orientation) and robot data sync;
- TODO clock drift evaluation of two independent systems;

## References
In case of usage of the materials, please, refer to the source and/or publications:

<sup>1</sup>
```
@article{faizullin2021twist,
  title={Twist-n-Sync: Software Clock Synchronization with Microseconds Accuracy Using MEMS-Gyroscopes},
  author={Faizullin, Marsel and Kornilova, Anastasiia and Akhmetyanov, Azat and Ferrer, Gonzalo},
  journal={Sensors},
  volume={21},
  number={1},
  pages={68},
  year={2021},
  publisher={Multidisciplinary Digital Publishing Institute}
}
```

<sup>2</sup>
```
@ARTICLE{9709778,
  author={Faizullin, Marsel and Kornilova, Anastasiia and Akhmetyanov, Azat and Pakulev, Konstantin and Sadkov, Andrey and Ferrer, Gonzalo},
  journal={IEEE Sensors Journal}, 
  title={SmartDepthSync: Open Source Synchronized Video Recording System of Smartphone RGB and Depth Camera Range Image Frames with Sub-millisecond Precision}, 
  year={2022},
  volume={},
  number={},
  pages={1-1},
  doi={10.1109/JSEN.2022.3150973}
}
```

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.

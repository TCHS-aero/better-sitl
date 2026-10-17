# Better SITL

## Table of contents:

| Categories    | What's shown?|
| ------------- |:-------------:|
| [Overview](#over) | Project Overview. |
| [Setup](#set) | Setup/Installation instructions. |
| [Usage](#use) | How to use this program. |
| [Used Resources](#res) | All resources used in this repo. |

<a name="over">

### Overview
In Aero, we use drone simulations a lot; especially with PX4. However, simulations are encumbersome to setup, and even more difficult to manage. PX4 makes docker images for their simulation environments, which does make things easier, but even their scripts to run them easily aren't very robust. As a solution, we at Aero developed a convenient CLI that makes things far easier to manage.

<a name="set">

### Setup

#### Prerequisites
- Docker Desktop or Docker Engine
- Active Docker Daemon
- Sudo privileges (Linux and MacOS)
  
#### How To Install Docker
All docker installation directions can be found [here](https://docs.docker.com/desktop/). However, there are some important things to note.

> [!CAUTION]
> Docker Desktop is available on brew by using `brew install --cask docker`. However, installation this way requires the Docker Daemon to be installed seperately, as it is not supported on MacOS. A community project named `Colima` can be used as a replacement. This may be the preferred method for many developers.

```zsh
brew install colima
colima start
```

> [!IMPORTANT]
> If you encounter credential errors on MacOS, edit `$HOME/.docker/config.json` and change `"credsStore": "desktop"` to `"credsStore": "osxkeychain"`.

#### Installation
1. Clone this repository
```bash
git clone https://github.com/TCHS-aero/better-sitl.git
```
2. Install with pip
```bash
pip install better-sitl
```

<a name="use">

### Usage
Manage PX4 Docker images with `sitl image`
```plaintext
Usage: sitl image [OPTIONS] COMMAND [ARGS]...

  Handle installed Docker images.

Options:
  --help  Show this message and exit.

Commands:
  list    List installed PX4 Docker images.
  remove  Remove installed PX4 docker images.
```

Run PX4 Docker images; either Gazebo or SIH.
```plaintext
Usage: sitl run gazebo [OPTIONS]

  Launch PX4 SITL using Gazebo.

Options:
  --world [default|aruco|baylands|lawn|ridge|rover|walls|windy|moving_platform]
                                  World to load.  [required]
  --env KEY=VALUE                 Pass an extra environment variable. Repeat
                                  to add more.
  --model [TEXT]                  Vehicle model to load.  [required]
  --help                          Show this message and exit.
```

Gazebo and SIH have different models that can be ran through the simulation.

#### Gazebo:
1. gz_x500
2. gz_x500_vision
3. gz_x500_depth
4. gz_x500_mono_cam
5. gz_x500_mono_cam_down
6. gz_x500_mono_lidar_down
7. gz_x500_mono_lidar_front
8. gz_x500_mono_lidar_2d
9. gz_x500_gimbal
10. gz_rc_cessna
11. gz_advanced_plane
12. gz_standard_vtol
13. gz_quadtailsitter
14. gz_tiltrotor
15. gz_rover_differential
16. gz_rover_ackerman
17. gz_rover_mecanum

#### SIH:
1. sihsim_quadx
2. sihsim_hex
3. sihsim_airplane
4. sihsim_xvert
5. sihsim_standard_vtol
6. sihsim_rover_ackermann

<a name="res">

## Resources
* [PX4 Prebuilt Packages](https://docs.px4.io/main/en/simulation/px4_sitl_prebuilt_packages)
* [Gazebo Harmonic Vehicles](https://docs.px4.io/main/en/sim_gazebo_gz/vehicles)
* [SIH Simulation Details](https://docs.px4.io/main/en/sim_sih/index)
* [Click](https://click.palletsprojects.com/en/stable/)

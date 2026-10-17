from os import name
from subprocess import DEVNULL, run

import click

GZ_MODELS = [
    "gz_x500",
    "gz_x500_vision",
    "gz_x500_depth",
    "gz_x500_mono_cam",
    "gz_x500_mono_cam_down",
    "gz_x500_mono_lidar_down",
    "gz_x500_mono_lidar_front",
    "gz_x500_mono_lidar_2d",
    "gz_x500_gimbal",
    "gz_rc_cessna",
    "gz_advanced_plane",
    "gz_standard_vtol",
    "gz_quadtailsitter",
    "gz_tiltrotor",
    "gz_rover_differential",
    "gz_rover_ackerman",
    "gz_rover_mecanum",
]

SIH_MODELS = [
    "sihsim_quadx",
    "sihsim_hex",
    "sihsim_airplane",
    "sihsim_xvert",
    "sihsim_standard_vtol",
    "sihsim_rover_ackermann",
]

WORLDS = [
    "default",
    "aruco",
    "baylands",
    "lawn",
    "ridge",
    "rover",
    "walls",
    "windy",
    "moving_platform",
]


@click.group()
def cli():
    """Launch PX4 SITL simulators in Docker."""


@cli.group()
def image():
    """Handle installed images in Docker."""


def launch(
    simulator: str,
    world: str,
    model: str,
    env_vars: tuple[str, ...],
) -> None:
    """Run a PX4 SITL Docker image with the selected configuration.

    Args:
        simulator: Simulator backend, such as ``"sih"`` or ``"gazebo"``.
        world: World or environment to load.
        model: Vehicle model to load.
        env_vars: Extra environment variables in ``KEY=VALUE`` format.
    """
    env_array = list(env_vars)

    click.echo()
    click.echo(f"Simulator: {"sih" if not simulator else simulator}")
    click.echo(f"World: {world}")
    click.echo(f"Model: {model}")
    click.echo(f"Environment variables: {env_array}")

    command = [
        "docker",
        "run",
        "--rm",
        "-it",
        "--network",
        "host",
        "-e",
        f"PX4_GZ_WORLD={world}",
        "-e",
        f"PX4_SIM_MODEL={model}",
        "-e",
        "HEADLESS=1",
    ]

    if name != "nt":
        command.insert(0, "sudo")

    for var in env_array:
        command.append("-e")
        command.append(var)

    command.append(f"px4io/px4-sitl{"-gazebo" if simulator == "gazebo" else ""}:latest")

    click.echo(f"Running command: {" ".join(command)}")
    click.echo()

    run(command)


def simulator_options(function):
    """Add options shared by simulator commands."""

    function = click.option(
        "--env",
        "env_vars",
        multiple=True,
        metavar="KEY=VALUE",
        help="Pass an extra environment variable. Repeat to add more.",
    )(function)

    function = click.option(
        "--world",
        required=True,
        help="World to load.",
        type=click.Choice(WORLDS),
    )(function)
    return function


@cli.command(
    epilog=f"Available Models: {" ".join([f"{model}" for model in SIH_MODELS])}"
)
@simulator_options
@click.option(
    "--model",
    required=True,
    help="Vehicle model to load.",
    type=click.Choice(SIH_MODELS),
    show_choices=False,
)
def sih(world: str, model: str, env_vars: tuple[str, ...]) -> None:
    """Launch PX4 SITL using the SIH simulator."""
    launch("str", world, model, env_vars)


@cli.command(
    epilog=f"Available Models: {" ".join([f"{model}" for model in GZ_MODELS])}"
)
@simulator_options
@click.option(
    "--model",
    required=True,
    help="Vehicle model to load.",
    type=click.Choice(GZ_MODELS),
    show_choices=False,
)
def gazebo(world: str, model: str, env_vars: tuple[str, ...]) -> None:
    """Launch PX4 SITL using Gazebo."""
    launch("gazebo", world, model, env_vars)


def _verify_docker_install():
    try:
        result = run(["docker"], stdout=DEVNULL, stderr=DEVNULL)
    except FileNotFoundError:
        print(
            "Docker is not installed in your system.\nPlease visit https://docs.docker.com/ and installing either Docker Engine or Docker Desktop.\nFor Arch-Based distrobutions of linux, Docker Engine can be installed through pacman."
        )

        raise SystemExit(1)


def main():
    try:
        _verify_docker_install()
        cli()
    except KeyboardInterrupt:
        print("\n-- Interrupted.")
        raise SystemExit(130)


if __name__ == "__main__":
    main()

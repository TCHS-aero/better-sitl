from os import name
from shutil import which
from subprocess import run

import click

IMAGE_REFS = {
    "gazebo": "px4io/px4-sitl-gazebo:latest",
    "sih": "px4io/px4-sitl:latest",
}

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


def docker_command(*args: str) -> list[str]:
    """Build a Docker command, using sudo on non-Windows systems."""
    prefix = ["sudo"] if name != "nt" else []
    return [*prefix, "docker", *args]


@click.group()
def cli():
    pass


@cli.group(name="run")
def exec():
    """Launch PX4 SITL simulators in Docker."""


@cli.group()
def image():
    """Handle installed Docker images."""


@image.command(name="list", help="List installed PX4 Docker images.")
def list_images() -> None:
    result = run(
        docker_command(
            "image",
            "ls",
            "--filter",
            "reference=px4io/*",
            "--format",
            "{{.Repository}}:{{.Tag}}",
        ),
        capture_output=True,
        text=True,
        check=True,
    )

    installed_refs = set(result.stdout.splitlines())
    installed_names = [
        short_name
        for short_name, image_ref in IMAGE_REFS.items()
        if image_ref in installed_refs
    ]

    if not installed_names:
        click.echo("You currently have no supported PX4 images installed.")
        return

    names = " and ".join(f'"{short_name}"' for short_name in installed_names)
    plural = len(installed_names) > 1

    click.echo(
        f"You currently have the {names} image{'s' if plural else ''} installed."
    )
    click.echo(
        f"To remove {'them' if plural else 'it'}, use "
        f"{' or '.join(f'--image {name}' for name in installed_names)} "
        "with the image remove command."
    )


@image.command()
@click.option(
    "--image",
    "images",
    multiple=True,
    required=True,
    type=click.Choice(tuple(IMAGE_REFS)),
    help="PX4 image to remove. Repeat this option to remove multiple images.",
)
def remove(images: tuple[str, ...]) -> None:
    image_refs = [IMAGE_REFS[short_name] for short_name in images]

    run(
        docker_command("image", "rm", *image_refs),
        check=True,
    )


def launch(
    simulator: str,
    world: str,
    model: str,
    env_vars: tuple[str, ...],
) -> None:
    """Run a PX4 SITL Docker image with the selected configuration."""
    image_ref = IMAGE_REFS[simulator]

    click.echo(f"Simulator: {simulator}")
    click.echo(f"World: {world}")
    click.echo(f"Model: {model}")
    click.echo(f"Environment variables: {list(env_vars)}")

    command = docker_command(
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
    )

    for env_var in env_vars:
        command.extend(["-e", env_var])

    command.append(image_ref)

    click.echo(f"Running command: {' '.join(command)}")
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

    return click.option(
        "--world",
        required=True,
        type=click.Choice(WORLDS),
        help="World to load.",
    )(function)


@exec.command()
@simulator_options
@click.option(
    "--model",
    required=True,
    type=click.Choice(SIH_MODELS),
    show_choices=False,
    help="Vehicle model to load.",
)
def sih(world: str, model: str, env_vars: tuple[str, ...]) -> None:
    """Launch PX4 SITL using the SIH simulator."""
    launch("sih", world, model, env_vars)


@exec.command()
@simulator_options
@click.option(
    "--model",
    required=True,
    type=click.Choice(GZ_MODELS),
    show_choices=False,
    help="Vehicle model to load.",
)
def gazebo(world: str, model: str, env_vars: tuple[str, ...]) -> None:
    """Launch PX4 SITL using Gazebo."""
    launch("gazebo", world, model, env_vars)


def main() -> None:
    if which("docker") is None:
        raise click.ClickException(
            "Docker is not installed or is not available on PATH."
        )

    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n-- Interrupted.")
        raise SystemExit(130)


if __name__ == "__main__":
    main()

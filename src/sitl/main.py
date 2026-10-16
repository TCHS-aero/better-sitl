import click


@click.group()
def cli():
    """Launch PX4 SITL simulators in Docker."""


def launch(
    simulator: str,
    world: str,
    model: str,
    env_vars: tuple[str, ...],
    headless: bool,
) -> None:
    """Run a PX4 SITL Docker image with the selected configuration.

    Args:
        simulator: Simulator backend, such as ``"sih"`` or ``"gazebo"``.
        world: World or environment to load.
        model: Vehicle model to load.
        env_vars: Extra environment variables in ``KEY=VALUE`` format.
        headless: Whether to run without a graphical interface.
    """
    env_array = list(env_vars)

    click.echo(f"Simulator: {simulator}")
    click.echo(f"World: {world}")
    click.echo(f"Model: {model}")
    click.echo(f"Environment variables: {env_array}")
    click.echo(f"Headless: {headless}")


def simulator_options(function):
    """Add options shared by simulator commands."""
    function = click.option(
        "--headless",
        is_flag=True,
        default=False,
        help="Run without a graphical interface.",
    )(function)
    function = click.option(
        "--env",
        "env_vars",
        multiple=True,
        metavar="KEY=VALUE",
        help="Pass an extra environment variable. Repeat to add more.",
    )(function)
    function = click.option("--model", required=True, help="Vehicle model to load.")(
        function
    )
    function = click.option("--world", required=True, help="World to load.")(function)
    return function


@cli.command()
@simulator_options
def sih(world: str, model: str, env_vars: tuple[str, ...], headless: bool) -> None:
    """Launch PX4 SITL using the SIH simulator."""
    launch("sih", world, model, env_vars, headless)


@cli.command()
@simulator_options
def gazebo(world: str, model: str, env_vars: tuple[str, ...], headless: bool) -> None:
    """Launch PX4 SITL using Gazebo."""
    launch("gazebo", world, model, env_vars, headless)


def main():
    try:
        cli()
    except KeyboardInterrupt:
        print("\n-- Interrupted.")
        raise SystemExit(130)


if __name__ == "__main__":
    main()

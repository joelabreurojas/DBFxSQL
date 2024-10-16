import click


class OrderCommands(click.Group):
    """Top-level command group for managing orders."""

    def list_commands(self, ctx: click.Context) -> list[str]:
        """Returns a list of available subcommands in the declared order."""

        return self.commands

import click

@click.group()
def cli():
    print("load the core settings")

@cli.command()
def init():
    print("set up campaign dirs")

@cli.command()
def describe():
    print("describe the configured game systems, or types")

@cli.command()
def session():
    print("create and open new session and plot files")

@cli.command()
def latest():
    print("open the most recent session and/or plot file")

@cli.command()
def settings():
    print("open the user or campaign settings.yaml files")

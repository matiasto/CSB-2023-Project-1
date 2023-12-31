from invoke import task


@task
def init(ctx):
    ctx.run("python3 init_db.py", pty=True)


@task
def start(ctx):
    ctx.run("python3 src/app.py", pty=True)


@task
def lint(ctx):
    ctx.run("pylint src", pty=True)


@task
def format(ctx):  # pylint: disable=redefined-builtin
    ctx.run("autopep8 --in-place --recursive src", pty=True)

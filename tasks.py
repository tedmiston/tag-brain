from invoke import task

@task
def lint(ctx):
    ctx.run('pycodestyle .')

@task
def test(ctx):
    ctx.run('nose2')

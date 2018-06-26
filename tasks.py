from invoke import task

@task
def test(c, docs=False):
    c.run('python -m pytest')

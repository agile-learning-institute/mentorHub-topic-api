import click
import subprocess
import signal
import sys


commands = {
        'blackbox': 'docker run --rm --network mentorhub_default -e STEPCI_DISABLE_ANALYTICS=1 -v "$PWD"/test:/tests --mount "type=bind,src=$PWD/docs,dst=/docs" ghcr.io/stepci/stepci tests/topic.stepci.yaml',
        'build': 'docker build --rm --tag ghcr.io/agile-learning-institute/mentorhub-topic-api:latest .',
        'start': "CONNECTION_STRING='mongodb://root:example@localhost:27017/?tls=false&directConnection=true' ./.venv/bin/python3 src/app/wsgi.py",
        'stepci': 'docker run --rm --network bridge -e STEPCI_DISABLE_ANALYTICS=1 -v "$PWD"/test:/tests --mount "type=bind,src=$PWD/docs,dst=/docs" ghcr.io/stepci/stepci tests/topic.stepci.yaml'
}


@click.group()
@click.option('--mh', default='mh', metavar='PATH', help='Path to the mh script')
@click.pass_context
def cli(ctx, mh):
    ctx.obj = mh


@cli.command()
@click.pass_obj
def container(mh):

    subprocess.run([mh,'up','topic-api'])


@cli.command()
@click.pass_obj
def blackbox(mh):

    container = subprocess.run([mh,'up','topic-api'])

    if container.returncode == 0:
        subprocess.run(commands['blackbox'], shell=True)

    subprocess.run([mh,'down'])


@cli.command()
def build():
    subprocess.run(commands['build'], shell=True)


@cli.command()
@click.pass_obj
def start(mh):

    def signal_handler(signum, frame):
        signal.signal(signum, signal.SIG_IGN)
        subprocess.run([mh,'down'])
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    subprocess.run([mh,'up','mongodb'])

    subprocess.run(commands['start'], shell=True)


@cli.command()
def stepci():

    subprocess.run(commands['stepci'], shell=True)


if __name__ == '__main__':
    cli()

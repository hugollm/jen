from .cli import CliApp

from .run import Run
from .build import Build


app = CliApp()
app.command(Run())
app.command(Build())

if __name__ == '__main__':
    app.call()

from .cli import CliApp

from .server import Server
from .build import Build


app = CliApp()
app.command(Server())
app.command(Build())

if __name__ == '__main__':
    app.call()

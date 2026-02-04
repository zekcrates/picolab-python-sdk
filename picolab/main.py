import typer
from rich.console import Console
from . import auth 
from . import client

app = typer.Typer()
console = Console()

@app.command()
def login(key: str = typer.Option(..., prompt=True, hide_input=True)):
    """Login securely."""
    console.print("[yellow] Authenticating...[/yellow]")
    auth.save_key(key)
    console.print("[green] Success! Key saved.[/green]")

@app.command()
def get(project_name: str):
    """Download a starter project."""
    console.print(f"[cyan]⬇ Fetching {project_name}...[/cyan]")
    
    success, message = client.create_starter_project(project_name)
    
    if success:
        console.print(f"[green] Created:[/green] {message}")
        console.print(f"Run: [bold]cd {project_name}[/bold]")
    else:
        console.print(f"[red] Error:[/red] {message}")

@app.command()
def push():
    """Deploy your code."""
    try:
        key = auth.get_key_or_fail()
    except FileNotFoundError:
        console.print("[red] Not logged in.[/red] Run 'picolab login'.")
        return

    console.print("[yellow] Packaging and uploading...[/yellow]")
    try:
        response = client.upload_project(key)

    except Exception as e:
        console.print(f"[red] Connection failed:[/red] {e}")


def main():
    app()

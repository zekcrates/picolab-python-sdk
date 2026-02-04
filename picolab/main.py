import typer
from rich.console import Console
from . import auth 
from . import client

app = typer.Typer()
console = Console()


@app.command()
def login(key: str = typer.Option(..., prompt=True, hide_input=True)):
    """
    Authenticate securely. Verifies the key with the server first.
    """
    console.print("[yellow] Authenticating...[/yellow]")
    
    is_valid, message = client.verify_key(key)
    
    if is_valid:
        auth.save_key(key)
        console.print(f"[bold green] Success![/bold green] Logged in as [cyan]{message}[/cyan]")
        console.print(f"[dim]Credentials saved to: {auth.CONFIG_FILE}[/dim]")
    else:
        console.print(f"[bold red]❌ Login Failed:[/bold red] {message}")
        console.print("Please check your key and try again.")
        raise typer.Exit(code=1)
@app.command()
def get(project_name: str):
    """Download a project from the Picolab Server."""
    try:
        key = auth.get_key_or_fail()
    except Exception:
        console.print("[red] Not logged in.[/red] Run 'picolab login' first.")
        return
    console.print(f"[cyan]⬇  Fetching {project_name}...[/cyan]")
    
    success, message = client.download_starter_project(project_name, key)
    
    if success:
        console.print(f"[bold green] Success![/bold green]")
        console.print(message)
        console.print(f"\n Next step: [bold white]cd {project_name}[/bold white]")
    else:
        console.print(f"[bold red] Error:[/bold red] {message}")
@app.command()
def push():
    """Deploy your code."""
    try:
        key = auth.get_key_or_fail()
    except FileNotFoundError:
        console.print("[red] Not logged in.[/red] Run 'picolab login'.")
        return

    console.print("[yellow] Packaging and uploading...[/yellow]")
    
    result = client.upload_project(key)
    
    if result["success"]:
        console.print("[green] BUILD PASSED[/green]")
        
        server_response = result.get("data", {})
        console.print(server_response.get("message", "Upload successful."))
        
    else:
        console.print(f"[red]❌ Failed:[/red] {result['message']}")

def main():
    app()

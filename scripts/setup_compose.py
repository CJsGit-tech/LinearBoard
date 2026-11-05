"""Create the local Compose password once; never rotate existing credentials."""
from pathlib import Path
import secrets
root=Path(__file__).resolve().parents[1]/'data/docker'
root.mkdir(parents=True,exist_ok=True)
root.chmod(0o700)
password=root/'database-password'
if not password.exists():
    with password.open('x') as file:
        file.write(secrets.token_urlsafe(40))
# The containing directory is owner-only; mounted files must be readable by
# the non-root database and application users inside their containers.
password.chmod(0o644)
print('Compose secret ready; existing password preserved')

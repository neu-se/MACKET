pycodestyle --exclude venv . \
&& isort --check --diff --skip venv . \
&& pyright

# Install pygame if not installed
if [[ ! -f "./venv" ]]; then
    echo "Installing pygame"
    python -m venv venv
    ./venv/bin/python -m pip install pygame
fi

source ./venv/bin/activate
python -m tictactoe

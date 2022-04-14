//create virtual environment
python3 -m venv ~/goinfre/env #(in windows: python -m venv env)

ln -s ~/goinfre/env env #(in windows: nothing)

source ./env/bin/activate #(in windows: env/bin/activate.bat)


//install librares
pip install --upgrade pip

pip install pygame

pip install numpy

pip install PyOpenGL

pip install PyGLM

pip install --upgrade Pillow


//start program
python3 main.py #(in windows: python main.py)


//actions: move - WASD, up - Z, down - Q, rotate - press left mouse button and move mouse
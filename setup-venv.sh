PYTHON_EXECUTABLE=python3.9

if ! $PYTHON_EXECUTABLE --version; then
  echo "$PYTHON_EXECUTABLE is needed"
  exit 1
fi

# create virtualenv
$PYTHON_EXECUTABLE -m venv venv
if [ $? -ne 0 ]; then
  echo 'Creation of virtualenv failed'
  exit 1
fi

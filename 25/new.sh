# takes 1 input arg e.g. "10"
# creates a new python file with the name of the input arg
if [ -z "$1" ]; then
  echo "Error: No input argument provided. Please provide the new day number"
  exit 1
fi
# check if "$1.py" already exists
if [ -e "day$1.py" ]; then
  echo "Error: The file 'day$1.py' already exists."
  exit 1
fi

cp Day00.py "day$1.py"
git add "day$1.py"
touch data/day$1.txt
touch data/day$1_test.txt

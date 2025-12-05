# takes 1 input arg e.g. "10"
# creates a new python file with the name of the input arg
if [ -z "$1" ]; then
  echo "Error: No input argument provided. Please provide the new day number"
  exit 1
fi
# check if "$1.py" already exists
if [ -e "Day$1.py" ]; then
  echo "Error: The file 'Day$1.py' already exists."
  exit 1
fi

cp Day00.py "Day$1.py"
touch ../data/Day$1.txt
touch ../data/Day$1_test.txt

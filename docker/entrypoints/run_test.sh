#!/usr/bin/env bash
set -e

trap error_handler ERR

# pretty colours
SET_BLACK_TEXT="\e[30m"
SET_YELLOW_TEXT="\e[33m"
SET_RED_BACKGROUND="\e[101m"
SET_ERROR_TEXT="$SET_BLACK_TEXT$SET_RED_BACKGROUND"
RESET_FORMATTING="\e[0m"
ERROR_PREFIX="${SET_ERROR_TEXT}ERROR: ${RESET_FORMATTING}"

error_handler() {
  exitcode=$?
  echo -e "$SET_ERROR_TEXT $BASH_COMMAND failed!!! ❌ $RESET_FORMATTING"
  # Some more clean up code can be added here before exiting
  exit $exitcode
}

# Default values
BACKEND_DIR="/app/backend"

# Declare the arrays
declare -a ALL_STEPS
declare -a LINT_STEPS
declare -a TEST_STEPS
# Declare the associative array
declare -A STEP_EXTRA_ARGUMENTS

function usage() {
  echo "usage: entrypoint.sh <service_name> [--all] [--run|--skip {step} <extra_args>] [--skip-coverage] [--run-coverage]"
  echo ""
  echo "  <service_name>    : The name of the service or library (e.g., globdoc, specter)"
  echo ""
  echo "Valid steps: {${ALL_STEPS[*]}}"
  echo ""
  echo "Options:"
  echo "  --all             : Run both the unit test and linting suites"
  echo "  --lint            : Run the full linting suite."
  echo "  --unit-test       : Run the full unit test suite."
  echo "  --skip-coverage   : Skip pytest coverage."
  echo "  --run-coverage    : Run pytest with coverage."
  echo "  --run/--skip      : Specify a specific check to run/skip. --run optionally accepts extra"
  echo "                      arguments that are passed to the step. This option can be used multiple times."
  echo "  -h | --help       : Display this help message"
  exit 1
}

# Check for service name as the first argument
if [ -z "$1" ]; then
  echo "${ERROR_PREFIX} Please provide a service name (e.g., globdoc, specter, subscription, usermod) ❌"
  usage
fi
SERVICE="$1"
shift # Remove the service name from the arguments list

# Stores all arguments passed to the script
SCRIPT_ARGS=("$@")

# Set options accepted by the CLI and all steps in the test suite.
VALID_CLI_OPTIONS=("--all" "--lint" "--unit-test" "--run" "--skip" "--skip-coverage" "--run-coverage" "--help" "-h")
LINT_STEPS=("bandit" "black" "flake8" "isort" "mypy")
TEST_STEPS=("pytest")
ALL_STEPS=("${TEST_STEPS[@]}" "${LINT_STEPS[@]}")

# Controls which steps will run as part of the test suite.
declare -A STEPS_ACTIVE_MAP
for step in "${ALL_STEPS[@]}"; do
  STEPS_ACTIVE_MAP["$step"]=true
done

# Declare the associative array for extra arguments.
declare -A STEP_EXTRA_ARGUMENTS
for step in "${ALL_STEPS[@]}"; do
  STEP_EXTRA_ARGUMENTS["$step"]=""
done

# Coverage specific flags
SKIP_COVERAGE="false"

####################################################################
# Determine if array contains value
####################################################################
array_contains() {
  local seeking=$1
  shift
  local in=1
  for element; do
    if [[ "$element" == "$seeking" ]]; then
      in=0
      break
    fi
  done
  return $in
}

####################################################################
# Sets extra arguments for a provided step
####################################################################
add_extra_arguments() {
    local step=$1
    shift # Remove the step name
    if ! array_contains "$step" "${ALL_STEPS[@]}"; then
        printf "%b The specified step %s is invalid. ❌\n" "${ERROR_PREFIX}" "$step"
        usage
    fi
    STEP_EXTRA_ARGUMENTS["$step"]="$*"
}

####################################################################
# Toggles a step between on (will run) and off (won't run)
####################################################################
toggle_step() {
  local action=$1
  shift
  if [[ "$action" != "on" ]] && [[ "$action" != "off" ]]; then
    echo "Specified invalid step $step. Choose between on and off. ❌"
    exit 1
  fi
  for step in "$@"; do # Iterate over the provided steps
    if ! array_contains "$step" "${ALL_STEPS[@]}"; then
      printf "%b The specified step %s is invalid. ❌\n" "${ERROR_PREFIX}" "$step"
      usage
    fi
    if [[ "$action" == "on" ]]; then
      STEPS_ACTIVE_MAP["$step"]=true
    else
      STEPS_ACTIVE_MAP["$step"]=false
    fi
  done
}

###############################################
# Parse CLI flags and set variables accordingly
###############################################
function handle_input() {
    # Default to running all steps if no specific options are given
    if [[ $# -eq 0 ]]; then
        toggle_step "on" "${ALL_STEPS[@]}"
        return
    fi

    local run_steps=()  # Array to store steps specified with --run

    while [[ $# -gt 0 ]]; do
        arg="$1"

        case "$arg" in
            --all)
                toggle_step "on" "${ALL_STEPS[@]}"
                shift
                ;;
            --run)
                shift  # Consume --run
                if [[ $# -eq 0 ]]; then
                    echo "${ERROR_PREFIX} --run requires a step name. ❌"
                    usage
                fi
                step="$1"
                if ! array_contains "$step" "${ALL_STEPS[@]}"; then
                    printf "%b The specified step %s is invalid. ❌\n" "${ERROR_PREFIX}" "$step"
                    usage
                fi
                run_steps+=("$step")
                shift  # Consume step name

                extra_args=()
                while [[ $# -gt 0 ]] && ! array_contains "$1" "${VALID_CLI_OPTIONS[@]}"; do
                    extra_args+=("$1")
                    shift
                done
                STEP_EXTRA_ARGUMENTS["$step"]=$(IFS=' '; echo "${extra_args[*]}")
                ;;
            --skip)
                shift  # Consume --skip
                if [[ $# -eq 0 ]]; then
                    echo "${ERROR_PREFIX} --skip requires a step name. ❌"
                    usage
                fi
                step="$1"
                if ! array_contains "$step" "${ALL_STEPS[@]}"; then
                    printf "%b The specified step %s is invalid. ❌\n" "${ERROR_PREFIX}" "$step"
                    usage
                fi
                toggle_step "off" "$step"
                shift  # Consume step name
                ;;
            --skip-coverage)
                SKIP_COVERAGE="true"
                shift
                ;;
            -h | --help)
                usage
                shift
                ;;
            *)
                echo "Unexpected argument: $arg ❌"
                usage
                shift
                ;;
        esac
    done

    # If --run is used, disable all steps first, then enable specified steps
    if [[ ${#run_steps[@]} -gt 0 ]]; then
        toggle_step "off" "${ALL_STEPS[@]}"
        toggle_step "on" "${run_steps[@]}"
    fi
}

###############################################
# Run active steps
###############################################
function run_steps() {

  echo "Starting test suite for service: $SERVICE 🚀"

  # Determine the service directory.
  if [[ -d "$BACKEND_DIR/services/$SERVICE" ]]; then
    SERVICE_DIR="$BACKEND_DIR/services/$SERVICE"
  elif [[ -d "$BACKEND_DIR/libs/$SERVICE" ]]; then
    SERVICE_DIR="$BACKEND_DIR/libs/$SERVICE"
  else
    echo -e "${ERROR_PREFIX} Service or library '$SERVICE' not found in services or libs directory. ❌"
    exit 1
  fi

  # Find the pyproject.toml file.
  PYPROJECT_DIR=$(dirname "$(find "$SERVICE_DIR" -name "pyproject.toml" | head -n 1)")
  if [ -z "$PYPROJECT_DIR" ]; then
    echo -e "${ERROR_PREFIX} pyproject.toml not found in $SERVICE_DIR ❌"
    exit 1
  fi

  # Copy config files
  echo "📂 Copying configuration files to $PYPROJECT_DIR"
  cp -r "$BACKEND_DIR/.bandit" "$PYPROJECT_DIR"
  cp -r "$BACKEND_DIR/.flake8" "$PYPROJECT_DIR"
  cp -r "$BACKEND_DIR/mypy.ini" "$PYPROJECT_DIR"
  cp -r "$BACKEND_DIR/pytest.ini" "$PYPROJECT_DIR"
  DEFAULT_COVERAGE_CONFIG="$BACKEND_DIR/.coveragerc"
  if [[ -f "$DEFAULT_COVERAGE_CONFIG" ]]; then
    cp -r "$DEFAULT_COVERAGE_CONFIG" "$PYPROJECT_DIR/.coveragerc"
  fi

  export PYTHONPATH=$PYTHONPATH:$PYPROJECT_DIR/src

  # Change to the service's directory.
  cd "$PYPROJECT_DIR"
  echo "Found pyproject.toml at: $PYPROJECT_DIR ✅"

  # Install dev dependencies
  echo "📦 Installing dependencies using Poetry..."
  if ! poetry install --with dev --no-root; then
    echo "❌ Error installing dependencies.
            This usually happens if the dockerfile doesnt have the correct user/permissions.
            Try adding the following to your Dockerfile:
            RUN chown -R \$USER:\$GROUP /app
            "
    exit 1
  fi

  # Define a cleanup function
  cleanup() {
    echo "🧹 Cleaning up configuration files from $PYPROJECT_DIR"
    rm -rf "$PYPROJECT_DIR/.bandit"
    rm -rf "$PYPROJECT_DIR/.flake8"
    rm -rf "$PYPROJECT_DIR/mypy.ini"
    rm -rf "$PYPROJECT_DIR/pytest.ini"
    rm -rf "$PYPROJECT_DIR/.coveragerc"
  }
  #set the cleanup function to run when the script exits.
  trap cleanup EXIT

  # Check which steps are active and run them.
  if [[ ${STEPS_ACTIVE_MAP[black]} == "true" ]]; then
    echo "Running black... 🧹"
    eval "poetry run black ${BLACK_ACTION} ${STEP_EXTRA_ARGUMENTS[black]} ."
  fi

  if [[ ${STEPS_ACTIVE_MAP[isort]} == "true" ]]; then
    echo "Running isort... 🧽"
    eval "poetry run isort ${ISORT_ACTION} ${STEP_EXTRA_ARGUMENTS[isort]} ."
  fi

  if [[ ${STEPS_ACTIVE_MAP[flake8]} == "true" ]]; then
    echo "Running flake8... 🧐"
    eval "poetry run flake8 ${STEP_EXTRA_ARGUMENTS[flake8]} ."
  fi

  if [[ ${STEPS_ACTIVE_MAP[mypy]} == "true" ]]; then
    echo "Running mypy... 🐍"
    eval "poetry run mypy ${STEP_EXTRA_ARGUMENTS[mypy]} ."
  fi

  if [[ ${STEPS_ACTIVE_MAP[pytest]} == "true" ]]; then
    if [[ ${SKIP_COVERAGE} == "true" ]]; then
      echo "Running pytest... ✅"
      eval "poetry run pytest ${STEP_EXTRA_ARGUMENTS[pytest]}"
    else
      echo "Running pytest with coverage... ✅"
      eval "poetry run pytest --cov=. --cov-report=term-missing ${STEP_EXTRA_ARGUMENTS[pytest]}"
    fi
  fi

  if [[ ${STEPS_ACTIVE_MAP[bandit]} == "true" ]]; then
    echo "Running bandit... 🕵️"
    eval "poetry run bandit --ini .bandit -rq ${STEP_EXTRA_ARGUMENTS[bandit]} ."
  fi
}

handle_input "$@"
run_steps

#!/usr/bin/env bash

# Dry Run Test Runner
# Usage: ./test_dry_run.sh [challenge]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo -e "${BLUE}🧪 Dry Run Quality Test Runner${NC}"
echo -e "${BLUE}================================${NC}"

# Configuration
TESTS_FOLDER="$PROJECT_ROOT/code/tests"
DRY_RUN_FOLDER="$PROJECT_ROOT/dry_run_output"
DRY_RUN_RESULTS_FOLDER="$DRY_RUN_FOLDER/test_results"

# Available tests (using existing test files)
TESTS=("1_code_compilability" "2_code_length" "3_modularity" "4_functional_completeness")
MODELS=("chatgpt" "claude" "gemini")

# Check if dry run output exists
if [ ! -d "$DRY_RUN_FOLDER" ]; then
    echo -e "${RED}❌ Dry run output directory not found: $DRY_RUN_FOLDER${NC}"
    echo -e "${YELLOW}💡 Run a dry run first: uv run python code/scraper/main.py --dry-run${NC}"
    exit 1
fi

# Get challenge from argument or find all challenges
CHALLENGE=""
if [ $# -gt 0 ]; then
    CHALLENGE="$1"
    echo -e "${GREEN}🎯 Testing challenge: $CHALLENGE${NC}"
else
    echo -e "${GREEN}🎯 Testing all challenges${NC}"
fi

# Create results directory
mkdir -p "$DRY_RUN_RESULTS_FOLDER"

# Find all generated code directories
CODE_DIRS=()
if [ -n "$CHALLENGE" ]; then
    # Specific challenge
    if [ -d "$DRY_RUN_FOLDER/code/$CHALLENGE" ]; then
        for prompt_dir in "$DRY_RUN_FOLDER/code/$CHALLENGE"/*; do
            if [ -d "$prompt_dir" ]; then
                for iter_dir in "$prompt_dir"/*; do
                    if [ -d "$iter_dir" ]; then
                        CODE_DIRS+=("$iter_dir")
                    fi
                done
            fi
        done
    fi
else
    # All challenges
    for challenge_dir in "$DRY_RUN_FOLDER/code"/*; do
        if [ -d "$challenge_dir" ]; then
            challenge_name=$(basename "$challenge_dir")
            for prompt_dir in "$challenge_dir"/*; do
                if [ -d "$prompt_dir" ]; then
                    for iter_dir in "$prompt_dir"/*; do
                        if [ -d "$iter_dir" ]; then
                            CODE_DIRS+=("$iter_dir")
                        fi
                    done
                fi
            done
        fi
    done
fi

if [ ${#CODE_DIRS[@]} -eq 0 ]; then
    echo -e "${RED}❌ No generated code directories found${NC}"
    exit 1
fi

echo -e "${GREEN}📊 Found ${#CODE_DIRS[@]} test directories${NC}"

# Function to run a single test
run_test() {
    local test_dir="$1"
    local test_name="$2"
    local model="$3"
    
    # Extract challenge name from path
    local challenge_name=$(echo "$test_dir" | sed -E 's|.*/code/([^/]+)/.*|\1|')
    
    # Copy test file to the directory
    local test_file="$TESTS_FOLDER/$challenge_name/$test_name.py"
    if [ ! -f "$test_file" ]; then
        echo -e "${YELLOW}⚠️  Test file not found: $test_file${NC}"
        return 1
    fi
    
    cp "$test_file" "$test_dir/$test_name.py"
    
    # Run the test
    local result_file="$DRY_RUN_RESULTS_FOLDER/$(basename "$test_dir")_${test_name}_${model}.txt"
    
    (
        cd "$test_dir"
        python3 "$test_name.py" "$model" > "$result_file" 2>&1
    )
    
    local exit_code=$?
    
    # Clean up test file
    rm -f "$test_dir/$test_name.py"
    
    return $exit_code
}

# Run tests on all directories
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

for test_dir in "${CODE_DIRS[@]}"; do
    dir_name=$(basename "$test_dir")
    echo -e "\n${BLUE}🔍 Testing: $dir_name${NC}"
    
    # Check which model files exist
    for model in "${MODELS[@]}"; do
        model_file="$test_dir/$model.py"
        if [ -f "$model_file" ]; then
            echo -e "  ${GREEN}📝 Found: $model.py${NC}"
            
            # Run each test
            for test in "${TESTS[@]}"; do
                echo -n "    🧪 $test... "
                TOTAL_TESTS=$((TOTAL_TESTS + 1))
                
                if run_test "$test_dir" "$test" "$model"; then
                    echo -e "${GREEN}✅ PASS${NC}"
                    PASSED_TESTS=$((PASSED_TESTS + 1))
                else
                    echo -e "${RED}❌ FAIL${NC}"
                    FAILED_TESTS=$((FAILED_TESTS + 1))
                fi
            done
        else
            echo -e "  ${YELLOW}⚠️  Missing: $model.py${NC}"
        fi
    done
done

# Summary
echo -e "\n${BLUE}📋 TEST SUMMARY${NC}"
echo -e "${BLUE}===============${NC}"
echo -e "Total tests run: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "${RED}Failed: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "\n${YELLOW}⚠️  Some tests failed. Check results in: $DRY_RUN_RESULTS_FOLDER${NC}"
    exit 1
fi

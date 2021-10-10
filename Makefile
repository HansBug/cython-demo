.PHONY: docs test unittest build clean

PYTHON := $(shell which python)

DOC_DIR  := ./docs
TEST_DIR := ./test
SRC_DIR  := ./cythondemo

RANGE_DIR      ?= .
RANGE_TEST_DIR := ${TEST_DIR}/${RANGE_DIR}
RANGE_SRC_DIR  := ${SRC_DIR}/${RANGE_DIR}

CYTHON_FILES := $(shell find ${SRC_DIR} -name '*.pyx')

COV_TYPES ?= xml term-missing

build:
	$(PYTHON) setup.py build_ext --inplace

clean:
	rm -rf $(shell find ${SRC_DIR} -name '*.so') \
			$(shell ls $(addsuffix .c, $(basename ${CYTHON_FILES})) \
					  $(addsuffix .cpp, $(basename ${CYTHON_FILES})) \
				2> /dev/null)

test: unittest benchmark

unittest:
	pytest "${RANGE_TEST_DIR}" \
		-sv -m unittest \
		$(shell for type in ${COV_TYPES}; do echo "--cov-report=$$type"; done) \
		--cov="${RANGE_SRC_DIR}" \
		$(if ${MIN_COVERAGE},--cov-fail-under=${MIN_COVERAGE},) \
		$(if ${WORKERS},-n ${WORKERS},)

benchmark:
	pytest "${RANGE_TEST_DIR}" \
		-sv -m benchmark \
		--durations=0 \
		$(if ${WORKERS},-n ${WORKERS},)

docs:
	$(MAKE) -C "${DOC_DIR}" build
pdocs:
	$(MAKE) -C "${DOC_DIR}" prod


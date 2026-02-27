PROJECT_NAME = F103_Jitter_PoC
BUILD_DIR    = F103_Jitter_PoC/build
GENERATOR    = "Unix Makefiles"

.PHONY: all configure build clean flash stflash size openocd debug

all: build

configure:
	mkdir -p $(BUILD_DIR)
	cd $(BUILD_DIR) && cmake -G $(GENERATOR) \
		-DCMAKE_TOOLCHAIN_FILE=../cmake/gcc-arm-none-eabi.cmake \
		-DCMAKE_BUILD_TYPE=Debug \
		..

build: configure
	cmake --build $(BUILD_DIR) -j$(shell nproc 2>/dev/null || echo 4)

clean:
	rm -rf $(BUILD_DIR)

flash: build
	cmake --build $(BUILD_DIR) --target flash

stflash: build
	cmake --build $(BUILD_DIR) --target stflash

size: build
	arm-none-eabi-size $(BUILD_DIR)/$(PROJECT_NAME).elf

openocd: build
	cmake --build $(BUILD_DIR) --target openocd

debug: build
	@GDB=; \
	if which gdb-multiarch >/dev/null 2>&1; then GDB=gdb-multiarch; fi; \
	if [ -z "$$GDB" ] && which arm-none-eabi-gdb >/dev/null 2>&1; then GDB=arm-none-eabi-gdb; fi; \
	if [ -z "$$GDB" ]; then echo "ERROR: No suitable GDB found. Install with sudo apt install gdb-multiarch"; exit 1; fi; \
	echo "Using GDB: $$GDB"; \
	$$GDB $(BUILD_DIR)/$(PROJECT_NAME).elf \
		-ex "target remote localhost:3333" \
		-ex "monitor reset halt" \
		-ex "load" \
		-ex "break main" \
		-ex "continue"
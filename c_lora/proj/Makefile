BIN_DIR = ./bin
OBJ_DIR = ./obj
USER_DIR=../user
LORA_DIR=../lora

INC_DIR= -I${USER_DIR} \
         -I${LORA_DIR}

SRC_USER = ${wildcard  ${USER_DIR}/*.c}
SRC_LORA = ${wildcard  ${LORA_DIR}/*.c}

OBJ_USER = ${patsubst %.c,${OBJ_DIR}/%.o,$(notdir ${SRC_USER})}
OBJ_LORA = ${patsubst %.c,${OBJ_DIR}/%.o,$(notdir ${SRC_LORA})}

TARGET=${BIN_DIR}/lora
# CC=gcc
CC=arm-none-linux-gnueabi-gcc
CCFLAGS=-g -Wall ${INC_DIR} -std=gnu99

${TARGET}: ${OBJ_USER} ${OBJ_LORA}
	${CC} ${OBJ_USER} ${OBJ_LORA} -o $@ -lpthread -lsqlite3
	@echo "Compile done."

$(OBJ_USER):${OBJ_DIR}/%.o:${USER_DIR}/%.c
	@echo "Compiling $< ==> $@"
	${CC} ${CCFLAGS} -c $< -o $@

$(OBJ_LORA):${OBJ_DIR}/%.o:${LORA_DIR}/%.c
	@echo "Compiling $< ==> $@"
	${CC} ${CCFLAGS} -c $< -o $@

clean:
	@rm -f ${OBJ_USER}
	@rm -f ${OBJ_LORA}
	@echo "Clean object files done."

	@rm -f *~
	@echo "Clean tempreator files done."

	@rm -f ${TARGET}
	@echo "Clean target files done."

	@echo "Clean done."

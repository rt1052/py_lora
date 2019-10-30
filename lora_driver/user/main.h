#ifndef _MAIN_H_
#define _MAIN_H_

#include <pthread.h>
#include <sys/types.h> 
#include <sys/socket.h> 
#include <unistd.h> 
#include <netinet/in.h> 
#include <arpa/inet.h> 
#include <stdint.h>
#include <stdio.h> 
#include <stdlib.h> 
#include <errno.h> 
#include <netdb.h> 
#include <stdarg.h> 
#include <string.h> 
#include <sys/msg.h>
#include <stdbool.h>
#include <semaphore.h>
#include <time.h>
#include <signal.h>

#include "sqlite3.h"  

 
typedef struct {
    long int type;
    void *pdata;
} msg_st;



extern int lora_recv_msg, lora_send_msg;
extern pthread_mutex_t lora_lock, lora_send_lock;
extern pthread_cond_t lora_cond;
extern sem_t lora_sem;


void *thread_user(void *arg);
void *thread_gets(void *arg);
void *thread_data(void *arg);
void *thread_alarm(void *arg);


uint8_t check_sum(uint8_t *buf, uint16_t len);

#endif



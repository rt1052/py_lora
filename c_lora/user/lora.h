#ifndef _LORA_H_
#define _LORA_H_

 

void *thread_lora(void *arg);
void *thread_tcp(void *arg);
uint8_t check_sum(uint8_t *buf, uint16_t len);



#endif

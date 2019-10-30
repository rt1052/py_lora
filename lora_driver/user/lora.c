#include <stdint.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>

#include "platform.h"

#include "sx1276-Hal.h"
#include "radio.h"
#include "sx1276.h"

#include "main.h"
#include "tcp.h"
#include "lora.h"

 
int fd_tcp_cli;

void *thread_lora(void *arg)
{
    uint8_t buf[1024];
    uint16_t len;

    SX1276Init();
    SX1276StartRx();    

    while(1) {   
        switch(SX1276Process()) {          
        case RF_RX_TIMEOUT:      
            break;
        case RF_RX_DONE:
            SX1276GetRxPacket(buf, &len);

            if ((len < 20) && (buf[len-1] == check_sum(buf, len-1))) {
                send(fd_tcp_cli, buf, len, 0);
            } else {
                // log_write("lora err len = %d \r\n", len);
            }
            break;
        case RF_TX_DONE:
            SX1276StartRx();
            break;
        default:
            break;
        }
        usleep(5 * 1000);
    }
}

void *thread_tcp(void *arg)
{
    int res;
    struct sockaddr_in server, client;
    uint8_t buf[1024];

    /* 设置端口和地址 */
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = htonl(INADDR_ANY);
    server.sin_port = htons(54201);

    /* 建立socket */
    int fd_tcp_srv = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(fd_tcp_srv, SOL_SOCKET, SO_REUSEADDR, NULL, 1);
    bind(fd_tcp_srv, (struct sockaddr *)&server, sizeof(server));
    listen(fd_tcp_srv, 5);


    int len = sizeof(struct sockaddr);
    /* 只支持一个连接 */
    fd_tcp_cli = accept(fd_tcp_srv, (struct sockaddr *)&client,
                        (socklen_t *)&len);
    /* 设置超时时间 */
    struct timeval timeout = {0, 200 * 1000};
    setsockopt(fd_tcp_cli, SOL_SOCKET, SO_RCVTIMEO, (char *)&timeout,
               sizeof(struct timeval));

    while(1) {
        int len = recv(fd_tcp_cli, buf, sizeof(buf), 0);  //MSG_WAITALL
        if (len > 0) {
            /* 等待lora空闲 */
            while(SX1276GetRFState() != 0x2) {
                usleep(200*1000);
            }
            /* 发送lora数据 */
            SX1276SetTxPacket(buf, len); 
        } else if (len == -1) {
            /* 超时则等待 */
            usleep(100);
        } else {
            /* len = 0 表示连接断开 */
            break;
        }
    }

    close(fd_tcp_srv);

    pthread_exit("tcp thread end");
}


uint8_t check_sum(uint8_t *buf, uint16_t len) 
{
    uint16_t i;
    uint8_t sum = 0;

    for(i = 0; i < len; i++) {
        sum += buf[i];
    }

    return sum;        
}

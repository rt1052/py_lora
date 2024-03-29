#include "main.h"
#include "lora.h"


void handle_pipe(int sig)
{
    //log_write("signal \r\n");
}

int main(void)
{
    int ch;
    int res;        
    void *thread_result;
    pthread_t tcp_thread, lora_thread;

    /* avoid tcp send to a closed connection to stop the program */
    struct sigaction sa;
    sa.sa_handler = handle_pipe;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGPIPE,&sa,NULL);

    printf("lora driver \r\n");

    /* tcp thread */
    res = pthread_create(&tcp_thread, NULL, thread_tcp, NULL);
    if (res != 0) {
        printf("tcp thread creation failed");
        exit(EXIT_FAILURE);
    }      

    /* lora rx&tx */
    res = pthread_create(&lora_thread, NULL, thread_lora, NULL);
    if (res != 0) {
        printf("lora thread creation failed");
        exit(EXIT_FAILURE);
    }

    /* wait for thread finish */
    res = pthread_join(lora_thread, &thread_result);
    if (res != 0) {
        printf("lora thread join failed");
        exit(EXIT_FAILURE);
    }

    res = pthread_join(tcp_thread, &thread_result);
    if (res != 0) {
        printf("tcp thread join failed");
        exit(EXIT_FAILURE);
    }

    exit(EXIT_SUCCESS);
}

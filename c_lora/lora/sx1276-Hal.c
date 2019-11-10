/*
 * THE FOLLOWING FIRMWARE IS PROVIDED: (1) "AS IS" WITH NO WARRANTY; AND
 * (2)TO ENABLE ACCESS TO CODING INFORMATION TO GUIDE AND FACILITATE CUSTOMER.
 * CONSEQUENTLY, SEMTECH SHALL NOT BE HELD LIABLE FOR ANY DIRECT, INDIRECT OR
 * CONSEQUENTIAL DAMAGES WITH RESPECT TO ANY CLAIMS ARISING FROM THE CONTENT
 * OF SUCH FIRMWARE AND/OR THE USE MADE BY CUSTOMERS OF THE CODING INFORMATION
 * CONTAINED HEREIN IN CONNECTION WITH THEIR PRODUCTS.
 *
 * Copyright (C) SEMTECH S.A.
 */
/*!
 * \file       sx1276-Hal.c
 * \brief      SX1276 Hardware Abstraction Layer
 *
 * \version    2.0.B2
 * \date       Nov 21 2012
 * \author     Miguel Luis
 *
 * Last modified by Miguel Luis on Jun 19 2013
 */

#include "platform.h"
#include "sx1276-Hal.h"
#include "string.h"

int fd_spi;

void SX1276InitIo( void )
{
    gpio_init(GPIO_RST);
    gpio_direction(GPIO_RST, 1);

    gpio_set_value(GPIO_RST, 0);
    usleep(500 * 1000);
    gpio_set_value(GPIO_RST, 1);

    fd_spi = spi_init(0, 1, 400000);
}

void SX1276SetReset( uint8_t state )
{
    // Configure radio DI2 as inputs
    //GPIO_Init(RESET_IOPORT, RESET_PIN, GPIO_Mode_Out_PP_High_Fast);

    if( state == RADIO_RESET_ON )
    {
        gpio_set_value(GPIO_RST, 0);
    }
    else
    {
        gpio_set_value(GPIO_RST, 1);
    }

}

void SX1276Write( uint8_t addr, uint8_t data )
{
    SX1276WriteBuffer( addr, &data, 1 );
}

void SX1276Read( uint8_t addr, uint8_t *data )
{
    SX1276ReadBuffer( addr, data, 1 );
}

void SX1276WriteBuffer( uint8_t addr, uint8_t *buffer, uint8_t size )
{
    uint8_t buf[512];

    buf[0] = addr | 0x80;
    memcpy(buf+1, buffer, size);
    spi_write_then_read(fd_spi, buf, size+1, NULL, 0);
}

void SX1276ReadBuffer( uint8_t addr, uint8_t *buffer, uint8_t size )
{
    uint8_t buf[512];
    uint8_t buf_r[512];

    buf[0] = addr & 0x7f;
    memset(buf+1, 0, size);
    spi_write_then_read(fd_spi, buf, size+1, buf_r, size+1);
    memcpy(buffer, buf_r+1, size);
}

void SX1276WriteFifo( uint8_t *buffer, uint8_t size )
{
    SX1276WriteBuffer( 0, buffer, size );
}

void SX1276ReadFifo( uint8_t *buffer, uint8_t size )
{
    SX1276ReadBuffer( 0, buffer, size );
}

inline uint8_t SX1276ReadDio0( void )
{
    //return GPIO_ReadInputDataBit( DIO0_IOPORT, DIO0_PIN );
    return 0;
}

inline uint8_t SX1276ReadDio1( void )
{
    //return GPIO_ReadInputDataBit( DIO1_IOPORT, DIO1_PIN );
    return 0;
}

inline uint8_t SX1276ReadDio2( void )
{
    //return GPIO_ReadInputDataBit( DIO2_IOPORT, DIO2_PIN );
    return 0;
}

inline uint8_t SX1276ReadDio3( void )
{
    //return IoePinGet( RF_DIO3_PIN );
    //return GPIO_ReadInputDataBit( DIO3_IOPORT, DIO3_PIN );
    return 0;
}

inline uint8_t SX1276ReadDio4( void )
{
    //return IoePinGet( RF_DIO4_PIN );
    //return GPIO_ReadInputDataBit( DIO4_IOPORT, DIO4_PIN );
    return 0;
}

inline uint8_t SX1276ReadDio5( void )
{
    //return IoePinGet( RF_DIO5_PIN );
    //return GPIO_ReadInputDataBit( DIO5_IOPORT, DIO5_PIN );
    return 0;
}

inline void SX1276WriteRxTx( uint8_t txEnable )
{
    //u_printf("*********SX1276WriteRxTx en:%d\r\n", txEnable);
}

#include "time.h"

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

uint32_t GET_TICK_COUNT( void )
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    uint32_t t = tv.tv_sec * 1000 + tv.tv_usec / 1000;
    return t;
}
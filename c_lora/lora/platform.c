#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <linux/types.h>
#include <linux/spi/spidev.h>
#include "platform.h"

/***************************************************************************//**
 * @brief spi_init
*******************************************************************************/
int spi_init(uint8_t  clk_pha,
            uint8_t  clk_pol,
            uint32_t speed)
{
    uint8_t mode = 0;   //SPI_CPHA | SPI_CPOL;
    uint8_t bits = 8;
    int ret;

    if (clk_pha) {
        // Unused variable - fix compiler warning
    }
    if (clk_pol) {
        // Unused variable - fix compiler warning
    }

    int fd = open(SPIDEV_DEV, O_RDWR);
    if (fd < 0) {
        printf("%s: Can't open device\n\r", __func__);
        return -1;
    }

    ret = ioctl(fd, SPI_IOC_WR_MODE, &mode);
    if (ret == -1) {
        printf("%s: Can't set spi mode\n\r", __func__);
        return ret;
    }

    ret = ioctl(fd, SPI_IOC_RD_MODE, &mode);
    if (ret == -1) {
        printf("%s: Can't set spi mode\n\r", __func__);
        return ret;
    }

    ret = ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
    if (ret == -1) {
        printf("%s: Can't set bits per word\n\r", __func__);
        return ret;
    }

    ret = ioctl(fd, SPI_IOC_RD_BITS_PER_WORD, &bits);
    if (ret == -1) {
        printf("%s: Can't set bits per word\n\r", __func__);
        return ret;
    }

    ret = ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
    if (ret == -1) {
        printf("%s: Can't set max speed hz\n\r", __func__);
        return ret;
    }

    ret = ioctl(fd, SPI_IOC_RD_MAX_SPEED_HZ, &speed);
    if (ret == -1) {
        printf("%s: Can't set max speed hz\n\r", __func__);
        return ret;
    }

    return fd;
}



/***************************************************************************//**
 * @brief spi_write_then_read
*******************************************************************************/
int spi_write_then_read(int fd,
        uint8_t *txbuf, uint16_t n_tx,
        uint8_t *rxbuf, uint16_t n_rx)
{
    int ret = 0;

/*
    struct spi_ioc_transfer tr[2] = {
        {
            .tx_buf = (unsigned long)txbuf,
            .len = n_tx,
        }, {
            .rx_buf = (unsigned long)rxbuf,
            .len = n_rx,
        },
    };
*/

struct spi_ioc_transfer tr[] = {
    {
        .tx_buf = (unsigned long)txbuf,
        .rx_buf = (unsigned long)rxbuf,
        .len = n_tx,
    },
};

    ret = ioctl(fd, SPI_IOC_MESSAGE(1), &tr);
    if (ret == 1) {
        printf("%s: Can't send spi message\n\r", __func__);
        return -EIO;
    }

    return ret;
}

void spi_close(int fd)
{
    close(fd);
}


/***************************************************************************//**
 * @brief gpio_init
*******************************************************************************/
void gpio_init(uint32_t pin)
{
    int fd, len;
    char buf[11];
    int ret;

    fd = open("/sys/class/gpio/export", O_WRONLY);
    if (fd < 0) {
        printf("%s: Can't export GPIO\n\r", __func__);
        return;
    }

    len = snprintf(buf, sizeof(buf), "%d", pin);
    ret = write(fd, buf, len);
    if (ret == -1) {
        // Unused variable - fix compiler warning
    }

    close(fd);
}

/***************************************************************************//**
 * @brief gpio_direction
*******************************************************************************/
void gpio_direction(uint16_t pin, uint8_t direction)
{
    int fd;
    char buf[60];
    int ret;

    //snprintf(buf, sizeof(buf), "/sys/class/gpio/gpio%d/direction", pin);
    snprintf(buf, sizeof(buf), "/sys/class/gpio/pio%c%d/direction", (pin / 32) + 'A', (pin % 32));

    fd = open(buf, O_WRONLY);
    if (fd < 0) {
        printf("%s: Can't set GPIO direction\n\r", __func__);
        return;
    }

    if (direction == 1)
        ret = write(fd, "out", 4);
    else
        ret = write(fd, "in", 3);
    if (ret == -1) {
        // Unused variable - fix compiler warning
    }

    close(fd);
}

/***************************************************************************//**
 * @brief gpio_set_value
*******************************************************************************/
void gpio_set_value(unsigned pin, int value)
{
    int fd;
    char buf[60];
    int ret;

    //snprintf(buf, sizeof(buf), "/sys/class/gpio/gpio%d/value", pin);
    snprintf(buf, sizeof(buf), "/sys/class/gpio/pio%c%d/value", (pin / 32) + 'A', (pin % 32));

    fd = open(buf, O_WRONLY);
    if (fd < 0) {
        printf("%s: Can't set GPIO value\n\r", __func__);
        return;
    }

    if (value)
        ret = write(fd, "1", 2);
    else
        ret = write(fd, "0", 2);
    if (ret == -1) {
        // Unused variable - fix compiler warning
    }

    close(fd);
}

int gpio_get_value(unsigned pin)
{
    int fd;
    char buf[60];
    char str[3];

    //snprintf(buf, sizeof(buf), "/sys/class/gpio/gpio%d/value", pin);
    snprintf(buf, sizeof(buf), "/sys/class/gpio/pio%c%d/value", (pin / 32) + 'A', (pin % 32));

    fd = open(buf, O_RDONLY);
    if (fd < 0) {
        printf("%s: Can't get GPIO value\n\r", __func__);
        return -1;
    }

    read(fd, str, 2);
    close(fd);

    if (str[0] == '1') {
        return 1;
    } else {
        return 0;
    }
}

void fpga_led(int value)
{
    int fd;
    fd =  open("/sys/class/leds/d1/brightness", O_WRONLY);
    if (fd < 0) {
        printf("%s: Can't set led value\n\r", __func__);
        return;
    }

    if (value) {
        write(fd, "1", 2);
    } else {
        write(fd, "0", 2);
    }

    close(fd);
}

int fpga_init(void)
{
    int fd = spi_init(0, 1, 32000000);

    gpio_init(GPIO_DONE);
    gpio_init(GPIO_INIT);
    gpio_init(GPIO_PROG);

    gpio_direction(GPIO_DONE, 0);
    gpio_direction(GPIO_INIT, 0);
    gpio_direction(GPIO_PROG, 1);

    return fd;
}

void fpga_close(int fd)
{
    spi_close(fd);
}

/******************************************************************************
* delay() is a simple wait loop. It very roughly matches 1 us on a 75 MHz MB
* system. Used to make sure PROGRAM_B is asserted long enough

* @param count is the number of units of time (very roughly 1 us with a 75 MHz
*   clock) to wait
*
* @return
*   None
*
******************************************************************************/
void delay(int count)
{
    int us_adjust = 500;
    for(int i = 0; i < count * us_adjust ; i++)
        ;
}

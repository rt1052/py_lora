#include <stdint.h>
#include <linux/spi/spidev.h>


#define SPIDEV_DEV          "/dev/spidev32765.0"  // "/dev/spidev1.0"

#define GPIOA_CHIP_BASE	    0
#define GPIOB_CHIP_BASE	    32
#define GPIOE_CHIP_BASE	    128
#define GPIO_DONE			(GPIOB_CHIP_BASE + 0)
#define GPIO_INIT		    (GPIOB_CHIP_BASE + 2)
#define GPIO_PROG			(GPIOB_CHIP_BASE + 8)   // not defined

#define GPIO_RST  (GPIOA_CHIP_BASE + 27)

int spi_init(uint8_t  clk_pha,
            uint8_t  clk_pol,
            uint32_t speed);

int spi_write_then_read(int fd,
        uint8_t *txbuf, uint16_t n_tx,
        uint8_t *rxbuf, uint16_t n_rx);

void spi_close(int fd);

void gpio_init(uint32_t device_id);
void gpio_direction(uint16_t pin, uint8_t direction);
void gpio_set_value(unsigned gpio, int value);
int gpio_get_value(unsigned gpio);
void fpga_led(int value);
int fpga_init(void);
void fpga_close(int fd);
void delay(int);;

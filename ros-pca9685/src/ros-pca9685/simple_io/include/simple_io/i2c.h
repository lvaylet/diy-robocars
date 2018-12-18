/*******************************************************************************
 * MIT License
 *
 * Copyright (c) 2016 cocasema
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 ******************************************************************************/

#pragma once

#include <ros/ros.h>

#include <errno.h>
#include <fcntl.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>

namespace simple_io {

class I2C
{
public:
  I2C(uint8_t bus, uint8_t address)
    : bus_(bus)
    , address_(address)
    , file_(0)
  {}

  ~I2C()
  {
    close(file_);
  }

  bool init()
  {
    char filename[20];
    snprintf(filename, sizeof(filename), "/dev/i2c-%u", bus_);

    if ((file_ = open(filename, O_RDWR)) < 0) {
      ROS_ERROR("I2C: Failed to open bus '%s': %i-%s",
                filename, errno, strerror(errno));
      return false;
    }

    if (ioctl(file_, I2C_SLAVE, address_) < 0) {
      ROS_ERROR("I2C: Failed to acquire bus access and/or talk to slave: %i-%s",
                errno, strerror(errno));
      return false;
    }

    ROS_INFO("I2C: Successfully initialized [%s 0x%02x]", filename, address_);
    return true;
  }


  bool write(uint8_t reg, uint8_t const* data, size_t size)
  {
    uint8_t buf[1 + size];
    buf[0] = reg;
    memcpy(buf + 1, data, size);

    if (::write(file_, buf, sizeof(buf)) != (ssize_t)sizeof(buf)) {
      ROS_ERROR("I2C: Failed to write data to register 0x%02x: %i-%s",
                reg, errno, strerror(errno));
      return false;
    }

    ROS_DEBUG("I2C: Successfully wrote %zu byte(s) to reg=0x%02x", size, reg);
    return true;
  }

  template <typename T>
  bool write(uint8_t reg, T const& data)
  {
    return write(reg, reinterpret_cast<uint8_t const*>(&data), sizeof(T));
  }

  template <typename T, size_t N>
  bool write(uint8_t reg, T (&data)[N])
  {
    return write(reg, reinterpret_cast<uint8_t const*>(&data), sizeof(T) * N);
  }

  bool write_uint8 (uint8_t reg, uint8_t data)  { return write(reg, data); }
  bool write_uint16(uint8_t reg, uint16_t data) { return write(reg, data); }


  bool read(uint8_t reg, uint8_t* data, size_t size)
  {
    if (::write(file_, &reg, sizeof(reg)) != sizeof(reg)) {
      ROS_ERROR("I2C: Failed to read byte(s) - writing reg=0x%02x: %i-%s",
                reg, errno, strerror(errno));
      return false;
    }

    if (::read(file_, data, (ssize_t)size) != (ssize_t)size) {
      ROS_ERROR("I2C: Failed to read byte(s) - reading reg=0x%02x: %i-%s",
                reg, errno, strerror(errno));
      return false;
    }

    ROS_DEBUG("I2C: Successfully read %zu byte(s) from reg=0x%02x", size, reg);
    return true;
  }

  template <typename T>
  bool read(uint8_t reg, T* data)
  {
    return read(reg, reinterpret_cast<uint8_t*>(data), sizeof(T));
  }

  template <typename T, size_t N>
  bool read(uint8_t reg, T (*data)[N])
  {
    return read(reg, reinterpret_cast<uint8_t*>(data), sizeof(T) * N);
  }

private:
  const uint8_t bus_;
  const uint8_t address_;

  int file_;
};

} // namespace simple_io

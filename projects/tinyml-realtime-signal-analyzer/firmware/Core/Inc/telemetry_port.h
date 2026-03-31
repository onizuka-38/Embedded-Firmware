#ifndef TELEMETRY_PORT_H
#define TELEMETRY_PORT_H

#include <stdint.h>

int telemetry_port_send_line(const char *line, uint32_t length);

#endif

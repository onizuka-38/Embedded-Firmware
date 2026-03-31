#ifndef TELEMETRY_H
#define TELEMETRY_H

int telemetry_send_sample(float sample);
int telemetry_send_inference(float probability, int label);

#endif

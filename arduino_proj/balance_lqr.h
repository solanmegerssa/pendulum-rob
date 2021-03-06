#include "constants.h"
#include <assert.h>
#include <math.h>

// need pos, v, pitch, pitch_rate gains for torque response
float torque_gains[SIZE_STATE] = {-0.95668461, -15.58193723, 16.2464761, 9.07575802}; //computed in balance_lqr.py
const float OMEGA_MAX = 24.0;
const float TORQUE_OMEGA_GAIN = 0.5; // gain from torque command to angular velocity command

float weightSum(float state_array[], float weights[]) {
    float response = 0.0;
    if (sizeof(state_array) == sizeof(weights));
        // assert arrays are same length?
        for (int i =0; i < SIZE_STATE; i++) {
            response += weights[i]*state_array[i];
        }

    return response;
}

float computeLQRResponse(float state_array[]) {
    // computes weighted sum and clips result
    float response = weightSum(state_array, torque_gains);
    response *= TORQUE_OMEGA_GAIN;
    response = fmin(fmax(response, -OMEGA_MAX), OMEGA_MAX);
    
    return response;
}
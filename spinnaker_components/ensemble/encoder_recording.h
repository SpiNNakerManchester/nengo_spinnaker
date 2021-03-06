/**
 * Ensemble - Encoder recording
 * -----------------------------
 * Functions to perform recording of encoder learning in action
 *
 * Authors:
 *   - James Knight <knightj@cs.man.ac.uk>
 *
 * Copyright:
 *   - Advanced Processor Technologies, School of Computer Science,
 *      University of Manchester
 *
 * \addtogroup ensemble
 * @{
 */


#ifndef __ENCODER_RECORDING_H__
#define __ENCODER_RECORDING_H__

#include <stdbool.h>
#include <string.h>

#include "spin1_api.h"
#include "common-typedefs.h"
#include "nengo_typedefs.h"

//-----------------------------------------------------------------------------
// Structs
//-----------------------------------------------------------------------------
typedef struct encoder_recording_buffer_t
{
  //! Whether or not to record learnt encoders
  bool record;

  //! Start of the buffer in SDRAM
  value_t *sdram_start;

  //! Current location in the SDRAM buffer
  value_t *sdram_current;
} encoder_recording_buffer_t;

//-----------------------------------------------------------------------------
// Inline functions
//-----------------------------------------------------------------------------
static inline void record_learnt_encoders(encoder_recording_buffer_t *buffer,
  uint n_input_dimensions, const value_t *learnt_encoder_vector)
{
  // If recording's enabled
  if(buffer->record)
  {
    // Copy vector into SDRAM
    memcpy(buffer->sdram_current, learnt_encoder_vector,
           sizeof(value_t) * n_input_dimensions);

    // Advance SDRAM pointer
    buffer->sdram_current += n_input_dimensions;
  }
}


//-----------------------------------------------------------------------------
// Functions
//-----------------------------------------------------------------------------
bool record_learnt_encoders_initialise(encoder_recording_buffer_t *buffer, address_t region);

void record_learnt_encoders_reset(encoder_recording_buffer_t *buffer);

#endif  // __ENCODER_RECORDING_H__
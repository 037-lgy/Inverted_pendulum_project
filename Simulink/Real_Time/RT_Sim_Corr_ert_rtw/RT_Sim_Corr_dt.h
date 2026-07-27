/*
 * RT_Sim_Corr_dt.h
 *
 * Classroom License -- for classroom instructional use only.  Not for
 * government, commercial, academic research, or other organizational use.
 *
 * Code generation for model "RT_Sim_Corr".
 *
 * Model version              : 1.920
 * Simulink Coder version : 9.3 (R2020a) 18-Nov-2019
 * C source code generated on : Mon Jul 27 10:28:57 2026
 *
 * Target selection: ert.tlc
 * Embedded hardware selection: ARM Compatible->ARM 9
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "ext_types.h"

/* data type size table */
static uint_T rtDataTypeSizes[] = {
  sizeof(real_T),
  sizeof(real32_T),
  sizeof(int8_T),
  sizeof(uint8_T),
  sizeof(int16_T),
  sizeof(uint16_T),
  sizeof(int32_T),
  sizeof(uint32_T),
  sizeof(boolean_T),
  sizeof(fcn_call_T),
  sizeof(int_T),
  sizeof(pointer_T),
  sizeof(action_T),
  2*sizeof(uint32_T)
};

/* data type name table */
static const char_T * rtDataTypeNames[] = {
  "real_T",
  "real32_T",
  "int8_T",
  "uint8_T",
  "int16_T",
  "uint16_T",
  "int32_T",
  "uint32_T",
  "boolean_T",
  "fcn_call_T",
  "int_T",
  "pointer_T",
  "action_T",
  "timer_uint32_pair_T"
};

/* data type transitions for block I/O structure */
static DataTypeTransition rtBTransitions[] = {
  { (char_T *)(&RT_Sim_Corr_B.Sum), 0, 0, 1 },

  { (char_T *)(&RT_Sim_Corr_B.counter_value), 1, 0, 6 }
  ,

  { (char_T *)(&RT_Sim_Corr_DWork.FromWs_PWORK.TimePtr), 11, 0, 4 },

  { (char_T *)(&RT_Sim_Corr_DWork.UnitDelay_DSTATE[0]), 1, 0, 12 },

  { (char_T *)(&RT_Sim_Corr_DWork.FromWs_IWORK.PrevIndex), 10, 0, 1 },

  { (char_T *)(&RT_Sim_Corr_DWork.FixPtUnitDelay2_DSTATE), 3, 0, 1 },

  { (char_T *)(&RT_Sim_Corr_DWork.GyroCalibration_SubsysRanBC), 2, 0, 2 },

  { (char_T *)(&RT_Sim_Corr_DWork.BalanceandDriveControl_MODE), 8, 0, 1 }
};

/* data type transition table for block I/O structure */
static DataTypeTransitionTable rtBTransTable = {
  8U,
  rtBTransitions
};

/* data type transitions for Parameters structure */
static DataTypeTransition rtPTransitions[] = {
  { (char_T *)(&RT_Sim_Corr_P.pwm_gain), 0, 0, 2 },

  { (char_T *)(&RT_Sim_Corr_P.BATTERY), 1, 0, 7 },

  { (char_T *)(&RT_Sim_Corr_P.Speaker_speakerVolume), 7, 0, 1 },

  { (char_T *)(&RT_Sim_Corr_P.Gain1_Gain), 0, 0, 8 },

  { (char_T *)(&RT_Sim_Corr_P.UnitDelay_InitialCondition), 1, 0, 34 },

  { (char_T *)(&RT_Sim_Corr_P.Constant_Value_aljrxhz2pj), 7, 0, 3 },

  { (char_T *)(&RT_Sim_Corr_P.FixPtUnitDelay2_InitialConditio), 3, 0, 4 }
};

/* data type transition table for Parameters structure */
static DataTypeTransitionTable rtPTransTable = {
  7U,
  rtPTransitions
};

/* [EOF] RT_Sim_Corr_dt.h */

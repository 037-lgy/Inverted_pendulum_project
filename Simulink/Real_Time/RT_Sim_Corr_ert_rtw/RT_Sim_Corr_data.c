/*
 * Classroom License -- for classroom instructional use only.  Not for
 * government, commercial, academic research, or other organizational use.
 *
 * File: RT_Sim_Corr_data.c
 *
 * Code generated for Simulink model 'RT_Sim_Corr'.
 *
 * Model version                  : 1.920
 * Simulink Coder version         : 9.3 (R2020a) 18-Nov-2019
 * C/C++ source code generated on : Mon Jul 27 10:23:26 2026
 *
 * Target selection: ert.tlc
 * Embedded hardware selection: ARM Compatible->ARM 9
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "RT_Sim_Corr.h"
#include "RT_Sim_Corr_private.h"

/* Block parameters (default storage) */
Parameters_RT_Sim_Corr RT_Sim_Corr_P = {
  /* Variable: pwm_gain
   * Referenced by:
   *   '<S13>/Gain'
   *   '<S14>/Gain'
   */
  1.0,

  /* Variable: pwm_offset
   * Referenced by:
   *   '<S13>/Gain1'
   *   '<S14>/Gain1'
   */
  0.0,

  /* Variable: BATTERY
   * Referenced by: '<S1>/Constant4'
   */
  8000.0F,

  /* Variable: a_d
   * Referenced by: '<S18>/Gain2'
   */
  0.8F,

  /* Variable: a_gc
   * Referenced by: '<S5>/Gain3'
   */
  0.8F,

  /* Variable: a_gd
   * Referenced by: '<S15>/Gain4'
   */
  0.999F,

  /* Variable: time_start
   * Referenced by: '<S4>/Constant'
   */
  1250.0F,

  /* Variable: ts1
   * Referenced by: '<S17>/Gain'
   */
  0.004F,

  /* Mask Parameter: CompareToConstant1_const
   * Referenced by: '<S9>/Constant'
   */
  0.8F,

  /* Mask Parameter: Speaker_speakerVolume
   * Referenced by: '<S20>/Speaker'
   */
  25U,

  /* Expression: 100
   * Referenced by: '<S7>/Gain1'
   */
  100.0,

  /* Expression: 100
   * Referenced by: '<S7>/Saturation2'
   */
  100.0,

  /* Expression: -100
   * Referenced by: '<S7>/Saturation2'
   */
  -100.0,

  /* Expression: 100
   * Referenced by: '<S7>/Gain3'
   */
  100.0,

  /* Expression: 100
   * Referenced by: '<S7>/Saturation3'
   */
  100.0,

  /* Expression: -100
   * Referenced by: '<S7>/Saturation3'
   */
  -100.0,

  /* Expression: 0
   * Referenced by: '<Root>/Constant'
   */
  0.0,

  /* Expression: -0.2606
   * Referenced by: '<Root>/Gain1'
   */
  -0.2606,

  /* Computed Parameter: UnitDelay_InitialCondition
   * Referenced by: '<S17>/Unit Delay'
   */
  0.0F,

  /* Computed Parameter: Gain1_Gain_j0r0df4nzm
   * Referenced by: '<S15>/Gain1'
   */
  0.001F,

  /* Computed Parameter: FixPtUnitDelay1_InitialConditio
   * Referenced by: '<S19>/FixPt Unit Delay1'
   */
  0.0F,

  /* Computed Parameter: deg2rad_Gain
   * Referenced by: '<S8>/deg2rad'
   */
  0.0174532924F,

  /* Computed Parameter: deg2rad1_Gain
   * Referenced by: '<S8>/deg2rad1'
   */
  0.0174532924F,

  /* Computed Parameter: Gain_Gain
   * Referenced by: '<S8>/Gain'
   */
  0.5F,

  /* Computed Parameter: Gain3_Gain_hka0xvmyzz
   * Referenced by: '<S18>/Gain3'
   */
  0.2F,

  /* Computed Parameter: UnitDelay_InitialCon_bijcdbwmgf
   * Referenced by: '<S18>/Unit Delay'
   */
  0.0F,

  /* Computed Parameter: UnitDelay_InitialCon_azw54opzqy
   * Referenced by: '<S16>/Unit Delay'
   */
  0.0F,

  /* Computed Parameter: Gain_Gain_bwkvwsewsv
   * Referenced by: '<S16>/Gain'
   */
  250.0F,

  /* Computed Parameter: deg2rad2_Gain
   * Referenced by: '<S8>/deg2rad2'
   */
  0.0174532924F,

  /* Computed Parameter: Gain3_Gain_gjv3wryppp
   * Referenced by: '<S12>/Gain3'
   */
  0.001089F,

  /* Computed Parameter: Constant_Value_kzvkk53bcx
   * Referenced by: '<S12>/Constant'
   */
  0.625F,

  /* Computed Parameter: Gain2_Gain
   * Referenced by: '<S5>/Gain2'
   */
  0.2F,

  /* Computed Parameter: UnitDelay_InitialCon_egsil4m2ui
   * Referenced by: '<S5>/Unit Delay'
   */
  0.0F,

  /* Computed Parameter: Constant5_Value
   * Referenced by: '<S21>/Constant5'
   */
  0.0F,

  /* Computed Parameter: Constant8_Value
   * Referenced by: '<S6>/Constant8'
   */
  5000.0F,

  /* Computed Parameter: Constant6_Value
   * Referenced by: '<S21>/Constant6'
   */
  0.0F,

  /* Computed Parameter: UnitDelay_InitialCon_g5o4mik1am
   * Referenced by: '<Root>/Unit Delay'
   */
  { 0.0F, 0.0F, 0.0F, 0.0F },

  /* Computed Parameter: Gain2_Gain_ezbw1uq0ur
   * Referenced by: '<Root>/Gain2'
   */
  { -0.2606F, -18.0048F, -0.7444F, -1.75716F },

  /* Computed Parameter: Constant6_Value_hyqvqn5fwb
   * Referenced by: '<S6>/Constant6'
   */
  0.0F,

  /* Computed Parameter: UnitDelay3_InitialCondition
   * Referenced by: '<S21>/UnitDelay3'
   */
  0.0F,

  /* Computed Parameter: Constant7_Value
   * Referenced by: '<S6>/Constant7'
   */
  1.0F,

  /* Computed Parameter: Constant5_Value_jhrxeiwmg5
   * Referenced by: '<S6>/Constant5'
   */
  1.0F,

  /* Computed Parameter: DiscreteFilter_NumCoef
   * Referenced by: '<S1>/Discrete Filter'
   */
  0.2F,

  /* Computed Parameter: DiscreteFilter_DenCoef
   * Referenced by: '<S1>/Discrete Filter'
   */
  { 1.0F, -0.8F },

  /* Computed Parameter: DiscreteFilter_InitialStates
   * Referenced by: '<S1>/Discrete Filter'
   */
  0.0F,

  /* Computed Parameter: Constant_Value_aljrxhz2pj
   * Referenced by: '<S5>/Constant'
   */
  440U,

  /* Computed Parameter: Speaker_p2
   * Referenced by: '<S20>/Speaker'
   */
  100U,

  /* Computed Parameter: Speaker_p4
   * Referenced by: '<S20>/Speaker'
   */
  100U,

  /* Computed Parameter: FixPtUnitDelay2_InitialConditio
   * Referenced by: '<S19>/FixPt Unit Delay2'
   */
  1U,

  /* Computed Parameter: FixPtConstant_Value
   * Referenced by: '<S19>/FixPt Constant'
   */
  0U,

  /* Computed Parameter: Speaker_p1
   * Referenced by: '<S20>/Speaker'
   */
  1U,

  /* Computed Parameter: ManualSwitch_CurrentSetting
   * Referenced by: '<Root>/Manual Switch'
   */
  1U
};

/*
 * File trailer for generated code.
 *
 * [EOF]
 */

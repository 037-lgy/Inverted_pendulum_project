/*
 * Classroom License -- for classroom instructional use only.  Not for
 * government, commercial, academic research, or other organizational use.
 *
 * File: RT_Sim_Corr.h
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

#ifndef RTW_HEADER_RT_Sim_Corr_h_
#define RTW_HEADER_RT_Sim_Corr_h_
#include <math.h>
#include <float.h>
#include <string.h>
#include <stddef.h>
#ifndef RT_Sim_Corr_COMMON_INCLUDES_
# define RT_Sim_Corr_COMMON_INCLUDES_
#include "rtwtypes.h"
#include "rtw_extmode.h"
#include "sysran_types.h"
#include "rtw_continuous.h"
#include "rtw_solver.h"
#include "dt_info.h"
#include "ext_work.h"
#include "driver_ev3.h"
#endif                                 /* RT_Sim_Corr_COMMON_INCLUDES_ */

#include "RT_Sim_Corr_types.h"

/* Shared type includes */
#include "multiword_types.h"
#include "rtGetNaN.h"
#include "rt_nonfinite.h"
#include "rtGetInf.h"

/* Macros for accessing real-time model data structure */
#ifndef rtmGetFinalTime
# define rtmGetFinalTime(rtm)          ((rtm)->Timing.tFinal)
#endif

#ifndef rtmGetRTWExtModeInfo
# define rtmGetRTWExtModeInfo(rtm)     ((rtm)->extModeInfo)
#endif

#ifndef rtmGetErrorStatus
# define rtmGetErrorStatus(rtm)        ((rtm)->errorStatus)
#endif

#ifndef rtmSetErrorStatus
# define rtmSetErrorStatus(rtm, val)   ((rtm)->errorStatus = (val))
#endif

#ifndef rtmGetStopRequested
# define rtmGetStopRequested(rtm)      ((rtm)->Timing.stopRequestedFlag)
#endif

#ifndef rtmSetStopRequested
# define rtmSetStopRequested(rtm, val) ((rtm)->Timing.stopRequestedFlag = (val))
#endif

#ifndef rtmGetStopRequestedPtr
# define rtmGetStopRequestedPtr(rtm)   (&((rtm)->Timing.stopRequestedFlag))
#endif

#ifndef rtmGetT
# define rtmGetT(rtm)                  (rtmGetTPtr((rtm))[0])
#endif

#ifndef rtmGetTFinal
# define rtmGetTFinal(rtm)             ((rtm)->Timing.tFinal)
#endif

#ifndef rtmGetTPtr
# define rtmGetTPtr(rtm)               ((rtm)->Timing.t)
#endif

/* Block signals (default storage) */
typedef struct {
  real_T Sum;                          /* '<Root>/Sum' */
  real32_T counter_value;              /* '<S21>/Switch1' */
  real32_T Sum1;                       /* '<S5>/Sum1' */
  real32_T UnitDelay;                  /* '<S17>/Unit Delay' */
  real32_T Gain;                       /* '<S8>/Gain' */
  real32_T Gain_oopwalytwu;            /* '<S16>/Gain' */
  real32_T psidot;                     /* '<S8>/deg2rad2' */
} BlockIO_RT_Sim_Corr;

/* Block states (default storage) for system '<Root>' */
typedef struct {
  struct {
    void *TimePtr;
    void *DataPtr;
    void *RSimInfoPtr;
  } FromWs_PWORK;                      /* '<S2>/FromWs' */

  struct {
    void *LoggedData[2];
  } Scope_PWORK;                       /* '<Root>/Scope' */

  struct {
    void *LoggedData;
  } Scope_PWORK_pmo3q4xz34;            /* '<S6>/Scope' */

  real32_T UnitDelay_DSTATE[4];        /* '<Root>/Unit Delay' */
  real32_T UnitDelay3_DSTATE;          /* '<S21>/UnitDelay3' */
  real32_T DiscreteFilter_states;      /* '<S1>/Discrete Filter' */
  real32_T UnitDelay_DSTATE_cfkvxtl130;/* '<S5>/Unit Delay' */
  real32_T UnitDelay_DSTATE_hzuovbre5y;/* '<S17>/Unit Delay' */
  real32_T FixPtUnitDelay1_DSTATE;     /* '<S19>/FixPt Unit Delay1' */
  real32_T UnitDelay_DSTATE_orvhqhlbcp;/* '<S18>/Unit Delay' */
  real32_T UnitDelay_DSTATE_mjna1kxy33;/* '<S16>/Unit Delay' */
  real32_T DiscreteFilter_tmp;         /* '<S1>/Discrete Filter' */
  struct {
    int_T PrevIndex;
  } FromWs_IWORK;                      /* '<S2>/FromWs' */

  uint8_T FixPtUnitDelay2_DSTATE;      /* '<S19>/FixPt Unit Delay2' */
  int8_T GyroCalibration_SubsysRanBC;  /* '<S1>/Gyro Calibration' */
  int8_T BalanceandDriveControl_SubsysRa;/* '<S1>/Balance and Drive Control' */
  boolean_T BalanceandDriveControl_MODE;/* '<S1>/Balance and Drive Control' */
} D_Work_RT_Sim_Corr;

/* Parameters (default storage) */
struct Parameters_RT_Sim_Corr_ {
  real_T pwm_gain;                     /* Variable: pwm_gain
                                        * Referenced by:
                                        *   '<S13>/Gain'
                                        *   '<S14>/Gain'
                                        */
  real_T pwm_offset;                   /* Variable: pwm_offset
                                        * Referenced by:
                                        *   '<S13>/Gain1'
                                        *   '<S14>/Gain1'
                                        */
  real32_T BATTERY;                    /* Variable: BATTERY
                                        * Referenced by: '<S1>/Constant4'
                                        */
  real32_T a_d;                        /* Variable: a_d
                                        * Referenced by: '<S18>/Gain2'
                                        */
  real32_T a_gc;                       /* Variable: a_gc
                                        * Referenced by: '<S5>/Gain3'
                                        */
  real32_T a_gd;                       /* Variable: a_gd
                                        * Referenced by: '<S15>/Gain4'
                                        */
  real32_T time_start;                 /* Variable: time_start
                                        * Referenced by: '<S4>/Constant'
                                        */
  real32_T ts1;                        /* Variable: ts1
                                        * Referenced by: '<S17>/Gain'
                                        */
  real32_T CompareToConstant1_const; /* Mask Parameter: CompareToConstant1_const
                                      * Referenced by: '<S9>/Constant'
                                      */
  uint32_T Speaker_speakerVolume;      /* Mask Parameter: Speaker_speakerVolume
                                        * Referenced by: '<S20>/Speaker'
                                        */
  real_T Gain1_Gain;                   /* Expression: 100
                                        * Referenced by: '<S7>/Gain1'
                                        */
  real_T Saturation2_UpperSat;         /* Expression: 100
                                        * Referenced by: '<S7>/Saturation2'
                                        */
  real_T Saturation2_LowerSat;         /* Expression: -100
                                        * Referenced by: '<S7>/Saturation2'
                                        */
  real_T Gain3_Gain;                   /* Expression: 100
                                        * Referenced by: '<S7>/Gain3'
                                        */
  real_T Saturation3_UpperSat;         /* Expression: 100
                                        * Referenced by: '<S7>/Saturation3'
                                        */
  real_T Saturation3_LowerSat;         /* Expression: -100
                                        * Referenced by: '<S7>/Saturation3'
                                        */
  real_T Constant_Value;               /* Expression: 0
                                        * Referenced by: '<Root>/Constant'
                                        */
  real_T Gain1_Gain_cpx4lbewpy;        /* Expression: -0.2606
                                        * Referenced by: '<Root>/Gain1'
                                        */
  real32_T UnitDelay_InitialCondition;
                               /* Computed Parameter: UnitDelay_InitialCondition
                                * Referenced by: '<S17>/Unit Delay'
                                */
  real32_T Gain1_Gain_j0r0df4nzm;   /* Computed Parameter: Gain1_Gain_j0r0df4nzm
                                     * Referenced by: '<S15>/Gain1'
                                     */
  real32_T FixPtUnitDelay1_InitialConditio;
                          /* Computed Parameter: FixPtUnitDelay1_InitialConditio
                           * Referenced by: '<S19>/FixPt Unit Delay1'
                           */
  real32_T deg2rad_Gain;               /* Computed Parameter: deg2rad_Gain
                                        * Referenced by: '<S8>/deg2rad'
                                        */
  real32_T deg2rad1_Gain;              /* Computed Parameter: deg2rad1_Gain
                                        * Referenced by: '<S8>/deg2rad1'
                                        */
  real32_T Gain_Gain;                  /* Computed Parameter: Gain_Gain
                                        * Referenced by: '<S8>/Gain'
                                        */
  real32_T Gain3_Gain_hka0xvmyzz;   /* Computed Parameter: Gain3_Gain_hka0xvmyzz
                                     * Referenced by: '<S18>/Gain3'
                                     */
  real32_T UnitDelay_InitialCon_bijcdbwmgf;
                          /* Computed Parameter: UnitDelay_InitialCon_bijcdbwmgf
                           * Referenced by: '<S18>/Unit Delay'
                           */
  real32_T UnitDelay_InitialCon_azw54opzqy;
                          /* Computed Parameter: UnitDelay_InitialCon_azw54opzqy
                           * Referenced by: '<S16>/Unit Delay'
                           */
  real32_T Gain_Gain_bwkvwsewsv;     /* Computed Parameter: Gain_Gain_bwkvwsewsv
                                      * Referenced by: '<S16>/Gain'
                                      */
  real32_T deg2rad2_Gain;              /* Computed Parameter: deg2rad2_Gain
                                        * Referenced by: '<S8>/deg2rad2'
                                        */
  real32_T Gain3_Gain_gjv3wryppp;   /* Computed Parameter: Gain3_Gain_gjv3wryppp
                                     * Referenced by: '<S12>/Gain3'
                                     */
  real32_T Constant_Value_kzvkk53bcx;
                                /* Computed Parameter: Constant_Value_kzvkk53bcx
                                 * Referenced by: '<S12>/Constant'
                                 */
  real32_T Gain2_Gain;                 /* Computed Parameter: Gain2_Gain
                                        * Referenced by: '<S5>/Gain2'
                                        */
  real32_T UnitDelay_InitialCon_egsil4m2ui;
                          /* Computed Parameter: UnitDelay_InitialCon_egsil4m2ui
                           * Referenced by: '<S5>/Unit Delay'
                           */
  real32_T Constant5_Value;            /* Computed Parameter: Constant5_Value
                                        * Referenced by: '<S21>/Constant5'
                                        */
  real32_T Constant8_Value;            /* Computed Parameter: Constant8_Value
                                        * Referenced by: '<S6>/Constant8'
                                        */
  real32_T Constant6_Value;            /* Computed Parameter: Constant6_Value
                                        * Referenced by: '<S21>/Constant6'
                                        */
  real32_T UnitDelay_InitialCon_g5o4mik1am[4];
                          /* Computed Parameter: UnitDelay_InitialCon_g5o4mik1am
                           * Referenced by: '<Root>/Unit Delay'
                           */
  real32_T Gain2_Gain_ezbw1uq0ur[4];/* Computed Parameter: Gain2_Gain_ezbw1uq0ur
                                     * Referenced by: '<Root>/Gain2'
                                     */
  real32_T Constant6_Value_hyqvqn5fwb;
                               /* Computed Parameter: Constant6_Value_hyqvqn5fwb
                                * Referenced by: '<S6>/Constant6'
                                */
  real32_T UnitDelay3_InitialCondition;
                              /* Computed Parameter: UnitDelay3_InitialCondition
                               * Referenced by: '<S21>/UnitDelay3'
                               */
  real32_T Constant7_Value;            /* Computed Parameter: Constant7_Value
                                        * Referenced by: '<S6>/Constant7'
                                        */
  real32_T Constant5_Value_jhrxeiwmg5;
                               /* Computed Parameter: Constant5_Value_jhrxeiwmg5
                                * Referenced by: '<S6>/Constant5'
                                */
  real32_T DiscreteFilter_NumCoef; /* Computed Parameter: DiscreteFilter_NumCoef
                                    * Referenced by: '<S1>/Discrete Filter'
                                    */
  real32_T DiscreteFilter_DenCoef[2];
                                   /* Computed Parameter: DiscreteFilter_DenCoef
                                    * Referenced by: '<S1>/Discrete Filter'
                                    */
  real32_T DiscreteFilter_InitialStates;
                             /* Computed Parameter: DiscreteFilter_InitialStates
                              * Referenced by: '<S1>/Discrete Filter'
                              */
  uint32_T Constant_Value_aljrxhz2pj;
                                /* Computed Parameter: Constant_Value_aljrxhz2pj
                                 * Referenced by: '<S5>/Constant'
                                 */
  uint32_T Speaker_p2;                 /* Computed Parameter: Speaker_p2
                                        * Referenced by: '<S20>/Speaker'
                                        */
  uint32_T Speaker_p4;                 /* Computed Parameter: Speaker_p4
                                        * Referenced by: '<S20>/Speaker'
                                        */
  uint8_T FixPtUnitDelay2_InitialConditio;
                          /* Computed Parameter: FixPtUnitDelay2_InitialConditio
                           * Referenced by: '<S19>/FixPt Unit Delay2'
                           */
  uint8_T FixPtConstant_Value;        /* Computed Parameter: FixPtConstant_Value
                                       * Referenced by: '<S19>/FixPt Constant'
                                       */
  uint8_T Speaker_p1;                  /* Computed Parameter: Speaker_p1
                                        * Referenced by: '<S20>/Speaker'
                                        */
  uint8_T ManualSwitch_CurrentSetting;
                              /* Computed Parameter: ManualSwitch_CurrentSetting
                               * Referenced by: '<Root>/Manual Switch'
                               */
};

/* Real-time Model Data Structure */
struct tag_RTM_RT_Sim_Corr {
  const char_T *errorStatus;
  RTWExtModeInfo *extModeInfo;
  RTWSolverInfo solverInfo;

  /*
   * Sizes:
   * The following substructure contains sizes information
   * for many of the model attributes such as inputs, outputs,
   * dwork, sample times, etc.
   */
  struct {
    uint32_T checksums[4];
  } Sizes;

  /*
   * SpecialInfo:
   * The following substructure contains special information
   * related to other components that are dependent on RTW.
   */
  struct {
    const void *mappingInfo;
  } SpecialInfo;

  /*
   * Timing:
   * The following substructure contains information regarding
   * the timing information for the model.
   */
  struct {
    uint32_T clockTick0;
    uint32_T clockTickH0;
    time_T stepSize0;
    uint32_T clockTick1;
    uint32_T clockTickH1;
    uint32_T clockTick2;
    uint32_T clockTickH2;
    struct {
      uint8_T TID[3];
    } TaskCounters;

    time_T tFinal;
    SimTimeStep simTimeStep;
    boolean_T stopRequestedFlag;
    time_T *t;
    time_T tArray[3];
  } Timing;
};

/* Block parameters (default storage) */
extern Parameters_RT_Sim_Corr RT_Sim_Corr_P;

/* Block signals (default storage) */
extern BlockIO_RT_Sim_Corr RT_Sim_Corr_B;

/* Block states (default storage) */
extern D_Work_RT_Sim_Corr RT_Sim_Corr_DWork;

/* Model entry point functions */
extern void RT_Sim_Corr_initialize(void);
extern void RT_Sim_Corr_step(void);
extern void RT_Sim_Corr_terminate(void);

/* Real-time Model object */
extern RT_MODEL_RT_Sim_Corr *const RT_Sim_Corr_M;

/*-
 * These blocks were eliminated from the model due to optimizations:
 *
 * Block '<S19>/FixPt Data Type Duplicate1' : Unused code path elimination
 * Block '<S21>/Relational Operator2' : Unused code path elimination
 * Block '<S21>/Sum1' : Unused code path elimination
 * Block '<S1>/Data Type Conversion2' : Eliminate redundant data type conversion
 * Block '<S1>/Data Type Conversion5' : Eliminate redundant data type conversion
 * Block '<S20>/Data Type Conversion' : Eliminate redundant data type conversion
 */

/*-
 * The generated code includes comments that allow you to trace directly
 * back to the appropriate location in the model.  The basic format
 * is <system>/block_name, where system is the system number (uniquely
 * assigned by Simulink) and block_name is the name of the block.
 *
 * Use the MATLAB hilite_system command to trace the generated code back
 * to the model.  For example,
 *
 * hilite_system('<S3>')    - opens system 3
 * hilite_system('<S3>/Kp') - opens and selects block Kp which resides in S3
 *
 * Here is the system hierarchy for this model
 *
 * '<Root>' : 'RT_Sim_Corr'
 * '<S1>'   : 'RT_Sim_Corr/Plant'
 * '<S2>'   : 'RT_Sim_Corr/Signal Builder'
 * '<S3>'   : 'RT_Sim_Corr/Plant/Balance and Drive Control'
 * '<S4>'   : 'RT_Sim_Corr/Plant/Compare To Constant'
 * '<S5>'   : 'RT_Sim_Corr/Plant/Gyro Calibration'
 * '<S6>'   : 'RT_Sim_Corr/Plant/cont'
 * '<S7>'   : 'RT_Sim_Corr/Plant/Balance and Drive Control/Cal PWM'
 * '<S8>'   : 'RT_Sim_Corr/Plant/Balance and Drive Control/Cal x1'
 * '<S9>'   : 'RT_Sim_Corr/Plant/Balance and Drive Control/Compare To Constant1'
 * '<S10>'  : 'RT_Sim_Corr/Plant/Balance and Drive Control/Motor'
 * '<S11>'  : 'RT_Sim_Corr/Plant/Balance and Drive Control/Motor1'
 * '<S12>'  : 'RT_Sim_Corr/Plant/Balance and Drive Control/Cal PWM/Cal vol_max'
 * '<S13>'  : 'RT_Sim_Corr/Plant/Balance and Drive Control/Cal PWM/Friction Compensator1'
 * '<S14>'  : 'RT_Sim_Corr/Plant/Balance and Drive Control/Cal PWM/Friction Compensator2'
 * '<S15>'  : 'RT_Sim_Corr/Plant/Balance and Drive Control/Cal x1/Cal gyro_offset'
 * '<S16>'  : 'RT_Sim_Corr/Plant/Balance and Drive Control/Cal x1/Discrete Derivative (backward difference)'
 * '<S17>'  : 'RT_Sim_Corr/Plant/Balance and Drive Control/Cal x1/Discrete Integrator (Forward Euler)'
 * '<S18>'  : 'RT_Sim_Corr/Plant/Balance and Drive Control/Cal x1/Filter'
 * '<S19>'  : 'RT_Sim_Corr/Plant/Balance and Drive Control/Cal x1/Cal gyro_offset/Unit Delay External IC'
 * '<S20>'  : 'RT_Sim_Corr/Plant/Gyro Calibration/Speaker1'
 * '<S21>'  : 'RT_Sim_Corr/Plant/cont/conteur'
 */
#endif                                 /* RTW_HEADER_RT_Sim_Corr_h_ */

/*
 * File trailer for generated code.
 *
 * [EOF]
 */

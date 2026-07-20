/*
 * Classroom License -- for classroom instructional use only.  Not for
 * government, commercial, academic research, or other organizational use.
 *
 * File: Real_Time_Simulation_Correction.c
 *
 * Code generated for Simulink model 'Real_Time_Simulation_Correction'.
 *
 * Model version                  : 1.920
 * Simulink Coder version         : 9.3 (R2020a) 18-Nov-2019
 * C/C++ source code generated on : Mon Jul 20 17:19:13 2026
 *
 * Target selection: ert.tlc
 * Embedded hardware selection: ARM Compatible->ARM 9
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "Real_Time_Simulation_Correction.h"
#include "Real_Time_Simulation_Correction_private.h"
#include "Real_Time_Simulation_Correction_dt.h"

/* Block signals (default storage) */
BlockIO_Real_Time_Simulation_Co Real_Time_Simulation_Correcti_B;

/* Block states (default storage) */
D_Work_Real_Time_Simulation_Cor Real_Time_Simulation_Corr_DWork;

/* Real-time model */
RT_MODEL_Real_Time_Simulation_C Real_Time_Simulation_Correct_M_;
RT_MODEL_Real_Time_Simulation_C *const Real_Time_Simulation_Correct_M =
  &Real_Time_Simulation_Correct_M_;
static void rate_scheduler(void);

/*
 *   This function updates active task flag for each subrate.
 * The function is called at model base rate, hence the
 * generated code self-manages all its subrates.
 */
static void rate_scheduler(void)
{
  /* Compute which subrates run during the next base time step.  Subrates
   * are an integer multiple of the base rate counter.  Therefore, the subtask
   * counter is reset when it reaches its limit (zero means run).
   */
  (Real_Time_Simulation_Correct_M->Timing.TaskCounters.TID[2])++;
  if ((Real_Time_Simulation_Correct_M->Timing.TaskCounters.TID[2]) > 49) {/* Sample time: [0.2s, 0.0s] */
    Real_Time_Simulation_Correct_M->Timing.TaskCounters.TID[2] = 0;
  }
}

/* Model step function */
void Real_Time_Simulation_Correction_step(void)
{
  /* local block i/o variables */
  real_T rtb_Saturation3;
  real32_T rtb_Sum2;
  real32_T rtb_Sum;
  real32_T rtb_Sum_nvdedzgoqp;
  int32_T rtb_Encoder1_0;
  int32_T rtb_Encoder1_1;
  int32_T rtb_Encoder1_2;
  int8_T tmp;
  boolean_T Compare;
  real32_T u0;
  real_T tmp_0;
  real_T rtb_Saturation3_tmp;

  /* Reset subsysRan breadcrumbs */
  srClearBC(Real_Time_Simulation_Corr_DWork.BalanceandDriveControl_SubsysRa);

  /* Reset subsysRan breadcrumbs */
  srClearBC(Real_Time_Simulation_Corr_DWork.GyroCalibration_SubsysRanBC);

  /* FromWorkspace: '<S2>/FromWs' */
  {
    real_T *pDataValues = (real_T *)
      Real_Time_Simulation_Corr_DWork.FromWs_PWORK.DataPtr;
    real_T *pTimeValues = (real_T *)
      Real_Time_Simulation_Corr_DWork.FromWs_PWORK.TimePtr;
    int_T currTimeIndex = Real_Time_Simulation_Corr_DWork.FromWs_IWORK.PrevIndex;
    real_T t = Real_Time_Simulation_Correct_M->Timing.t[0];

    /* Get index */
    if (t <= pTimeValues[0]) {
      currTimeIndex = 0;
    } else if (t >= pTimeValues[7]) {
      currTimeIndex = 6;
    } else {
      if (t < pTimeValues[currTimeIndex]) {
        while (t < pTimeValues[currTimeIndex]) {
          currTimeIndex--;
        }
      } else {
        while (t >= pTimeValues[currTimeIndex + 1]) {
          currTimeIndex++;
        }
      }
    }

    Real_Time_Simulation_Corr_DWork.FromWs_IWORK.PrevIndex = currTimeIndex;

    /* Post output */
    {
      real_T t1 = pTimeValues[currTimeIndex];
      real_T t2 = pTimeValues[currTimeIndex + 1];
      if (t1 == t2) {
        if (t < t1) {
          rtb_Saturation3 = pDataValues[currTimeIndex];
        } else {
          rtb_Saturation3 = pDataValues[currTimeIndex + 1];
        }
      } else {
        real_T f1 = (t2 - t) / (t2 - t1);
        real_T f2 = 1.0 - f1;
        real_T d1;
        real_T d2;
        int_T TimeIndex= currTimeIndex;
        d1 = pDataValues[TimeIndex];
        d2 = pDataValues[TimeIndex + 1];
        rtb_Saturation3 = (real_T) rtInterpolate(d1, d2, f1, f2);
        pDataValues += 8;
      }
    }
  }

  /* ManualSwitch: '<Root>/Manual Switch' incorporates:
   *  Constant: '<Root>/Constant'
   */
  if (Real_Time_Simulation_Correcti_P.ManualSwitch_CurrentSetting == 1) {
    rtb_Saturation3 = Real_Time_Simulation_Correcti_P.Constant_Value;
  }

  /* End of ManualSwitch: '<Root>/Manual Switch' */

  /* Sum: '<Root>/Sum' incorporates:
   *  Gain: '<Root>/Gain1'
   *  Gain: '<Root>/Gain2'
   *  UnitDelay: '<Root>/Unit Delay'
   */
  Real_Time_Simulation_Correcti_B.Sum =
    Real_Time_Simulation_Correcti_P.Gain1_Gain_cpx4lbewpy * rtb_Saturation3 -
    (((Real_Time_Simulation_Correcti_P.Gain2_Gain_ezbw1uq0ur[0] *
       Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE[0] +
       Real_Time_Simulation_Correcti_P.Gain2_Gain_ezbw1uq0ur[1] *
       Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE[1]) +
      Real_Time_Simulation_Correcti_P.Gain2_Gain_ezbw1uq0ur[2] *
      Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE[2]) +
     Real_Time_Simulation_Correcti_P.Gain2_Gain_ezbw1uq0ur[3] *
     Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE[3]);

  /* S-Function (ev3_gyro_sensor): '<S1>/Gyro Sensor1' */
  rtb_Encoder1_0 = getGyroSensorValue(4U);

  /* Switch: '<S21>/Switch1' incorporates:
   *  Constant: '<S21>/Constant6'
   *  Constant: '<S6>/Constant5'
   *  Constant: '<S6>/Constant6'
   *  Switch: '<S21>/Switch3'
   */
  if (Real_Time_Simulation_Correcti_P.Constant6_Value_hyqvqn5fwb != 0.0F) {
    Real_Time_Simulation_Correcti_B.counter_value =
      Real_Time_Simulation_Correcti_P.Constant6_Value;
  } else {
    if (Real_Time_Simulation_Correcti_P.Constant5_Value_jhrxeiwmg5 != 0.0F) {
      /* Switch: '<S21>/Switch3' incorporates:
       *  Constant: '<S6>/Constant7'
       */
      u0 = Real_Time_Simulation_Correcti_P.Constant7_Value;
    } else {
      /* Switch: '<S21>/Switch3' incorporates:
       *  Constant: '<S21>/Constant5'
       */
      u0 = Real_Time_Simulation_Correcti_P.Constant5_Value;
    }

    /* Sum: '<S21>/Sum' incorporates:
     *  UnitDelay: '<S21>/UnitDelay3'
     */
    u0 += Real_Time_Simulation_Corr_DWork.UnitDelay3_DSTATE;

    /* MinMax: '<S21>/MinMax' incorporates:
     *  Constant: '<S6>/Constant8'
     */
    if ((u0 < Real_Time_Simulation_Correcti_P.Constant8_Value) || rtIsNaNF
        (Real_Time_Simulation_Correcti_P.Constant8_Value)) {
      Real_Time_Simulation_Correcti_B.counter_value = u0;
    } else {
      Real_Time_Simulation_Correcti_B.counter_value =
        Real_Time_Simulation_Correcti_P.Constant8_Value;
    }

    /* End of MinMax: '<S21>/MinMax' */
  }

  /* End of Switch: '<S21>/Switch1' */

  /* RelationalOperator: '<S4>/Compare' incorporates:
   *  Constant: '<S4>/Constant'
   */
  Compare = (Real_Time_Simulation_Correcti_B.counter_value >=
             Real_Time_Simulation_Correcti_P.time_start);

  /* Outputs for Enabled SubSystem: '<S1>/Gyro Calibration' incorporates:
   *  EnablePort: '<S5>/Enable'
   */
  /* Logic: '<S1>/Logical Operator' */
  if (!Compare) {
    if (1) {
      /* Sum: '<S5>/Sum1' incorporates:
       *  DataTypeConversion: '<S1>/Data Type Conversion4'
       *  Gain: '<S5>/Gain2'
       *  Gain: '<S5>/Gain3'
       *  S-Function (ev3_gyro_sensor): '<S1>/Gyro Sensor1'
       *  UnitDelay: '<S5>/Unit Delay'
       */
      Real_Time_Simulation_Correcti_B.Sum1 =
        Real_Time_Simulation_Correcti_P.Gain2_Gain * (real32_T)rtb_Encoder1_0 +
        Real_Time_Simulation_Correcti_P.a_gc *
        Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_cfkvxtl130;
    }

    if (Real_Time_Simulation_Correct_M->Timing.TaskCounters.TID[2] == 0) {
      /* S-Function (ev3_speaker): '<S20>/Speaker' incorporates:
       *  Constant: '<S5>/Constant'
       */
      playSoundFreqOnly
        (Real_Time_Simulation_Correcti_P.Constant_Value_aljrxhz2pj,
         Real_Time_Simulation_Correcti_P.Speaker_speakerVolume,
         Real_Time_Simulation_Correcti_P.Speaker_p4);
    }

    if (1) {
      /* Update for UnitDelay: '<S5>/Unit Delay' */
      Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_cfkvxtl130 =
        Real_Time_Simulation_Correcti_B.Sum1;
    }

    srUpdateBC(Real_Time_Simulation_Corr_DWork.GyroCalibration_SubsysRanBC);
  }

  /* End of Logic: '<S1>/Logical Operator' */
  /* End of Outputs for SubSystem: '<S1>/Gyro Calibration' */

  /* S-Function (ev3_encoder): '<S1>/Encoder' */
  rtb_Encoder1_1 = getEncoderValueNoReset(2U);

  /* S-Function (ev3_encoder): '<S1>/Encoder1' */
  rtb_Encoder1_2 = getEncoderValueNoReset(3U);

  /* DiscreteFilter: '<S1>/Discrete Filter' incorporates:
   *  Constant: '<S1>/Constant4'
   */
  Real_Time_Simulation_Corr_DWork.DiscreteFilter_tmp =
    (Real_Time_Simulation_Correcti_P.BATTERY -
     Real_Time_Simulation_Correcti_P.DiscreteFilter_DenCoef[1] *
     Real_Time_Simulation_Corr_DWork.DiscreteFilter_states) /
    Real_Time_Simulation_Correcti_P.DiscreteFilter_DenCoef[0];

  /* Outputs for Enabled SubSystem: '<S1>/Balance and Drive Control' incorporates:
   *  EnablePort: '<S3>/Enable'
   */
  Real_Time_Simulation_Corr_DWork.BalanceandDriveControl_MODE = Compare;
  if (Real_Time_Simulation_Corr_DWork.BalanceandDriveControl_MODE) {
    /* UnitDelay: '<S17>/Unit Delay' */
    Real_Time_Simulation_Correcti_B.UnitDelay =
      Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_hzuovbre5y;

    /* Stop: '<S3>/Stop Simulation' incorporates:
     *  Abs: '<S3>/Abs'
     *  Constant: '<S9>/Constant'
     *  RelationalOperator: '<S9>/Compare'
     */
    if ((real32_T)fabs(Real_Time_Simulation_Correcti_B.UnitDelay) >=
        Real_Time_Simulation_Correcti_P.CompareToConstant1_const) {
      rtmSetStopRequested(Real_Time_Simulation_Correct_M, 1);
    }

    /* End of Stop: '<S3>/Stop Simulation' */

    /* Switch: '<S19>/Init' incorporates:
     *  UnitDelay: '<S19>/FixPt Unit Delay1'
     *  UnitDelay: '<S19>/FixPt Unit Delay2'
     */
    if (Real_Time_Simulation_Corr_DWork.FixPtUnitDelay2_DSTATE != 0) {
      u0 = Real_Time_Simulation_Correcti_B.Sum1;
    } else {
      u0 = Real_Time_Simulation_Corr_DWork.FixPtUnitDelay1_DSTATE;
    }

    /* End of Switch: '<S19>/Init' */

    /* Sum: '<S15>/Sum2' incorporates:
     *  DataTypeConversion: '<S1>/Data Type Conversion4'
     *  Gain: '<S15>/Gain1'
     *  Gain: '<S15>/Gain4'
     *  S-Function (ev3_gyro_sensor): '<S1>/Gyro Sensor1'
     */
    rtb_Sum2 = Real_Time_Simulation_Correcti_P.Gain1_Gain_j0r0df4nzm * (real32_T)
      rtb_Encoder1_0 + Real_Time_Simulation_Correcti_P.a_gd * u0;

    /* Gain: '<S8>/Gain' incorporates:
     *  DataTypeConversion: '<S1>/Data Type Conversion1'
     *  DataTypeConversion: '<S1>/Data Type Conversion3'
     *  Gain: '<S8>/deg2rad'
     *  Gain: '<S8>/deg2rad1'
     *  S-Function (ev3_encoder): '<S1>/Encoder'
     *  S-Function (ev3_encoder): '<S1>/Encoder1'
     *  Sum: '<S8>/Sum1'
     *  Sum: '<S8>/Sum4'
     *  Sum: '<S8>/Sum6'
     */
    Real_Time_Simulation_Correcti_B.Gain =
      ((Real_Time_Simulation_Correcti_P.deg2rad_Gain * (real32_T)rtb_Encoder1_1
        + Real_Time_Simulation_Correcti_B.UnitDelay) +
       (Real_Time_Simulation_Correcti_P.deg2rad1_Gain * (real32_T)rtb_Encoder1_2
        + Real_Time_Simulation_Correcti_B.UnitDelay)) *
      Real_Time_Simulation_Correcti_P.Gain_Gain;

    /* Sum: '<S18>/Sum' incorporates:
     *  Gain: '<S18>/Gain2'
     *  Gain: '<S18>/Gain3'
     *  UnitDelay: '<S18>/Unit Delay'
     */
    rtb_Sum = Real_Time_Simulation_Correcti_P.Gain3_Gain_hka0xvmyzz *
      Real_Time_Simulation_Correcti_B.Gain + Real_Time_Simulation_Correcti_P.a_d
      * Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_orvhqhlbcp;

    /* Gain: '<S16>/Gain' incorporates:
     *  Sum: '<S16>/Sum'
     *  UnitDelay: '<S16>/Unit Delay'
     */
    Real_Time_Simulation_Correcti_B.Gain_oopwalytwu = (rtb_Sum -
      Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_mjna1kxy33) *
      Real_Time_Simulation_Correcti_P.Gain_Gain_bwkvwsewsv;

    /* Gain: '<S8>/deg2rad2' incorporates:
     *  DataTypeConversion: '<S1>/Data Type Conversion4'
     *  S-Function (ev3_gyro_sensor): '<S1>/Gyro Sensor1'
     *  Sum: '<S8>/Sum2'
     */
    Real_Time_Simulation_Correcti_B.psidot = ((real32_T)rtb_Encoder1_0 -
      rtb_Sum2) * Real_Time_Simulation_Correcti_P.deg2rad2_Gain;

    /* Sum: '<S17>/Sum' incorporates:
     *  Gain: '<S17>/Gain'
     */
    rtb_Sum_nvdedzgoqp = Real_Time_Simulation_Correcti_P.ts1 *
      Real_Time_Simulation_Correcti_B.psidot +
      Real_Time_Simulation_Correcti_B.UnitDelay;

    /* Product: '<S7>/Product1' incorporates:
     *  Constant: '<S12>/Constant'
     *  DiscreteFilter: '<S1>/Discrete Filter'
     *  Gain: '<S12>/Gain3'
     *  Product: '<S7>/Product2'
     *  Sum: '<S12>/Sum2'
     */
    rtb_Saturation3_tmp = Real_Time_Simulation_Correcti_B.Sum /
      (Real_Time_Simulation_Correcti_P.DiscreteFilter_NumCoef *
       Real_Time_Simulation_Corr_DWork.DiscreteFilter_tmp *
       Real_Time_Simulation_Correcti_P.Gain3_Gain_gjv3wryppp -
       Real_Time_Simulation_Correcti_P.Constant_Value_kzvkk53bcx);
    rtb_Saturation3 = rtb_Saturation3_tmp;

    /* Gain: '<S7>/Gain1' */
    rtb_Saturation3 *= Real_Time_Simulation_Correcti_P.Gain1_Gain;

    /* Signum: '<S13>/Sign' */
    if (rtb_Saturation3 < 0.0) {
      tmp_0 = -1.0;
    } else if (rtb_Saturation3 > 0.0) {
      tmp_0 = 1.0;
    } else if (rtb_Saturation3 == 0.0) {
      tmp_0 = 0.0;
    } else {
      tmp_0 = (rtNaN);
    }

    /* End of Signum: '<S13>/Sign' */

    /* Sum: '<S13>/Sum' incorporates:
     *  Gain: '<S13>/Gain'
     *  Gain: '<S13>/Gain1'
     */
    rtb_Saturation3 = Real_Time_Simulation_Correcti_P.pwm_offset * tmp_0 +
      Real_Time_Simulation_Correcti_P.pwm_gain * rtb_Saturation3;

    /* Saturate: '<S7>/Saturation2' */
    if (rtb_Saturation3 > Real_Time_Simulation_Correcti_P.Saturation2_UpperSat)
    {
      rtb_Saturation3 = Real_Time_Simulation_Correcti_P.Saturation2_UpperSat;
    } else {
      if (rtb_Saturation3 < Real_Time_Simulation_Correcti_P.Saturation2_LowerSat)
      {
        rtb_Saturation3 = Real_Time_Simulation_Correcti_P.Saturation2_LowerSat;
      }
    }

    /* End of Saturate: '<S7>/Saturation2' */

    /* DataTypeConversion: '<S10>/Data Type Conversion' */
    tmp_0 = floor(rtb_Saturation3);
    if (tmp_0 < 128.0) {
      if (tmp_0 >= -128.0) {
        /* S-Function (ev3_motor): '<S10>/Motor' */
        tmp = (int8_T)tmp_0;
      } else {
        /* S-Function (ev3_motor): '<S10>/Motor' */
        tmp = MIN_int8_T;
      }
    } else {
      /* S-Function (ev3_motor): '<S10>/Motor' */
      tmp = MAX_int8_T;
    }

    /* End of DataTypeConversion: '<S10>/Data Type Conversion' */

    /* S-Function (ev3_motor): '<S10>/Motor' */
    setMotor(&tmp, 2U, 2U);

    /* Product: '<S7>/Product2' */
    rtb_Saturation3 = rtb_Saturation3_tmp;

    /* Gain: '<S7>/Gain3' */
    rtb_Saturation3 *= Real_Time_Simulation_Correcti_P.Gain3_Gain;

    /* Signum: '<S14>/Sign' */
    if (rtb_Saturation3 < 0.0) {
      tmp_0 = -1.0;
    } else if (rtb_Saturation3 > 0.0) {
      tmp_0 = 1.0;
    } else if (rtb_Saturation3 == 0.0) {
      tmp_0 = 0.0;
    } else {
      tmp_0 = (rtNaN);
    }

    /* End of Signum: '<S14>/Sign' */

    /* Sum: '<S14>/Sum' incorporates:
     *  Gain: '<S14>/Gain'
     *  Gain: '<S14>/Gain1'
     */
    rtb_Saturation3 = Real_Time_Simulation_Correcti_P.pwm_offset * tmp_0 +
      Real_Time_Simulation_Correcti_P.pwm_gain * rtb_Saturation3;

    /* Saturate: '<S7>/Saturation3' */
    if (rtb_Saturation3 > Real_Time_Simulation_Correcti_P.Saturation3_UpperSat)
    {
      rtb_Saturation3 = Real_Time_Simulation_Correcti_P.Saturation3_UpperSat;
    } else {
      if (rtb_Saturation3 < Real_Time_Simulation_Correcti_P.Saturation3_LowerSat)
      {
        rtb_Saturation3 = Real_Time_Simulation_Correcti_P.Saturation3_LowerSat;
      }
    }

    /* End of Saturate: '<S7>/Saturation3' */

    /* DataTypeConversion: '<S11>/Data Type Conversion' */
    tmp_0 = floor(rtb_Saturation3);
    if (tmp_0 < 128.0) {
      if (tmp_0 >= -128.0) {
        /* S-Function (ev3_motor): '<S11>/Motor' */
        tmp = (int8_T)tmp_0;
      } else {
        /* S-Function (ev3_motor): '<S11>/Motor' */
        tmp = MIN_int8_T;
      }
    } else {
      /* S-Function (ev3_motor): '<S11>/Motor' */
      tmp = MAX_int8_T;
    }

    /* End of DataTypeConversion: '<S11>/Data Type Conversion' */

    /* S-Function (ev3_motor): '<S11>/Motor' */
    setMotor(&tmp, 3U, 2U);
    srUpdateBC(Real_Time_Simulation_Corr_DWork.BalanceandDriveControl_SubsysRa);
  }

  /* End of Outputs for SubSystem: '<S1>/Balance and Drive Control' */

  /* Update for UnitDelay: '<Root>/Unit Delay' */
  Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE[0] =
    Real_Time_Simulation_Correcti_B.Gain;
  Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE[1] =
    Real_Time_Simulation_Correcti_B.UnitDelay;
  Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE[2] =
    Real_Time_Simulation_Correcti_B.Gain_oopwalytwu;
  Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE[3] =
    Real_Time_Simulation_Correcti_B.psidot;

  /* Update for UnitDelay: '<S21>/UnitDelay3' */
  Real_Time_Simulation_Corr_DWork.UnitDelay3_DSTATE =
    Real_Time_Simulation_Correcti_B.counter_value;

  /* Update for DiscreteFilter: '<S1>/Discrete Filter' */
  Real_Time_Simulation_Corr_DWork.DiscreteFilter_states =
    Real_Time_Simulation_Corr_DWork.DiscreteFilter_tmp;

  /* Update for Enabled SubSystem: '<S1>/Balance and Drive Control' incorporates:
   *  EnablePort: '<S3>/Enable'
   */
  if (Real_Time_Simulation_Corr_DWork.BalanceandDriveControl_MODE) {
    /* Update for UnitDelay: '<S17>/Unit Delay' */
    Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_hzuovbre5y =
      rtb_Sum_nvdedzgoqp;

    /* Update for UnitDelay: '<S19>/FixPt Unit Delay2' incorporates:
     *  Constant: '<S19>/FixPt Constant'
     */
    Real_Time_Simulation_Corr_DWork.FixPtUnitDelay2_DSTATE =
      Real_Time_Simulation_Correcti_P.FixPtConstant_Value;

    /* Update for UnitDelay: '<S19>/FixPt Unit Delay1' */
    Real_Time_Simulation_Corr_DWork.FixPtUnitDelay1_DSTATE = rtb_Sum2;

    /* Update for UnitDelay: '<S18>/Unit Delay' */
    Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_orvhqhlbcp = rtb_Sum;

    /* Update for UnitDelay: '<S16>/Unit Delay' */
    Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_mjna1kxy33 = rtb_Sum;
  }

  /* End of Update for SubSystem: '<S1>/Balance and Drive Control' */

  /* External mode */
  rtExtModeUploadCheckTrigger(3);

  {                                    /* Sample time: [0.0s, 0.0s] */
    rtExtModeUpload(0, (real_T)Real_Time_Simulation_Correct_M->Timing.t[0]);
  }

  {                                    /* Sample time: [0.004s, 0.0s] */
    rtExtModeUpload(1, (real_T)
                    (((Real_Time_Simulation_Correct_M->Timing.clockTick1+
                       Real_Time_Simulation_Correct_M->Timing.clockTickH1*
                       4294967296.0)) * 0.004));
  }

  if (Real_Time_Simulation_Correct_M->Timing.TaskCounters.TID[2] == 0) {/* Sample time: [0.2s, 0.0s] */
    rtExtModeUpload(2, (real_T)
                    (((Real_Time_Simulation_Correct_M->Timing.clockTick2+
                       Real_Time_Simulation_Correct_M->Timing.clockTickH2*
                       4294967296.0)) * 0.2));
  }

  /* signal main to stop simulation */
  {                                    /* Sample time: [0.0s, 0.0s] */
    if ((rtmGetTFinal(Real_Time_Simulation_Correct_M)!=-1) &&
        !((rtmGetTFinal(Real_Time_Simulation_Correct_M)-
           Real_Time_Simulation_Correct_M->Timing.t[0]) >
          Real_Time_Simulation_Correct_M->Timing.t[0] * (DBL_EPSILON))) {
      rtmSetErrorStatus(Real_Time_Simulation_Correct_M, "Simulation finished");
    }

    if (rtmGetStopRequested(Real_Time_Simulation_Correct_M)) {
      rtmSetErrorStatus(Real_Time_Simulation_Correct_M, "Simulation finished");
    }
  }

  /* Update absolute time for base rate */
  /* The "clockTick0" counts the number of times the code of this task has
   * been executed. The absolute time is the multiplication of "clockTick0"
   * and "Timing.stepSize0". Size of "clockTick0" ensures timer will not
   * overflow during the application lifespan selected.
   * Timer of this task consists of two 32 bit unsigned integers.
   * The two integers represent the low bits Timing.clockTick0 and the high bits
   * Timing.clockTickH0. When the low bit overflows to 0, the high bits increment.
   */
  if (!(++Real_Time_Simulation_Correct_M->Timing.clockTick0)) {
    ++Real_Time_Simulation_Correct_M->Timing.clockTickH0;
  }

  Real_Time_Simulation_Correct_M->Timing.t[0] =
    Real_Time_Simulation_Correct_M->Timing.clockTick0 *
    Real_Time_Simulation_Correct_M->Timing.stepSize0 +
    Real_Time_Simulation_Correct_M->Timing.clockTickH0 *
    Real_Time_Simulation_Correct_M->Timing.stepSize0 * 4294967296.0;

  {
    /* Update absolute timer for sample time: [0.004s, 0.0s] */
    /* The "clockTick1" counts the number of times the code of this task has
     * been executed. The resolution of this integer timer is 0.004, which is the step size
     * of the task. Size of "clockTick1" ensures timer will not overflow during the
     * application lifespan selected.
     * Timer of this task consists of two 32 bit unsigned integers.
     * The two integers represent the low bits Timing.clockTick1 and the high bits
     * Timing.clockTickH1. When the low bit overflows to 0, the high bits increment.
     */
    Real_Time_Simulation_Correct_M->Timing.clockTick1++;
    if (!Real_Time_Simulation_Correct_M->Timing.clockTick1) {
      Real_Time_Simulation_Correct_M->Timing.clockTickH1++;
    }
  }

  if (Real_Time_Simulation_Correct_M->Timing.TaskCounters.TID[2] == 0) {
    /* Update absolute timer for sample time: [0.2s, 0.0s] */
    /* The "clockTick2" counts the number of times the code of this task has
     * been executed. The resolution of this integer timer is 0.2, which is the step size
     * of the task. Size of "clockTick2" ensures timer will not overflow during the
     * application lifespan selected.
     * Timer of this task consists of two 32 bit unsigned integers.
     * The two integers represent the low bits Timing.clockTick2 and the high bits
     * Timing.clockTickH2. When the low bit overflows to 0, the high bits increment.
     */
    Real_Time_Simulation_Correct_M->Timing.clockTick2++;
    if (!Real_Time_Simulation_Correct_M->Timing.clockTick2) {
      Real_Time_Simulation_Correct_M->Timing.clockTickH2++;
    }
  }

  rate_scheduler();
}

/* Model initialize function */
void Real_Time_Simulation_Correction_initialize(void)
{
  /* Registration code */

  /* initialize non-finites */
  rt_InitInfAndNaN(sizeof(real_T));

  /* initialize real-time model */
  (void) memset((void *)Real_Time_Simulation_Correct_M, 0,
                sizeof(RT_MODEL_Real_Time_Simulation_C));

  {
    /* Setup solver object */
    rtsiSetSimTimeStepPtr(&Real_Time_Simulation_Correct_M->solverInfo,
                          &Real_Time_Simulation_Correct_M->Timing.simTimeStep);
    rtsiSetTPtr(&Real_Time_Simulation_Correct_M->solverInfo, &rtmGetTPtr
                (Real_Time_Simulation_Correct_M));
    rtsiSetStepSizePtr(&Real_Time_Simulation_Correct_M->solverInfo,
                       &Real_Time_Simulation_Correct_M->Timing.stepSize0);
    rtsiSetErrorStatusPtr(&Real_Time_Simulation_Correct_M->solverInfo,
                          (&rtmGetErrorStatus(Real_Time_Simulation_Correct_M)));
    rtsiSetRTModelPtr(&Real_Time_Simulation_Correct_M->solverInfo,
                      Real_Time_Simulation_Correct_M);
  }

  rtsiSetSimTimeStep(&Real_Time_Simulation_Correct_M->solverInfo,
                     MAJOR_TIME_STEP);
  rtsiSetSolverName(&Real_Time_Simulation_Correct_M->solverInfo,
                    "FixedStepDiscrete");
  rtmSetTPtr(Real_Time_Simulation_Correct_M,
             &Real_Time_Simulation_Correct_M->Timing.tArray[0]);
  rtmSetTFinal(Real_Time_Simulation_Correct_M, -1);
  Real_Time_Simulation_Correct_M->Timing.stepSize0 = 0.004;

  /* External mode info */
  Real_Time_Simulation_Correct_M->Sizes.checksums[0] = (2855760259U);
  Real_Time_Simulation_Correct_M->Sizes.checksums[1] = (2959079637U);
  Real_Time_Simulation_Correct_M->Sizes.checksums[2] = (1713522580U);
  Real_Time_Simulation_Correct_M->Sizes.checksums[3] = (2605490048U);

  {
    static const sysRanDType rtAlwaysEnabled = SUBSYS_RAN_BC_ENABLE;
    static RTWExtModeInfo rt_ExtModeInfo;
    static const sysRanDType *systemRan[6];
    Real_Time_Simulation_Correct_M->extModeInfo = (&rt_ExtModeInfo);
    rteiSetSubSystemActiveVectorAddresses(&rt_ExtModeInfo, systemRan);
    systemRan[0] = &rtAlwaysEnabled;
    systemRan[1] = (sysRanDType *)
      &Real_Time_Simulation_Corr_DWork.BalanceandDriveControl_SubsysRa;
    systemRan[2] = (sysRanDType *)
      &Real_Time_Simulation_Corr_DWork.GyroCalibration_SubsysRanBC;
    systemRan[3] = &rtAlwaysEnabled;
    systemRan[4] = &rtAlwaysEnabled;
    systemRan[5] = &rtAlwaysEnabled;
    rteiSetModelMappingInfoPtr(Real_Time_Simulation_Correct_M->extModeInfo,
      &Real_Time_Simulation_Correct_M->SpecialInfo.mappingInfo);
    rteiSetChecksumsPtr(Real_Time_Simulation_Correct_M->extModeInfo,
                        Real_Time_Simulation_Correct_M->Sizes.checksums);
    rteiSetTPtr(Real_Time_Simulation_Correct_M->extModeInfo, rtmGetTPtr
                (Real_Time_Simulation_Correct_M));
  }

  /* block I/O */
  (void) memset(((void *) &Real_Time_Simulation_Correcti_B), 0,
                sizeof(BlockIO_Real_Time_Simulation_Co));

  /* states (dwork) */
  (void) memset((void *)&Real_Time_Simulation_Corr_DWork, 0,
                sizeof(D_Work_Real_Time_Simulation_Cor));

  /* data type transition information */
  {
    static DataTypeTransInfo dtInfo;
    (void) memset((char_T *) &dtInfo, 0,
                  sizeof(dtInfo));
    Real_Time_Simulation_Correct_M->SpecialInfo.mappingInfo = (&dtInfo);
    dtInfo.numDataTypes = 14;
    dtInfo.dataTypeSizes = &rtDataTypeSizes[0];
    dtInfo.dataTypeNames = &rtDataTypeNames[0];

    /* Block I/O transition table */
    dtInfo.BTransTable = &rtBTransTable;

    /* Parameters transition table */
    dtInfo.PTransTable = &rtPTransTable;
  }

  /* Start for FromWorkspace: '<S2>/FromWs' */
  {
    static real_T pTimeValues0[] = { 0.0, 10.0, 12.0, 12.0, 140.0, 140.0, 188.5,
      200.0 } ;

    static real_T pDataValues0[] = { -0.0, -0.0, -0.0, -0.0, 84.0, 84.0, 84.0,
      84.0 } ;

    Real_Time_Simulation_Corr_DWork.FromWs_PWORK.TimePtr = (void *) pTimeValues0;
    Real_Time_Simulation_Corr_DWork.FromWs_PWORK.DataPtr = (void *) pDataValues0;
    Real_Time_Simulation_Corr_DWork.FromWs_IWORK.PrevIndex = 0;
  }

  /* Start for S-Function (ev3_gyro_sensor): '<S1>/Gyro Sensor1' */
  initGyroSensor(4U);

  /* Start for Enabled SubSystem: '<S1>/Gyro Calibration' */
  /* Start for S-Function (ev3_speaker): '<S20>/Speaker' */
  initSpeaker();

  /* End of Start for SubSystem: '<S1>/Gyro Calibration' */

  /* Start for S-Function (ev3_encoder): '<S1>/Encoder' */
  initEncoder(2U);

  /* Start for S-Function (ev3_encoder): '<S1>/Encoder1' */
  initEncoder(3U);

  /* Start for Enabled SubSystem: '<S1>/Balance and Drive Control' */
  /* Start for S-Function (ev3_motor): '<S10>/Motor' */
  initMotor(2U);

  /* Start for S-Function (ev3_motor): '<S11>/Motor' */
  initMotor(3U);

  /* End of Start for SubSystem: '<S1>/Balance and Drive Control' */

  /* InitializeConditions for UnitDelay: '<Root>/Unit Delay' */
  Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE[0] =
    Real_Time_Simulation_Correcti_P.UnitDelay_InitialCon_g5o4mik1am[0];
  Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE[1] =
    Real_Time_Simulation_Correcti_P.UnitDelay_InitialCon_g5o4mik1am[1];
  Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE[2] =
    Real_Time_Simulation_Correcti_P.UnitDelay_InitialCon_g5o4mik1am[2];
  Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE[3] =
    Real_Time_Simulation_Correcti_P.UnitDelay_InitialCon_g5o4mik1am[3];

  /* InitializeConditions for UnitDelay: '<S21>/UnitDelay3' */
  Real_Time_Simulation_Corr_DWork.UnitDelay3_DSTATE =
    Real_Time_Simulation_Correcti_P.UnitDelay3_InitialCondition;

  /* InitializeConditions for DiscreteFilter: '<S1>/Discrete Filter' */
  Real_Time_Simulation_Corr_DWork.DiscreteFilter_states =
    Real_Time_Simulation_Correcti_P.DiscreteFilter_InitialStates;

  /* SystemInitialize for Enabled SubSystem: '<S1>/Gyro Calibration' */
  /* InitializeConditions for UnitDelay: '<S5>/Unit Delay' */
  Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_cfkvxtl130 =
    Real_Time_Simulation_Correcti_P.UnitDelay_InitialCon_egsil4m2ui;

  /* End of SystemInitialize for SubSystem: '<S1>/Gyro Calibration' */

  /* SystemInitialize for Enabled SubSystem: '<S1>/Balance and Drive Control' */
  /* InitializeConditions for UnitDelay: '<S17>/Unit Delay' */
  Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_hzuovbre5y =
    Real_Time_Simulation_Correcti_P.UnitDelay_InitialCondition;

  /* InitializeConditions for UnitDelay: '<S19>/FixPt Unit Delay2' */
  Real_Time_Simulation_Corr_DWork.FixPtUnitDelay2_DSTATE =
    Real_Time_Simulation_Correcti_P.FixPtUnitDelay2_InitialConditio;

  /* InitializeConditions for UnitDelay: '<S19>/FixPt Unit Delay1' */
  Real_Time_Simulation_Corr_DWork.FixPtUnitDelay1_DSTATE =
    Real_Time_Simulation_Correcti_P.FixPtUnitDelay1_InitialConditio;

  /* InitializeConditions for UnitDelay: '<S18>/Unit Delay' */
  Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_orvhqhlbcp =
    Real_Time_Simulation_Correcti_P.UnitDelay_InitialCon_bijcdbwmgf;

  /* InitializeConditions for UnitDelay: '<S16>/Unit Delay' */
  Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_mjna1kxy33 =
    Real_Time_Simulation_Correcti_P.UnitDelay_InitialCon_azw54opzqy;

  /* End of SystemInitialize for SubSystem: '<S1>/Balance and Drive Control' */
}

/* Model terminate function */
void Real_Time_Simulation_Correction_terminate(void)
{
  /* Terminate for S-Function (ev3_gyro_sensor): '<S1>/Gyro Sensor1' */
  terminateGyroSensor(4U);

  /* Terminate for Enabled SubSystem: '<S1>/Gyro Calibration' */
  /* Terminate for S-Function (ev3_speaker): '<S20>/Speaker' */
  terminateSpeaker();

  /* End of Terminate for SubSystem: '<S1>/Gyro Calibration' */

  /* Terminate for S-Function (ev3_encoder): '<S1>/Encoder' */
  terminateEncoder(2U);

  /* Terminate for S-Function (ev3_encoder): '<S1>/Encoder1' */
  terminateEncoder(3U);

  /* Terminate for Enabled SubSystem: '<S1>/Balance and Drive Control' */
  /* Terminate for S-Function (ev3_motor): '<S10>/Motor' */
  terminateMotor(2U, 2U);

  /* Terminate for S-Function (ev3_motor): '<S11>/Motor' */
  terminateMotor(3U, 2U);

  /* End of Terminate for SubSystem: '<S1>/Balance and Drive Control' */
}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */

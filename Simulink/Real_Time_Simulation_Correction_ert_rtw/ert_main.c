/*
 * Classroom License -- for classroom instructional use only.  Not for
 * government, commercial, academic research, or other organizational use.
 *
 * File: ert_main.c
 *
 * Code generated for Simulink model 'Real_Time_Simulation_Correction'.
 *
 * Model version                  : 1.917
 * Simulink Coder version         : 9.3 (R2020a) 18-Nov-2019
 * C/C++ source code generated on : Mon Jul 20 17:04:39 2026
 *
 * Target selection: ert.tlc
 * Embedded hardware selection: ARM Compatible->ARM 9
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include <stdio.h>
#include <stdlib.h>
#include "Real_Time_Simulation_Correction.h"
#include "Real_Time_Simulation_Correction_private.h"
#include "rtwtypes.h"
#include "limits.h"
#include "rt_nonfinite.h"
#include "driver_ev3.h"
#include "ev3_constants.h"
#include "ev3_include.h"
#include "lms2012.h"
#include "linuxinitialize.h"
#define UNUSED(x)                      x = x
#define NAMELEN                        16

/* Function prototype declaration*/
void exitFcn(int sig);
void *terminateTask(void *arg);
void *baseRateTask(void *arg);
void *subrateTask(void *arg);
volatile boolean_T stopRequested = false;
volatile boolean_T runModel = true;
sem_t stopSem;
sem_t baserateTaskSem;
pthread_t schedulerThread;
pthread_t baseRateThread;
pthread_t backgroundThread;
void *threadJoinStatus;
int terminatingmodel = 0;
void *baseRateTask(void *arg)
{
  runModel = (rtmGetErrorStatus(Real_Time_Simulation_Correct_M) == (NULL)) &&
    !rtmGetStopRequested(Real_Time_Simulation_Correct_M);
  while (runModel) {
    sem_wait(&baserateTaskSem);

    /* External mode */
    {
      boolean_T rtmStopReq = false;
      rtExtModePauseIfNeeded(Real_Time_Simulation_Correct_M->extModeInfo, 3,
        &rtmStopReq);
      if (rtmStopReq) {
        rtmSetStopRequested(Real_Time_Simulation_Correct_M, true);
      }

      if (rtmGetStopRequested(Real_Time_Simulation_Correct_M) == true) {
        rtmSetErrorStatus(Real_Time_Simulation_Correct_M, "Simulation finished");
        break;
      }
    }

    Real_Time_Simulation_Correction_step();

    /* Get model outputs here */
    rtExtModeCheckEndTrigger();
    stopRequested = !((rtmGetErrorStatus(Real_Time_Simulation_Correct_M) ==
                       (NULL)) && !rtmGetStopRequested
                      (Real_Time_Simulation_Correct_M));
    runModel = !stopRequested;
    runModel = runModel && !getBackButtonValue();
  }

  runModel = 0;
  terminateTask(arg);
  pthread_exit((void *)0);
  return NULL;
}

void exitFcn(int sig)
{
  UNUSED(sig);
  rtmSetErrorStatus(Real_Time_Simulation_Correct_M, "stopping the model");
}

void *terminateTask(void *arg)
{
  UNUSED(arg);
  terminatingmodel = 1;

  {
    runModel = 0;

    /* Wait for background task to complete */
    CHECK_STATUS(pthread_join(backgroundThread, &threadJoinStatus), 0,
                 "pthread_join");
  }

  MW_legoev3_terminatetasks();

  /* Disable rt_OneStep() here */

  /* Terminate model */
  Real_Time_Simulation_Correction_terminate();
  rtExtModeShutdown(3);
  sem_post(&stopSem);
  return NULL;
}

void *backgroundTask(void *arg)
{
  while (runModel) {
    /* External mode */
    {
      boolean_T rtmStopReq = false;
      rtExtModeOneStep(Real_Time_Simulation_Correct_M->extModeInfo, 3,
                       &rtmStopReq);
      if (rtmStopReq) {
        rtmSetStopRequested(Real_Time_Simulation_Correct_M, true);
      }
    }
  }

  return NULL;
}

int main(int argc, char **argv)
{
  UNUSED(argc);
  UNUSED(argv);
  MW_ev3_init();
  rtmSetErrorStatus(Real_Time_Simulation_Correct_M, 0);
  rtExtModeParseArgs(argc, (const char_T **)argv, NULL);

  /* Initialize model */
  Real_Time_Simulation_Correction_initialize();

  /* External mode */
  rtSetTFinalForExtMode(&rtmGetTFinal(Real_Time_Simulation_Correct_M));
  rtExtModeCheckInit(3);

  {
    boolean_T rtmStopReq = false;
    rtExtModeWaitForStartPkt(Real_Time_Simulation_Correct_M->extModeInfo, 3,
      &rtmStopReq);
    if (rtmStopReq) {
      rtmSetStopRequested(Real_Time_Simulation_Correct_M, true);
    }
  }

  rtERTExtModeStartMsg();

  /* Call RTOS Initialization function */
  legoev3RTOSInit(0.004, 0);

  /* Wait for stop semaphore */
  sem_wait(&stopSem);

#if (MW_NUMBER_TIMER_DRIVEN_TASKS > 0)

  {
    int i;
    for (i=0; i < MW_NUMBER_TIMER_DRIVEN_TASKS; i++) {
      CHECK_STATUS(sem_destroy(&timerTaskSem[i]), 0, "sem_destroy");
    }
  }

#endif

  return 0;
}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */

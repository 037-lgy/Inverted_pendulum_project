  function targMap = targDataMap(),

  ;%***********************
  ;% Create Parameter Map *
  ;%***********************
      
    nTotData      = 0; %add to this count as we go
    nTotSects     = 7;
    sectIdxOffset = 0;
    
    ;%
    ;% Define dummy sections & preallocate arrays
    ;%
    dumSection.nData = -1;  
    dumSection.data  = [];
    
    dumData.logicalSrcIdx = -1;
    dumData.dtTransOffset = -1;
    
    ;%
    ;% Init/prealloc paramMap
    ;%
    paramMap.nSections           = nTotSects;
    paramMap.sectIdxOffset       = sectIdxOffset;
      paramMap.sections(nTotSects) = dumSection; %prealloc
    paramMap.nTotData            = -1;
    
    ;%
    ;% Auto data (Real_Time_Simulation_Correcti_P)
    ;%
      section.nData     = 2;
      section.data(2)  = dumData; %prealloc
      
	  ;% Real_Time_Simulation_Correcti_P.pwm_gain
	  section.data(1).logicalSrcIdx = 0;
	  section.data(1).dtTransOffset = 0;
	
	  ;% Real_Time_Simulation_Correcti_P.pwm_offset
	  section.data(2).logicalSrcIdx = 1;
	  section.data(2).dtTransOffset = 1;
	
      nTotData = nTotData + section.nData;
      paramMap.sections(1) = section;
      clear section
      
      section.nData     = 7;
      section.data(7)  = dumData; %prealloc
      
	  ;% Real_Time_Simulation_Correcti_P.BATTERY
	  section.data(1).logicalSrcIdx = 2;
	  section.data(1).dtTransOffset = 0;
	
	  ;% Real_Time_Simulation_Correcti_P.a_d
	  section.data(2).logicalSrcIdx = 3;
	  section.data(2).dtTransOffset = 1;
	
	  ;% Real_Time_Simulation_Correcti_P.a_gc
	  section.data(3).logicalSrcIdx = 4;
	  section.data(3).dtTransOffset = 2;
	
	  ;% Real_Time_Simulation_Correcti_P.a_gd
	  section.data(4).logicalSrcIdx = 5;
	  section.data(4).dtTransOffset = 3;
	
	  ;% Real_Time_Simulation_Correcti_P.time_start
	  section.data(5).logicalSrcIdx = 6;
	  section.data(5).dtTransOffset = 4;
	
	  ;% Real_Time_Simulation_Correcti_P.ts1
	  section.data(6).logicalSrcIdx = 7;
	  section.data(6).dtTransOffset = 5;
	
	  ;% Real_Time_Simulation_Correcti_P.CompareToConstant1_const
	  section.data(7).logicalSrcIdx = 8;
	  section.data(7).dtTransOffset = 6;
	
      nTotData = nTotData + section.nData;
      paramMap.sections(2) = section;
      clear section
      
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% Real_Time_Simulation_Correcti_P.Speaker_speakerVolume
	  section.data(1).logicalSrcIdx = 9;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      paramMap.sections(3) = section;
      clear section
      
      section.nData     = 8;
      section.data(8)  = dumData; %prealloc
      
	  ;% Real_Time_Simulation_Correcti_P.Gain1_Gain
	  section.data(1).logicalSrcIdx = 10;
	  section.data(1).dtTransOffset = 0;
	
	  ;% Real_Time_Simulation_Correcti_P.Saturation2_UpperSat
	  section.data(2).logicalSrcIdx = 11;
	  section.data(2).dtTransOffset = 1;
	
	  ;% Real_Time_Simulation_Correcti_P.Saturation2_LowerSat
	  section.data(3).logicalSrcIdx = 12;
	  section.data(3).dtTransOffset = 2;
	
	  ;% Real_Time_Simulation_Correcti_P.Gain3_Gain
	  section.data(4).logicalSrcIdx = 13;
	  section.data(4).dtTransOffset = 3;
	
	  ;% Real_Time_Simulation_Correcti_P.Saturation3_UpperSat
	  section.data(5).logicalSrcIdx = 14;
	  section.data(5).dtTransOffset = 4;
	
	  ;% Real_Time_Simulation_Correcti_P.Saturation3_LowerSat
	  section.data(6).logicalSrcIdx = 15;
	  section.data(6).dtTransOffset = 5;
	
	  ;% Real_Time_Simulation_Correcti_P.Constant_Value
	  section.data(7).logicalSrcIdx = 16;
	  section.data(7).dtTransOffset = 6;
	
	  ;% Real_Time_Simulation_Correcti_P.Gain1_Gain_cpx4lbewpy
	  section.data(8).logicalSrcIdx = 17;
	  section.data(8).dtTransOffset = 7;
	
      nTotData = nTotData + section.nData;
      paramMap.sections(4) = section;
      clear section
      
      section.nData     = 27;
      section.data(27)  = dumData; %prealloc
      
	  ;% Real_Time_Simulation_Correcti_P.UnitDelay_InitialCondition
	  section.data(1).logicalSrcIdx = 18;
	  section.data(1).dtTransOffset = 0;
	
	  ;% Real_Time_Simulation_Correcti_P.Gain1_Gain_j0r0df4nzm
	  section.data(2).logicalSrcIdx = 19;
	  section.data(2).dtTransOffset = 1;
	
	  ;% Real_Time_Simulation_Correcti_P.FixPtUnitDelay1_InitialConditio
	  section.data(3).logicalSrcIdx = 20;
	  section.data(3).dtTransOffset = 2;
	
	  ;% Real_Time_Simulation_Correcti_P.deg2rad_Gain
	  section.data(4).logicalSrcIdx = 21;
	  section.data(4).dtTransOffset = 3;
	
	  ;% Real_Time_Simulation_Correcti_P.deg2rad1_Gain
	  section.data(5).logicalSrcIdx = 22;
	  section.data(5).dtTransOffset = 4;
	
	  ;% Real_Time_Simulation_Correcti_P.Gain_Gain
	  section.data(6).logicalSrcIdx = 23;
	  section.data(6).dtTransOffset = 5;
	
	  ;% Real_Time_Simulation_Correcti_P.Gain3_Gain_hka0xvmyzz
	  section.data(7).logicalSrcIdx = 24;
	  section.data(7).dtTransOffset = 6;
	
	  ;% Real_Time_Simulation_Correcti_P.UnitDelay_InitialCon_bijcdbwmgf
	  section.data(8).logicalSrcIdx = 25;
	  section.data(8).dtTransOffset = 7;
	
	  ;% Real_Time_Simulation_Correcti_P.UnitDelay_InitialCon_azw54opzqy
	  section.data(9).logicalSrcIdx = 26;
	  section.data(9).dtTransOffset = 8;
	
	  ;% Real_Time_Simulation_Correcti_P.Gain_Gain_bwkvwsewsv
	  section.data(10).logicalSrcIdx = 27;
	  section.data(10).dtTransOffset = 9;
	
	  ;% Real_Time_Simulation_Correcti_P.deg2rad2_Gain
	  section.data(11).logicalSrcIdx = 28;
	  section.data(11).dtTransOffset = 10;
	
	  ;% Real_Time_Simulation_Correcti_P.Gain3_Gain_gjv3wryppp
	  section.data(12).logicalSrcIdx = 29;
	  section.data(12).dtTransOffset = 11;
	
	  ;% Real_Time_Simulation_Correcti_P.Constant_Value_kzvkk53bcx
	  section.data(13).logicalSrcIdx = 30;
	  section.data(13).dtTransOffset = 12;
	
	  ;% Real_Time_Simulation_Correcti_P.Gain2_Gain
	  section.data(14).logicalSrcIdx = 31;
	  section.data(14).dtTransOffset = 13;
	
	  ;% Real_Time_Simulation_Correcti_P.UnitDelay_InitialCon_egsil4m2ui
	  section.data(15).logicalSrcIdx = 32;
	  section.data(15).dtTransOffset = 14;
	
	  ;% Real_Time_Simulation_Correcti_P.Constant5_Value
	  section.data(16).logicalSrcIdx = 33;
	  section.data(16).dtTransOffset = 15;
	
	  ;% Real_Time_Simulation_Correcti_P.Constant8_Value
	  section.data(17).logicalSrcIdx = 34;
	  section.data(17).dtTransOffset = 16;
	
	  ;% Real_Time_Simulation_Correcti_P.Constant6_Value
	  section.data(18).logicalSrcIdx = 35;
	  section.data(18).dtTransOffset = 17;
	
	  ;% Real_Time_Simulation_Correcti_P.UnitDelay_InitialCon_g5o4mik1am
	  section.data(19).logicalSrcIdx = 36;
	  section.data(19).dtTransOffset = 18;
	
	  ;% Real_Time_Simulation_Correcti_P.Gain2_Gain_ezbw1uq0ur
	  section.data(20).logicalSrcIdx = 37;
	  section.data(20).dtTransOffset = 22;
	
	  ;% Real_Time_Simulation_Correcti_P.Constant6_Value_hyqvqn5fwb
	  section.data(21).logicalSrcIdx = 38;
	  section.data(21).dtTransOffset = 26;
	
	  ;% Real_Time_Simulation_Correcti_P.UnitDelay3_InitialCondition
	  section.data(22).logicalSrcIdx = 39;
	  section.data(22).dtTransOffset = 27;
	
	  ;% Real_Time_Simulation_Correcti_P.Constant7_Value
	  section.data(23).logicalSrcIdx = 40;
	  section.data(23).dtTransOffset = 28;
	
	  ;% Real_Time_Simulation_Correcti_P.Constant5_Value_jhrxeiwmg5
	  section.data(24).logicalSrcIdx = 41;
	  section.data(24).dtTransOffset = 29;
	
	  ;% Real_Time_Simulation_Correcti_P.DiscreteFilter_NumCoef
	  section.data(25).logicalSrcIdx = 42;
	  section.data(25).dtTransOffset = 30;
	
	  ;% Real_Time_Simulation_Correcti_P.DiscreteFilter_DenCoef
	  section.data(26).logicalSrcIdx = 43;
	  section.data(26).dtTransOffset = 31;
	
	  ;% Real_Time_Simulation_Correcti_P.DiscreteFilter_InitialStates
	  section.data(27).logicalSrcIdx = 44;
	  section.data(27).dtTransOffset = 33;
	
      nTotData = nTotData + section.nData;
      paramMap.sections(5) = section;
      clear section
      
      section.nData     = 3;
      section.data(3)  = dumData; %prealloc
      
	  ;% Real_Time_Simulation_Correcti_P.Constant_Value_aljrxhz2pj
	  section.data(1).logicalSrcIdx = 45;
	  section.data(1).dtTransOffset = 0;
	
	  ;% Real_Time_Simulation_Correcti_P.Speaker_p2
	  section.data(2).logicalSrcIdx = 46;
	  section.data(2).dtTransOffset = 1;
	
	  ;% Real_Time_Simulation_Correcti_P.Speaker_p4
	  section.data(3).logicalSrcIdx = 47;
	  section.data(3).dtTransOffset = 2;
	
      nTotData = nTotData + section.nData;
      paramMap.sections(6) = section;
      clear section
      
      section.nData     = 4;
      section.data(4)  = dumData; %prealloc
      
	  ;% Real_Time_Simulation_Correcti_P.FixPtUnitDelay2_InitialConditio
	  section.data(1).logicalSrcIdx = 48;
	  section.data(1).dtTransOffset = 0;
	
	  ;% Real_Time_Simulation_Correcti_P.FixPtConstant_Value
	  section.data(2).logicalSrcIdx = 49;
	  section.data(2).dtTransOffset = 1;
	
	  ;% Real_Time_Simulation_Correcti_P.Speaker_p1
	  section.data(3).logicalSrcIdx = 50;
	  section.data(3).dtTransOffset = 2;
	
	  ;% Real_Time_Simulation_Correcti_P.ManualSwitch_CurrentSetting
	  section.data(4).logicalSrcIdx = 51;
	  section.data(4).dtTransOffset = 3;
	
      nTotData = nTotData + section.nData;
      paramMap.sections(7) = section;
      clear section
      
    
      ;%
      ;% Non-auto Data (parameter)
      ;%
    

    ;%
    ;% Add final counts to struct.
    ;%
    paramMap.nTotData = nTotData;
    


  ;%**************************
  ;% Create Block Output Map *
  ;%**************************
      
    nTotData      = 0; %add to this count as we go
    nTotSects     = 2;
    sectIdxOffset = 0;
    
    ;%
    ;% Define dummy sections & preallocate arrays
    ;%
    dumSection.nData = -1;  
    dumSection.data  = [];
    
    dumData.logicalSrcIdx = -1;
    dumData.dtTransOffset = -1;
    
    ;%
    ;% Init/prealloc sigMap
    ;%
    sigMap.nSections           = nTotSects;
    sigMap.sectIdxOffset       = sectIdxOffset;
      sigMap.sections(nTotSects) = dumSection; %prealloc
    sigMap.nTotData            = -1;
    
    ;%
    ;% Auto data (Real_Time_Simulation_Correcti_B)
    ;%
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% Real_Time_Simulation_Correcti_B.Sum
	  section.data(1).logicalSrcIdx = 0;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      sigMap.sections(1) = section;
      clear section
      
      section.nData     = 6;
      section.data(6)  = dumData; %prealloc
      
	  ;% Real_Time_Simulation_Correcti_B.counter_value
	  section.data(1).logicalSrcIdx = 2;
	  section.data(1).dtTransOffset = 0;
	
	  ;% Real_Time_Simulation_Correcti_B.Sum1
	  section.data(2).logicalSrcIdx = 3;
	  section.data(2).dtTransOffset = 1;
	
	  ;% Real_Time_Simulation_Correcti_B.UnitDelay
	  section.data(3).logicalSrcIdx = 4;
	  section.data(3).dtTransOffset = 2;
	
	  ;% Real_Time_Simulation_Correcti_B.Gain
	  section.data(4).logicalSrcIdx = 5;
	  section.data(4).dtTransOffset = 3;
	
	  ;% Real_Time_Simulation_Correcti_B.Gain_oopwalytwu
	  section.data(5).logicalSrcIdx = 6;
	  section.data(5).dtTransOffset = 4;
	
	  ;% Real_Time_Simulation_Correcti_B.psidot
	  section.data(6).logicalSrcIdx = 7;
	  section.data(6).dtTransOffset = 5;
	
      nTotData = nTotData + section.nData;
      sigMap.sections(2) = section;
      clear section
      
    
      ;%
      ;% Non-auto Data (signal)
      ;%
    

    ;%
    ;% Add final counts to struct.
    ;%
    sigMap.nTotData = nTotData;
    


  ;%*******************
  ;% Create DWork Map *
  ;%*******************
      
    nTotData      = 0; %add to this count as we go
    nTotSects     = 6;
    sectIdxOffset = 2;
    
    ;%
    ;% Define dummy sections & preallocate arrays
    ;%
    dumSection.nData = -1;  
    dumSection.data  = [];
    
    dumData.logicalSrcIdx = -1;
    dumData.dtTransOffset = -1;
    
    ;%
    ;% Init/prealloc dworkMap
    ;%
    dworkMap.nSections           = nTotSects;
    dworkMap.sectIdxOffset       = sectIdxOffset;
      dworkMap.sections(nTotSects) = dumSection; %prealloc
    dworkMap.nTotData            = -1;
    
    ;%
    ;% Auto data (Real_Time_Simulation_Corr_DWork)
    ;%
      section.nData     = 3;
      section.data(3)  = dumData; %prealloc
      
	  ;% Real_Time_Simulation_Corr_DWork.FromWs_PWORK.TimePtr
	  section.data(1).logicalSrcIdx = 0;
	  section.data(1).dtTransOffset = 0;
	
	  ;% Real_Time_Simulation_Corr_DWork.Scope_PWORK.LoggedData
	  section.data(2).logicalSrcIdx = 1;
	  section.data(2).dtTransOffset = 1;
	
	  ;% Real_Time_Simulation_Corr_DWork.Scope_PWORK_pmo3q4xz34.LoggedData
	  section.data(3).logicalSrcIdx = 2;
	  section.data(3).dtTransOffset = 3;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(1) = section;
      clear section
      
      section.nData     = 9;
      section.data(9)  = dumData; %prealloc
      
	  ;% Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE
	  section.data(1).logicalSrcIdx = 3;
	  section.data(1).dtTransOffset = 0;
	
	  ;% Real_Time_Simulation_Corr_DWork.UnitDelay3_DSTATE
	  section.data(2).logicalSrcIdx = 4;
	  section.data(2).dtTransOffset = 4;
	
	  ;% Real_Time_Simulation_Corr_DWork.DiscreteFilter_states
	  section.data(3).logicalSrcIdx = 5;
	  section.data(3).dtTransOffset = 5;
	
	  ;% Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_cfkvxtl130
	  section.data(4).logicalSrcIdx = 6;
	  section.data(4).dtTransOffset = 6;
	
	  ;% Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_hzuovbre5y
	  section.data(5).logicalSrcIdx = 7;
	  section.data(5).dtTransOffset = 7;
	
	  ;% Real_Time_Simulation_Corr_DWork.FixPtUnitDelay1_DSTATE
	  section.data(6).logicalSrcIdx = 8;
	  section.data(6).dtTransOffset = 8;
	
	  ;% Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_orvhqhlbcp
	  section.data(7).logicalSrcIdx = 9;
	  section.data(7).dtTransOffset = 9;
	
	  ;% Real_Time_Simulation_Corr_DWork.UnitDelay_DSTATE_mjna1kxy33
	  section.data(8).logicalSrcIdx = 10;
	  section.data(8).dtTransOffset = 10;
	
	  ;% Real_Time_Simulation_Corr_DWork.DiscreteFilter_tmp
	  section.data(9).logicalSrcIdx = 11;
	  section.data(9).dtTransOffset = 11;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(2) = section;
      clear section
      
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% Real_Time_Simulation_Corr_DWork.FromWs_IWORK.PrevIndex
	  section.data(1).logicalSrcIdx = 12;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(3) = section;
      clear section
      
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% Real_Time_Simulation_Corr_DWork.FixPtUnitDelay2_DSTATE
	  section.data(1).logicalSrcIdx = 13;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(4) = section;
      clear section
      
      section.nData     = 2;
      section.data(2)  = dumData; %prealloc
      
	  ;% Real_Time_Simulation_Corr_DWork.GyroCalibration_SubsysRanBC
	  section.data(1).logicalSrcIdx = 14;
	  section.data(1).dtTransOffset = 0;
	
	  ;% Real_Time_Simulation_Corr_DWork.BalanceandDriveControl_SubsysRa
	  section.data(2).logicalSrcIdx = 15;
	  section.data(2).dtTransOffset = 1;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(5) = section;
      clear section
      
      section.nData     = 1;
      section.data(1)  = dumData; %prealloc
      
	  ;% Real_Time_Simulation_Corr_DWork.BalanceandDriveControl_MODE
	  section.data(1).logicalSrcIdx = 17;
	  section.data(1).dtTransOffset = 0;
	
      nTotData = nTotData + section.nData;
      dworkMap.sections(6) = section;
      clear section
      
    
      ;%
      ;% Non-auto Data (dwork)
      ;%
    

    ;%
    ;% Add final counts to struct.
    ;%
    dworkMap.nTotData = nTotData;
    


  ;%
  ;% Add individual maps to base struct.
  ;%

  targMap.paramMap  = paramMap;    
  targMap.signalMap = sigMap;
  targMap.dworkMap  = dworkMap;
  
  ;%
  ;% Add checksums to base struct.
  ;%


  targMap.checksum0 = 2855760259;
  targMap.checksum1 = 2959079637;
  targMap.checksum2 = 1713522580;
  targMap.checksum3 = 2605490048;


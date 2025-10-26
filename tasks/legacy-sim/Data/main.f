C     Legacy Physics Simulation - Main Program
C     Written in 1995 for g77 compiler
C     Port to gfortran to make it work!
      
      PROGRAM PHYSSIM
      IMPLICIT NONE
      
C     Common blocks
      COMMON /SIMDATA/ NPTS, TIMESTEP, MAXITER
      COMMON /RESULTS/ ENERGY, MOMENTUM, TEMP
      INTEGER NPTS, MAXITER
      REAL*8 TIMESTEP, ENERGY, MOMENTUM, TEMP
      
C     Local variables
      INTEGER ITER
      REAL*8 START_TIME, END_TIME
      CHARACTER*80 INFILE, OUTFILE
      
C     Set file paths
      INFILE = 'input.txt'
      OUTFILE = 'results.dat'
      
      PRINT *, 'Legacy Fortran Simulation v1.0'
      PRINT *, 'Reading input from: ', INFILE
      
C     Read simulation parameters
      CALL READINPUT(INFILE)
      
      PRINT *, 'Grid points:', NPTS
      PRINT *, 'Time step:', TIMESTEP
      PRINT *, 'Max iterations:', MAXITER
      
C     Initialize simulation
      CALL INITDATA()
      
C     Record start time
      CALL CPU_TIME(START_TIME)
      
C     Run main simulation loop
      DO ITER = 1, MAXITER
         CALL COMPUTE_STEP(ITER)
         IF (MOD(ITER, 100) .EQ. 0) THEN
            PRINT *, 'Progress: ', ITER, '/', MAXITER
         ENDIF
      ENDDO
      
C     Record end time
      CALL CPU_TIME(END_TIME)
      
      PRINT *, 'Simulation completed successfully!'
      PRINT *, 'Time elapsed:', END_TIME - START_TIME, 'seconds'
      PRINT *, 'Final energy:', ENERGY
      
C     Write results to file
      CALL WRITEOUTPUT(OUTFILE)
      
      PRINT *, 'Results saved to:', OUTFILE
      
      END PROGRAM PHYSSIM

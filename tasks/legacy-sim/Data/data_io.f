C     Data I/O Routines
C     Handles reading parameters and writing results
      
      SUBROUTINE READINPUT(FILENAME)
      IMPLICIT NONE
      CHARACTER*(*) FILENAME
      
      COMMON /SIMDATA/ NPTS, TIMESTEP, MAXITER
      INTEGER NPTS, MAXITER
      REAL*8 TIMESTEP
      
      INTEGER IOSTAT
      
C     Open input file
      OPEN(UNIT=10, FILE=FILENAME, STATUS='OLD', IOSTAT=IOSTAT)
      
      IF (IOSTAT .NE. 0) THEN
         PRINT *, 'ERROR: Cannot open input file: ', FILENAME
         STOP
      ENDIF
      
C     Read simulation parameters
      READ(10, *) NPTS
      READ(10, *) TIMESTEP
      READ(10, *) MAXITER
      
      CLOSE(10)
      
      RETURN
      END SUBROUTINE READINPUT
      
      
      SUBROUTINE WRITEOUTPUT(FILENAME)
      IMPLICIT NONE
      CHARACTER*(*) FILENAME
      
      COMMON /SIMDATA/ NPTS, TIMESTEP, MAXITER
      COMMON /RESULTS/ ENERGY, MOMENTUM, TEMP
      INTEGER NPTS, MAXITER
      REAL*8 TIMESTEP, ENERGY, MOMENTUM, TEMP
      
      INTEGER I, IOSTAT
      REAL*8 X, VALUE
      
C     Open output file
      OPEN(UNIT=20, FILE=FILENAME, STATUS='UNKNOWN', IOSTAT=IOSTAT)
      
      IF (IOSTAT .NE. 0) THEN
         PRINT *, 'ERROR: Cannot create output file'
         STOP
      ENDIF
      
C     Write simulation summary
      WRITE(20, '(A)') '# 1D Wave Simulation Results'
      WRITE(20, '(A,I6)') '# Grid Points: ', NPTS
      WRITE(20, '(A,F12.6)') '# Time Step: ', TIMESTEP
      WRITE(20, '(A,I6)') '# Iterations: ', MAXITER
      WRITE(20, '(A)')
      WRITE(20, '(A,E16.8)') '# Final Energy: ', ENERGY
      WRITE(20, '(A,E16.8)') '# Final Momentum: ', MOMENTUM  
      WRITE(20, '(A,F12.4)') '# Final Temperature: ', TEMP
      WRITE(20, '(A)')
      
C     Write grid data
      DO I = 1, NPTS
         X = DBLE(I-1) / DBLE(NPTS-1)
         CALL GETPOINT(I, VALUE)
         WRITE(20, '(F10.6,2X,E16.8)') X, VALUE
      ENDDO
      
      CLOSE(20)
      
      RETURN
      END SUBROUTINE WRITEOUTPUT

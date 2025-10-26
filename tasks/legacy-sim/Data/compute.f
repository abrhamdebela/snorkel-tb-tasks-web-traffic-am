C     Core Computation Routines
C     Simple 1D wave simulation
      
      SUBROUTINE INITDATA()
      IMPLICIT NONE
      
      COMMON /SIMDATA/ NPTS, TIMESTEP, MAXITER
      COMMON /RESULTS/ ENERGY, MOMENTUM, TEMP
      COMMON /GRIDDATA/ GRID, VELOCITY
      INTEGER NPTS, MAXITER
      REAL*8 TIMESTEP, ENERGY, MOMENTUM, TEMP
      REAL*8 GRID(10000), VELOCITY(10000)
      
      INTEGER I
      REAL*8 PI, X
      
      PI = 4.0D0 * DATAN(1.0D0)
      
C     Initialize grid with a Gaussian pulse
      DO I = 1, NPTS
         X = DBLE(I-1) / DBLE(NPTS-1)
         GRID(I) = DEXP(-50.0D0 * (X - 0.5D0)**2)
         VELOCITY(I) = 0.0D0
      ENDDO
      
C     Set boundary conditions (fixed endpoints)
      GRID(1) = 0.0D0
      GRID(NPTS) = 0.0D0
      
C     Initialize global values
      ENERGY = 0.0D0
      MOMENTUM = 0.0D0
      TEMP = 300.0D0
      
      RETURN
      END SUBROUTINE INITDATA
      
      
      SUBROUTINE COMPUTE_STEP(ITER)
      IMPLICIT NONE
      INTEGER ITER
      
      COMMON /SIMDATA/ NPTS, TIMESTEP, MAXITER
      COMMON /RESULTS/ ENERGY, MOMENTUM, TEMP
      COMMON /GRIDDATA/ GRID, VELOCITY
      INTEGER NPTS, MAXITER
      REAL*8 TIMESTEP, ENERGY, MOMENTUM, TEMP
      REAL*8 GRID(10000), VELOCITY(10000)
      
      INTEGER I
      REAL*8 ACCEL, DAMPING
      
      DAMPING = 0.999D0
      
C     Simple 1D wave equation with damping
C     d^2u/dt^2 = d^2u/dx^2 - damping * du/dt
      
      DO I = 2, NPTS-1
C        Compute acceleration from neighbors (second derivative)
         ACCEL = GRID(I+1) - 2.0D0*GRID(I) + GRID(I-1)
         
C        Update velocity with damping
         VELOCITY(I) = VELOCITY(I) + ACCEL * TIMESTEP
         VELOCITY(I) = VELOCITY(I) * DAMPING
         
C        Update position
         GRID(I) = GRID(I) + VELOCITY(I) * TIMESTEP
      ENDDO
      
C     Enforce boundary conditions
      GRID(1) = 0.0D0
      GRID(NPTS) = 0.0D0
      VELOCITY(1) = 0.0D0
      VELOCITY(NPTS) = 0.0D0
      
C     Compute total energy and momentum
      ENERGY = 0.0D0
      MOMENTUM = 0.0D0
      DO I = 1, NPTS
         ENERGY = ENERGY + GRID(I)**2 + VELOCITY(I)**2
         MOMENTUM = MOMENTUM + VELOCITY(I)
      ENDDO
      ENERGY = 0.5D0 * ENERGY
      
C     Temperature scales with energy
      TEMP = 300.0D0 + ENERGY * 10.0D0
      
      RETURN
      END SUBROUTINE COMPUTE_STEP
      
      
      SUBROUTINE GETPOINT(INDEX, VALUE)
      IMPLICIT NONE
      INTEGER INDEX
      REAL*8 VALUE
      
      COMMON /GRIDDATA/ GRID, VELOCITY
      REAL*8 GRID(10000), VELOCITY(10000)
      
      IF (INDEX .GE. 1 .AND. INDEX .LE. 10000) THEN
         VALUE = GRID(INDEX)
      ELSE
         VALUE = 0.0D0
      ENDIF
      
      RETURN
      END SUBROUTINE GETPOINT

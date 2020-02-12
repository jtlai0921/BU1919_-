      SUBROUTINE DLOAD(F,KSTEP,KINC,TIME,NOEL,NPT,LAYER,KSPT,
     1 COORDS,JLTYP,SNAME)
C  
      INCLUDE 'ABA_PARAM.INC'
C
      DIMENSION TIME(2),COORDS (3)
      CHARACTER*80 SNAME
      integer i,j,k,m,n
      real rad1,Dia0,alpha,omega,Tforce,temp1,temp2,temp3,temp4,temp5
      real pi, num, CLen, E1,E2,v1,v2,Kb,cPo,Wb,pmax
      parameter (pi = 3.1415926, num = 8)
      real beta(num),theta(num),the2(num),force(num)
C
      Tforce=100000.0
      rad1=80.0
      Dia0=20.0
      omega=2.0*pi
      t=TIME(1)
      temp1=0.0
      CLen=1.0
      E1=210000.0
      E2=210000.0
      v1=0.3
      v2=0.3
      alpha=omega*t
      do i=1,num
        beta(i)=alpha*(rad1-Dia0)/rad1+(i-1.0)*2.0*pi/num
        beta(i)=MOD(beta(i),2.0*pi)
        theta(i)=beta(i)-alpha
        if (cos(theta(i)).GT.0.0) then
            the2(i) = (cos(theta(i)))**2
            temp1 = temp1+the2(i)
        else
            the2(i) = 0.0
        end if
      end do
      do j=1,num
        if (the2(j).NE.0.0) then
            force(j)=cos(theta(j))*Tforce/temp1
        else
            force(j)=0.0
        end if
      end do
      WRITE(7,*) 'force=', Tforce
      WRITE(7,*) 'Roller Diameter=', Dia0, 'mm'
      temp2=2.0*((1.0-v1**2)/E1+(1.0-v2**2)/E2)
      temp3=pi*CLen*(1.0/Dia0-0.5/rad1)
      Kb=(temp2/temp3)**0.5
      if ((COORDS(2).EQ.0.0) .and. (COORDS(1).GT.0.0)) then
          cPo=0.0
      else if ((COORDS(2).EQ.0.0) .and. (COORDS(1).LT.0.0)) then
          cPo=pi
      else if ((COORDS(1).EQ.0.0) .and. (COORDS(2).GT.0.0)) then
          cPo=0.5*pi
      else if ((COORDS(1).EQ.0.0) .and. (COORDS(2).LT.0.0)) then
          cPo=1.5*pi
      else if (COORDS(1).GT.0.0) then
          cPo=atan(COORDS(2)/COORDS(1))+2.0*pi
      else if (COORDS(1).LT.0.0) then
          cPo=atan(COORDS(2)/COORDS(1))+pi
      end if
      cPo=MOD(cPo, 2.0*pi)
      temp4 = 10000.0
      do m=1,num
        if (temp4>abs(cPo-beta(m))) then
            n=m
            temp4=abs(cPo-beta(m))
        end if        
      end do
      if (force(n).GT.0.0) then
        Wb=Kb*sqrt(force(n))
        pmax=2.0*force(n)/pi/CLen/Wb
        temp4=abs(cPo-beta(n))
        temp5=Wb/rad1
        if (temp4.GT.temp5) then
            F=0.0
        else
            F=pmax*sqrt(1.0-(temp4/temp5)**2)
        end if
      else
        F=0.0
      end if
      RETURN
      END
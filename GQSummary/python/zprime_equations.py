from ROOT import *
import ROOT,sys,os,math
from math import sqrt

mq = {"u":2.3e-3, "d":4.8e-3, "c":1.275, "s":0.095, "b":4.18, "t":173.21}


# Partial width Gamma(Z' -> qq)
# @param gq
# @param mZp = mediator mass
# @param qtype = quark flavor, u, d, c, s, b, or t
# @param vtype = "axial" or "vector"

def Gamma_qq(gq, mZp, vtype, qtype):
    if mZp < 2. * mq[qtype]:
        return 0.
    elif vtype == "axial":
        return 3. * gq**2 * mZp * (1. - (4. * mq[qtype]**2) / mZp**2)**1.5 / (12. * math.pi)
    elif vtype == "vector":
        return 3. * gq**2 * mZp * (1. - (4. * mq[qtype]**2) / mZp**2)**0.5 * (1. + 2. * mq[qtype]**2 / mZp**2) / (12. * math.pi)
    else:
        print "[Gamma_qq] ERROR : Unknown vtype {}".format(vtype)
        sys.exit(1)

# Total width Gamma(Z' -> quarks)
# @param gq
# @param mZp = mediator mass
# @param vtype = "axial" or "vector"
def Gamma_qq_tot(gq, mZp, vtype):
    this_width = 0.
    for qtype in ["u", "d", "s", "c", "b", "t"]:
        this_width += Gamma_qq(gq, mZp, vtype, qtype)
    return this_width

# Partial width Gamma(Z' -> chi chi)
# @param gq
# @param mZp = mediator mass
# @param mDM = dark matter mass
# @param vtype = "axial" or "vector"
def Gamma_DM(gDM, mZp, mDM, vtype):
    if 2 * mDM > mZp:
        return 0.
    elif vtype == "axial":
        return gDM**2 * mZp * (1. - (4. * mDM**2) / mZp**2)**1.5 / (12. * math.pi)
    elif vtype == "vector":
        return gDM**2 * mZp * (1. - (4. * mDM**2) / mZp**2)**0.5 * (1. + 2. * mDM**2 / mZp**2) / (12. * math.pi)
    else:
        print "[Gamma_DM] ERROR : Unknown vtype {}".format(vtype)
        sys.exit(1)

# Convert Z' width (Gamma(Z' -> qq)) to g_q
def width_to_gq(width, mZp, vtype):
    den = 0.
    for qtype in ["u", "d", "s", "c", "b", "t"]:
        if mZp > 2. * mq[qtype]:
            if vtype == "vector":
                den += 1. / (4. * math.pi) * (1. - 4. * mq[qtype]**2 / mZp**2)**0.5 * (1. + 2. * mq[qtype]**2 / mZp**2)
            elif vtype == "axial":
                den += 1. / (4. * math.pi) * (1. - 4. * mq[qtype]**2 / mZp**2)**1.5
            else:
                print "[width_to_gq] ERROR : Unknown vtype {}".format(vtype)
                sys.exit(1)
    return sqrt(width / mZp / den)

# Convert Gamma-over-mass (Gamma(Z'->qq)) to g_q
def gom_to_gq(gom, mZp, vtype):
    return width_to_gq(gom * mZp, mZp, vtype)

# g_q constraint from Z width
def gq_Z_constraint(x):
    
    # Zwidth = 2.4952;
    # ZwidthError = 0.0023*3; # times 3 to give 3 sigma
    # relZwidthUnc = ZwidthError/Zwidth;
    # sin2thetaW = 0.2312;
    # sinthetaW = math.sqrt(sin2thetaW);
    # costhetaW = math.sqrt(1 - sin2thetaW);
    # mW = 80.385;
    # vev = 246.;
    # g = mW*2./vev;
    # Vu = 0.25 - (4. * sin2thetaW / 6.);
    # Vd = -0.25 - (2. * sin2thetaW / 6.);
    # mZ = 91.18;
    # mZp = x[0];

    # # y = gZ
    # ynum = relZwidthUnc * 3 * g * -1. * math.fabs(1-(mZp*mZp/(mZ*mZ))) * (2*Vu*Vu + 3*Vd*Vd + 5/16.)
    # yden = 2*0.01*costhetaW*sinthetaW*(2*Vu+3*Vd);
    # # print ynum,yden,x[0],math.sqrt(ynum/yden)
    # y = math.sqrt(ynum/yden);
    # y *= 1.5;

    mZ = 91.1876
    mZp = x[0]
    ynum = 4. * math.sqrt( 4. * math.pi ) * 1.96 * 1.1e-3 * ( 1-(mZp*mZp/(mZ*mZ)) )
    yden = 1.193 * 0.02
    if ynum < 0: 
        ynum *= -1.
    y = math.sqrt(ynum/yden) / 6.

    return y

def gq_upsilon_constraint(x):
    mUps = 9.46
    WidUps = 54e-6
    alpha = 1/130.
    Argus = 5.3e-2
    DimuUps = 2.48e-2
    RUps = Argus/DimuUps
    mZp = x[0]

    y = abs(( 2*4*math.pi*alpha ) * ( math.sqrt( 3.*RUps + 1 ) + 1 ) * (1-(mZp*mZp/(mUps*mUps))))

    return math.sqrt(y)/6.

def convert_gq(gq, mZp, gDM, mDM, vtype):
    '''
    Convert excluded gq(mZp, mDM, gDM=0) to gq(mZp, mDM, gDM)
    '''
    return gq * math.sqrt(0.5 * (1. + math.sqrt(1. + 4. * Gamma_DM(gDM=gDM, mZp=mZp, mDM=mDM, vtype=vtype) / Gamma_qq_tot(gq=gq, mZp=mZp, vtype=vtype))))


#def A(gq,mZp,mDM,vtype):
#    return gq**2*Gammaqq_tot(gq,mZp,vtype)/(Gammaqq_tot(gq,mZp,vtype)+GammaDM(1,mZp,mDM,vtype))
#
#def B(gq,mZp,mDM,vtype):
#    return gq**4*GammaDM(1,mZp,1,vtype)/(Gammaqq_tot(gq,mZp,vtype)+GammaDM(1,mZp,mDM,vtype))
#
#### transfer the limit from gDM=1 & mDM=1 to arbitrary mDM
#### used by dijet chi analysis
#def g_q(gq,mZp,mDM,vtype):
#    return math.pow((A(gq,mZp,mDM,vtype)+math.pow(A(gq,mZp,mDM,vtype)**2+4*B(gq,mZp,mDM,vtype),0.5))*0.5,0.5)
#
#
#
#### transfer the limit for 2mDM>MMed (gqprime) to gDM=1 & mDM=1
#### not useful anymore
#def gq(gqprime):
#    #return gq*math.pow(0.5+math.pow(0.25+1/(18*(gq**2)),0.5),0.5)
#    return math.pow(3*gqprime**2+math.pow(gqprime**2*(9*gqprime**2+2),0.5),0.5)/math.pow(6,0.5)
#
#
#### width(gq, MMed) function (mDM=1, gDM=1)
#def medWidth(gq,mZp,vtype):
#  return Gammaqq_tot(gq, mZp, vtype)/float(mZp)+1/(12*3.141592653)
#
#
#### width(gqprime, MMed) function (2mDM>MMed)
#def medWidth_gqprime(gq,mZp,vtype):
#    #return 6*gq**2/(4*3.141592653)
#    return Gammaqq_tot(gq, mZp, vtype)/float(mZp)
#
#
#### gqprime(width, MMed) function
#def gqprime(width, mZp,vtype):
#    for gq in np.linspace(0,1.5,1001):
#        if medWidth_gqprime(gq,mZp,vtype)<=width:
#            gqprime=gq
#    return gqprime
#

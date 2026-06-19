from pymavlink import mavutil
import pandas as pd

def get_pwm_stats(binfile):

    log=mavutil.mavlink_connection(binfile)

    pwm=[]
    nf=[]

    while True:

        msg=log.recv_match(blocking=False)

        if msg is None:
            break

        if msg.get_type()=="RCOU":

            avg_pwm=(
                msg.C1+
                msg.C2+
                msg.C3+
                msg.C4+
                msg.C5+
                msg.C6
            )/6

            pwm.append(avg_pwm)

        elif msg.get_type()=="FTN":

            if msg.I==0:
                nf.append(msg.NF1)

    n=min(len(pwm),len(nf))

    pwm=pwm[:n]
    nf=nf[:n]

    corr=pd.Series(pwm).corr(
        pd.Series(nf)
    )

    return {
        "correlation": round(float(corr),3)
    }
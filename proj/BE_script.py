import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
from scipy import signal
import math
from control import matlab

from scipy.integrate import solve_ivp
import my_animation as mp

import NXTwaysim as nxt

# Plot le lieu des racines en boucle ouverte
plot_pmap = False

# Plot la réponse à un échelon unitaire en boucle ouverte
plot_step_bo = False

# Plot la réponse à un échelon (pi/5) du modèle non linéaire
plot_non_linear_bo = False

# Plot la comparaison de la sortie theta entre le modèle
# linéaire et non linéaire, sur un temps court avec un échelon unitaire entrée
plot_compare_lin_nonlin_bo = False

# Plot la réponse à un impulsion
plot_impulse_bo = False

# Plot le lieu des racines en fonction de Kp (à la main et avec rootlocus)
plot_locus_prop_gain = False

# Plot la réponse à un échelon unitaire avec Kp = 1
plot_prop_gain_resp = False

# Plot le lieu des racine après calcul du retour d'état
plot_pmap_bf = False

# Plot la réponse en bf à échelon sans lc
plot_step_bf = False

# Plot la réponse en bf à échelon avec lc
plot_step_bf_gain = False

# Plot la commande en bf avec retour d'état
plot_input_bf = False

# Plot la réponse en bf à échelon unitaire avec lc en utilisant lsim
plot_lsim_pregain = False

# Plot la réponse à un échelon (pi/5) du modèle non linéaire
plot_non_linear = False

# Plot la comparaison de theta/psi/u entre le modèle linéaire et non linéaire
# avec un échelon en entrée pour les valeurs de K et lc calculées au début
plot_compare_lin_nonlin_bf = False

#Pas utilisée
plot_non_linear_euler = False

start_animation = True

# Fonction pour changer l'échelon d'entrée
def consigne_temp(t, start_time, amplitude):
    if t < start_time:
        return 0
    else:
        return amplitude


def main():
    E_11 = (2 * nxt.m + nxt.M) * nxt.R ** 2 + 2 * nxt.Jw + 2 * nxt.n ** 2 * nxt.Jm
    E_12 = nxt.M * nxt.L * nxt.R - 2 * nxt.n ** 2 * nxt.Jm
    E_22 = nxt.M * nxt.L ** 2 + nxt.Jpsi + 2 * nxt.n ** 2 * nxt.Jm
    detE = E_11 * E_22 - E_12 ** 2

    A1_32 = -nxt.g * nxt.M * nxt.L * E_12 / detE
    A1_42 = nxt.g * nxt.M * nxt.L * E_11 / detE
    A1_33 = -2 * (nxt.tmp * E_22 + nxt.beta * E_12) / detE
    A1_43 = 2 * (nxt.tmp * E_12 + nxt.beta * E_11) / detE
    A1_34 = 2 * nxt.beta * (E_22 + E_12) / detE
    A1_44 = -2 * nxt.beta * (E_11 + E_12) / detE
    B1_3 = nxt.alpha * (E_22 + E_12) / detE
    B1_4 = -nxt.alpha * (E_11 + E_12) / detE

    # State-Space Matrix Calculation - MIMO model

    A1 = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [0, A1_32, A1_33, A1_34], [0, A1_42, A1_43, A1_44]])
    B1 = np.array([[0, 0], [0, 0], [B1_3, B1_3], [B1_4, B1_4]])
    C1 = np.identity(4)
    D1 = np.zeros((4, 2))

    I = nxt.m * nxt.W ** 2 / 2 + nxt.Jphi + (nxt.Jw + nxt.n ** 2 * nxt.Jm) * nxt.W ** 2 / (2 * nxt.R ** 2)
    J = nxt.tmp * nxt.W ** 2 / (2 * nxt.R ** 2)
    K = nxt.alpha * nxt.W / (2 * nxt.R)

    A2 = np.array([[0, 1], [0, -J / I]])
    B2 = np.array([[0, 0], [-K / I, K / I]])
    C2 = np.identity(2)
    D2 = np.zeros((2, 2))

    # State-Space Matrix Calculation - SISO model

    A = A1
    B = 2*B1[:, 0].reshape(4, 1)
    C = np.array([1, 0, 0, 0])
    D = 0
    sysbo = ctrl.ss(A, B, C, D)

    #Observability and controlability 

    Qo = ctrl.obsv(A, C)
    # print(np.linalg.matrix_rank(Qo))

    Qc = ctrl.ctrb(A, B)
    # print(np.linalg.matrix_rank(Qc))

    if plot_pmap:
        fig1, ax1 = plt.subplots()
        poles = ctrl.poles(sysbo)
        poles_real = np.real(poles)
        poles_im = np.imag(poles)
        ax1.scatter(poles_real, poles_im, marker='x', label='poles')
        zeros = ctrl.zeros(sysbo)
        zeros_real = np.real(zeros)
        zeros_im = np.imag(zeros)
        ax1.scatter(zeros_real, zeros_im, marker='o', label='zeros')
        ax1.set_xlabel('Real part')
        ax1.set_ylabel('Imaginary part')
        ax1.set_title('pzmap')
        ax1.legend()
        ax1.grid(True)

    # print(ctrl.damp(sysbo))

    if plot_step_bo:
        dt = 0.01
        tf = 1
        t = np.arange(0, tf, dt)
        x0 = np.array([[0], [0], [0], [0]])
        tout, theta = ctrl.step_response(sysbo, t, x0)

        fig2, ax2 = plt.subplots()
        ax2.plot(tout, theta)

        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Angle (rad)')
        ax2.set_title('Step response')
        ax2.grid(True)


    tspan = (0.0, 5.0)
    t_eval = np.linspace(tspan[0], tspan[1], num=200)
    x0 = [0.0, 0.0, 0.0, 0.0]
    reference_amplitude = np.pi/5
    start_reference_time = 0
    sol_bo = solve_ivp(nxt.xdot, tspan, x0, t_eval=t_eval, method='RK45', args=(0, 1, consigne_temp, start_reference_time, reference_amplitude))

    t = sol_bo.t
    xout = sol_bo.y
    theta_nlin_bo = sol_bo.y[0, :]
    psi_nlin_bo = sol_bo.y[1, :]

    if plot_non_linear_bo:
        fig13, ax13 = plt.subplots()
        ax13.plot(t, theta_nlin_bo, label='theta')
        ax13.plot(t, psi_nlin_bo, label='psi')

        ax13.set_xlabel('Time (s)')
        ax13.set_ylabel('Angle (rad)')
        ax13.set_title('Non linear step response')
        ax13.legend()
        ax13.grid(True)

    if plot_compare_lin_nonlin_bo:
        tspan = (0.0, 0.7)
        t_eval = np.linspace(tspan[0], tspan[1], num=200)
        x0 = [0.0, 0.0, 0.0, 0.0]
        reference_amplitude = 1
        start_reference_time = 0
        sol_bo = solve_ivp(nxt.xdot, tspan, x0, t_eval=t_eval, method='RK45', args=(0, 1, consigne_temp, start_reference_time, reference_amplitude))

        t = sol_bo.t
        xout = sol_bo.y
        theta_nlin_bo = sol_bo.y[0, :]
        psi_nlin_bo = sol_bo.y[1, :]
        x0 = np.array([[0], [0], [0], [0]])
        tout, theta = ctrl.step_response(sysbo, t, x0)

        fig14, ax14 = plt.subplots()
        ax14.plot(t, theta, label='linear theta')
        ax14.plot(t, theta_nlin_bo, label='non linear theta')

        ax14.set_xlabel('Time (s)')
        ax14.set_ylabel('Angle (rad)')
        ax14.set_title('BO step response linearization comparison')
        ax14.legend()
        ax14.grid(True)

    # Plot impulse response

    if plot_impulse_bo:
        dt = 0.01
        tf = 1
        t = np.arange(0, tf, dt)
        x0 = np.array([[0], [0], [0], [0]])
        tout, theta = ctrl.impulse_response(sysbo, timepts=t)

        fig3, ax3 = plt.subplots()
        ax3.plot(tout, theta)

        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Angle (rad)')
        ax3.set_title('Impulse response')
        ax3.grid(True)

    # Balance control

    # Erase unnecessary coefficients
    G = ctrl.ss2tf(A, B, C, D)
    num = G.num_array[0, 0]
    den = G.den_array[0, 0]
    for i in range(4):
        if 0.0005 > num[i] > -0.0005:
            num[i] = 0
        if 0.0005 > den[i] > -0.0005:
            den[i] = 0

    G = ctrl.TransferFunction(num, den)

    # Considering a closed loop system with proportional gain Kp : u = -Kp*epsilon

    if plot_locus_prop_gain:
        Kp = np.logspace(-1, 3, 200)
        fig4, ax4 = plt.subplots()
        ctrl.root_locus(G)
        ax4.set_xlabel('Real part')
        ax4.set_ylabel('Imaginary part')
        ax4.set_title('root locus plot for siso system')
        ax4.grid(True)
        fig5, ax5 = plt.subplots()
        for i in Kp:
            F = ctrl.feedback(i * G, 1)
            p = ctrl.poles(F)
            Z = ctrl.zeros(F)
            ax5.scatter(np.real(p), np.imag(p), marker='x')
            ax5.scatter(np.real(Z), np.imag(Z), marker='o')
        ax5.set_xlabel('Real part')
        ax5.set_ylabel('Imaginary part')
        ax5.set_title('pzmap depending on proportional gain')
        ax5.grid(True)

    if plot_prop_gain_resp:
        dt = 0.01
        tf = 1
        t = np.arange(0, tf, dt)
        x0 = np.array([[0], [0], [0], [0]])
        F = ctrl.feedback(1 * G, 1)
        tout, theta = ctrl.step_response(F, t)

        fig6, ax6 = plt.subplots()
        ax6.plot(tout, theta)

        ax6.set_xlabel('Time (s)')
        ax6.set_ylabel('Theta angle (rad)')
        ax6.set_title('Step response to unitary proportional gain')
        ax6.grid(True)

    # State feedback : u = -K*x

    a4 = den[0]
    a3 = den[1]
    a2 = den[2]
    a1 = den[3]
    a0 = den[4]

    # MCH horizontal companion form
    m4 = B
    m3 = np.dot((A + a3 * np.identity(4)), B)
    A_2 = np.dot(A, A)
    m2 = np.dot((A_2 + a3 * A + a2 * np.identity(4)), B)
    A_3 = np.dot(A_2, A)
    m1 = np.dot((A_3 + a3 * A_2 + a2 * A + a1 * np.identity(4)), B)

    MCH = np.hstack((m1, m2, m3, m4))  # to stack column by column

    # Determination of  the closed loop coefficients

    ##poly Closed loop
    # z=0.707; # D=5#
    # wn=4;p1=-50 ;p2=-30 # 2 real stable poles and a second order
    z = 0.707  # D=5# TE==0,78s wn=8 saturation si wn=6 no saturation
    wn = 8
    p1 = -50
    p2 = -30  # 2 real stable poles and a second order

    coef1 = np.array([1, 2 * z * wn, wn ** 2])
    coef2 = np.array([1, -p1])
    coef3 = np.array([1, -p2])

    polyClosedLoop = np.convolve(coef1, np.convolve(coef2, coef3))
    # print(polyClosedLoop)
    # print(np.roots(polyClosedLoop))

    Ktilde = np.array([polyClosedLoop[4] - a0, polyClosedLoop[3] - a1, polyClosedLoop[2] - a2, polyClosedLoop[1] - a3])
    # print(Ktilde)

    MCHinv = np.linalg.inv(MCH)
    K = np.dot(Ktilde, MCHinv)
    K = np.reshape(K, (1, 4))
    #print(K)

    imag_part = ((4 * wn ** 2 - 4 * z ** 2 * wn ** 2) ** (1 / 2)) / 2
    p3 = complex(-wn * z, imag_part)
    p4 = np.conj(p3)
    p_d = [p1, p2, p3, p4]
    K_p = matlab.place(A, B, p_d)
    #print(K_p)

    # Closed loop system

    ACL = np.dot(B, K)
    ACL = A - ACL
    BCL = B
    CCL = C
    # several ways
    sysGCL = ctrl.ss(ACL, BCL, CCL, D)
    # print(sysGCL)

    TFCL = ctrl.ss2tf(ACL, BCL, CCL, D)
    numGCL = TFCL.num_array[0, 0]
    denGCL = TFCL.den_array[0, 0]
    for i in range(4):
        if 0.0005 > numGCL[i] > -0.0005:
            numGCL[i] = 0
        if 0.0005 > denGCL[i] > -0.0005:
            denGCL[i] = 0

    TFCL = ctrl.TransferFunction(numGCL, denGCL)
    # print(TFCL)

    if plot_pmap_bf:
        fig7, ax7 = plt.subplots()
        poles_cl = ctrl.poles(sysGCL)
        poles_real_cl = np.real(poles_cl)
        poles_im_cl = np.imag(poles_cl)
        ax7.scatter(poles_real_cl, poles_im_cl, marker='x', label='poles')
        zeros_cl = ctrl.zeros(sysGCL)
        zeros_real_cl = np.real(zeros_cl)
        zeros_im_cl = np.imag(zeros_cl)
        ax7.scatter(zeros_real_cl, zeros_im_cl, marker='o', label='zeros')
        ax7.set_xlabel('Real part')
        ax7.set_ylabel('Imaginary part')
        ax7.set_title('closed loop pzmap')
        ax7.legend()
        ax7.grid(True)

    poles_cl = ctrl.poles(sysGCL)
    zeros_cl = ctrl.zeros(sysGCL)

    # print(poles_cl)
    # print(np.linalg.eig(ACL))
    # print(ctrl.damp(sysGCL)

    if plot_step_bf:
        dt = 0.001
        tf = 2
        t = np.arange(0, tf, dt)
        x0 = np.array([[0], [0], [0], [0]])
        yc = []
        for i in range(len(t)):
            yc.append(np.pi / 5)
        tout, theta = ctrl.step_response(np.pi / 5 * sysGCL, t, x0)

        fig8, ax8 = plt.subplots()
        ax8.plot(tout, theta, label='theta')
        ax8.plot(tout, yc, label='input')

        ax8.set_xlabel('Time (s)')
        ax8.set_ylabel('Angle (rad)')
        ax8.set_title('Step response with state feedback')
        ax8.legend()
        ax8.grid(True)

    # print(ctrl.step_info(np.pi/5*sysGCL))
    # print(ctrl.zpk(poles_cl, zeros_cl, 1)) # J'ai pas la forme que je devrais avoir

    dc_gain = ctrl.dcgain(sysGCL)
    lc = 1 / dc_gain

    #print(lc)

    sysGCL_eps = ctrl.ss(ACL, BCL * lc, CCL, D)
    # print(sysGCL_eps)

    if plot_step_bf_gain:
        dt = 0.001
        tf = 1
        t = np.arange(0, tf, dt)
        x0 = np.array([[0], [0], [0], [0]])
        tout, theta, xout = ctrl.step_response(sysGCL_eps, t, x0, return_x=True)
        u = np.array([-1 * np.dot(K, xout)])
        u = np.reshape(u, np.shape(tout))
        u = np.clip(u, -8, 8)

        fig9, ax9 = plt.subplots()
        ax9.plot(tout, theta, label='theta')
        ax9.plot(tout, u, label='u')

        ax9.set_xlabel('Time (s)')
        ax9.set_ylabel('Angle (rad)')
        ax9.set_title('Step feedback with reference gain')
        ax9.legend()
        ax9.grid(True)

    if plot_input_bf:
        dt = 0.01
        tf = 1
        t = np.arange(0, tf, dt)
        x0 = np.array([[0], [0], [0], [0]])
        tout, theta, xout = ctrl.step_response(np.pi / 5 * sysGCL, return_x=True)
        u = np.array([-1 * np.dot(K, xout)])
        u = np.reshape(u, np.shape(tout))

        fig10, ax10 = plt.subplots()
        ax10.plot(tout, u)

        ax10.set_xlabel('Time (s)')
        ax10.set_ylabel('Command (V)')
        ax10.set_title('u for a state feedback without pregain')
        ax10.grid(True)

    if plot_lsim_pregain:
        dt = 0.01
        tf = 3
        t = np.arange(0, tf, dt)
        x0 = np.array([[0], [0], [0], [0]])
        yc = np.zeros((1, int(tf / dt)))
        for i in range(len(t)):
            if t[i] >= 1:
                yc[0,i] = lc
            else:
                yc[0,i] = 0
        signal_sys = signal.StateSpace(ACL, BCL * lc, CCL, D)
        yc = np.reshape(yc, np.shape(t))
        tout, y, x = signal.lsim(signal_sys, U=yc, T=t)

        x = np.transpose(x)
        u = np.array([-1 * np.dot(K, x)] + lc * yc)
        u = np.reshape(u, np.shape(tout))

        fig11, ax11 = plt.subplots()
        ax11.plot(tout, y, label='theta')
        ax11.plot(tout, yc, label='yc')

        ax11.set_xlabel('Time (s)')
        ax11.set_ylabel('Amplitude')
        ax11.set_title('Response to any input using lsim')
        ax11.grid(True)
        ax11.legend()
        ax11.grid(True)

    # Improvement of K
    wn = 8 # limite de stabilité avec wn = 15 et z = 0.8
    z = 0.8
    imag_part = ((4*wn**2-4*z**2*wn**2)**(1/2)) / 2
    p1 = complex(-wn*z, imag_part)
    p2 = np.conj(p1)
    p3 = 5*p2.real
    p4 = 5*p2.real - 0.5
    p_desired = [p1, p2, p3, p4]
    K_robust = matlab.place(A,B, p_desired)


    ACL_robust = np.dot(B, K_robust)
    ACL_robust = A - ACL_robust
    BCL_robust = B
    CCL_robust = C

    sysGCL_robust = ctrl.ss(ACL_robust, BCL_robust, CCL_robust, D)

    dc_gain_robust = ctrl.dcgain(sysGCL_robust)
    lc_robust = 1 / dc_gain_robust
    #print(K_robust)
    #print(lc_robust)
    tspan = (0.0, 2.0)
    t_eval = np.linspace(tspan[0], tspan[1], num=200)

    x0 = [0.0, 0.0, 0.0, 0.0]
    start_reference_time = 1
    start_amplitude = np.pi/5
    sol = solve_ivp(nxt.xdot, tspan, x0, t_eval=t_eval, method='RK45', args=(K_robust, lc_robust, consigne_temp, start_reference_time, start_amplitude))

    t = sol.t
    xout = sol.y
    theta_nlin = sol.y[0, :]
    psi_nlin = sol.y[1, :]

    #compute u with non linearized model

    command = np.zeros(len(t))
    yc = []
    for i in range(len(t)):
        yc_actuelle = consigne_temp(t[i], start_reference_time, start_amplitude)
        x_actuelle = xout[:, i]
        utheo = -np.dot(K_robust, x_actuelle) + yc_actuelle*lc_robust
        utheo = np.clip(utheo, -8.0, 8.0)
        command[i] = utheo[0]
        yc.append(yc_actuelle)


    # Non linear simulation (same as ode45)
    if plot_non_linear:
        fig12, ax12 = plt.subplots()
        ax12.plot(t, theta_nlin, label='theta')
        ax12.plot(t, psi_nlin, label='psi')
        ax12.plot(t, command, label='u')
        ax12.plot(t, yc, label='yc')

        ax12.set_xlabel('Time (s)')
        ax12.set_ylabel('Amplitude')
        ax12.set_title('Closed-loop non linearized response')
        ax12.grid(True)
        ax12.legend()

    if plot_compare_lin_nonlin_bf:
        fig13, ax13 = plt.subplots()
        ax13.plot(t, theta_nlin, label='theta_non_lin')
        ax13.plot(t, psi_nlin, label='psi_non_lin')
        ax13.plot(t, command, label='u_non_lin')
        ax13.plot(t, yc, label='yc')

        yc = np.array(yc)
        signal_sys = signal.StateSpace(ACL, BCL * lc, CCL, D)
        tout, y, x = signal.lsim(signal_sys, U=yc, T=t)

        x = np.transpose(x)
        psi_lin_bf = x[1,:]
        u = np.array([-1 * np.dot(K, x)] + lc * yc)
        u = np.reshape(u, np.shape(tout))

        ax13.plot(tout, y, '--',label='theta_lin')
        ax13.plot(tout, psi_lin_bf, '--', label='psi_lin')
        ax13.plot(tout, u, '--', label='u_lin')

        ax13.set_xlabel('Time (s)')
        ax13.set_ylabel('Amplitude')
        ax13.set_title('BF step response linearization comparison')
        ax13.grid(True)
        ax13.legend()

    # non linear simulation (euler approximation)
    if plot_non_linear_euler:
        dt = 0.0001

    if start_animation:
        anim = mp.MyAnimation(K_robust, lc_robust, 0, 1)

    plt.show()

if __name__ == "__main__":
    main()
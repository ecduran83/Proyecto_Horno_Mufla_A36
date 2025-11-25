import csv
import math
import numpy as np
from PySide6.QtWidgets import QFileDialog


class CalculosDatos:

    def __init__(self):
        # Iniciaremos los parametros que son constantes para cualquier cálculo

        # Cálculos de áreas relacionadas a los aislantes
        self.A_1 = 4 * (0.13 * 0.195) + 2 * (0.13 * 0.13)  # m2 Área interior del horno
        self.A_2 = 4 * (0.18 * 0.235) + 2 * (0.18 * 0.18)  # m2 Área entre el ladrillo y la fibra cerámica
        self.A_3 = 4 * (0.22 * 0.275) + 2 * (0.22 * 0.22)  # m2 Área entre la fibra cerámica y la lana de roca
        self.A_4 = 4 * (0.26 * 0.315) + 2 * (0.26 * 0.26)
        self.A_5 = 4 * (0.30 * 0.35) + 2 * (0.30 * 0.30)  # m2 Área exterior del horno (no se toma en cuenta placa de acero)

        # Cálculo de las áreas medias
        self.A_int = self.A_1
        self.A_1m = math.sqrt(self.A_1 * self.A_2)
        self.A_2m = math.sqrt(self.A_2 * self.A_3)
        self.A_3m = math.sqrt(self.A_3 * self.A_4)
        self.A_4m = math.sqrt(self.A_4 * self.A_5)
        self.A_ext = self.A_4

        # Para la termocupla, considerandolo como una esfera
        self.r_t = 0.0035 / 2  # m Radio de la esfera de la termocupla
        self.l_t = 0.004  # longitud de union expuesta despues de la cabeza
        self.A_t = 4 * math.pi * self.r_t ** 2 + 2 * math.pi * self.r_t * self.l_t  # m2 Area de la termocupla

        # Calculo de volumenes necesarios
        self.V_1 = 0.13 * 0.13 * 0.195
        self.V_2 = 0.16 * 0.16 * 0.215
        self.V_3 = 0.18 * 0.18 * 0.235
        self.V_4 = 0.20 * 0.20 * 0.255
        self.V_5 = 0.22 * 0.22 * 0.275
        self.V_6 = 0.24 * 0.24 * 0.295
        self.V_7 = 0.26 * 0.26 * 0.315
        self.V_8 = 0.28 * 0.28 * 0.335
        self.V_9 = 0.30 * 0.30 * 0.35

        # Datos necesarios para cada material
        # Ladrillos
        self.rho_w = 750#650  # kg/m3 densidad del ladrillo refractario aislante
        self.ce_w = 950#850  # J/kg-K Calor específico del ladrillo refractario
        self.k_w = 0.42  # W/m-K Conductividad térmica de ladrillo refractario
        self.m_w_1 = self.rho_w * (self.V_2 - self.V_1)  # kg masa entre el nodo 1 y nodo 1-2
        self.m_w_2 = self.rho_w * (self.V_3 - self.V_2)

        # Fibra cerámica
        self.rho_f = 260
        self.ce_f = 950
        self.k_f = 0.23
        self.m_f_1 = self.rho_f * (self.V_4 - self.V_3)
        self.m_f_2 = self.rho_f * (self.V_5 - self.V_4)

        # Lana de roca
        self.rho_l = 100
        self.ce_l = 840
        self.k_l = 0.08
        self.m_l_1 = self.rho_l * (self.V_6 - self.V_5)
        self.m_l_2 = self.rho_l * (self.V_7 - self.V_6)
        self.m_l_3 = self.rho_l * (self.V_8 - self.V_7)
        self.m_l_4 = self.rho_l * (self.V_9 - self.V_8)

        # Aire
        self.rho_a = 1.25  # kg/m3 densidad del aire
        self.ce_a = 1000  # J/kg-K Calor específico del aire
        self.m_a = self.rho_a * (self.V_1)  # Masa del aire

        # Coeficientes de convecciones dentro y fuera de la camara
        self.h_aip = 6  # W/m2-k Coeficiente de convección de aire a la pieza
        self.h_aiw = 6  # W/m2-K Coeficiente de convección de aire a la pared
        self.h_ao = 15.4  # W/m2-k Coeficiente de convección para el exterior

        # Termocupla
        self.rho_t = 8700
        self.ce_t = 485
        self.v_t = (4 / 3) * math.pi * (0.0035 / 2) ** 3
        self.m_t = self.rho_t * self.v_t
        self.e_t = 0.95

        # Calculando resistencias
        self.R_i_f = 0.025 / (self.k_w * self.A_1m)
        self.R_f_la = 0.02 / (self.k_f * self.A_2m)
        self.R_la_lb = 0.02 / (self.k_l * self.A_3m)
        self.R_lb_lc = 0.02 / (self.k_l * self.A_4m)
        self.R_lc_e = 1 / (self.h_ao * self.A_ext)

        self.dt = 1

        self.Kp = 0.252#0.252
        self.Ki = 0.0367#0.367
        self.Kd = 0.432#0.432

    # Funcion para el proceso que involucra, ademas de la temperatura, la masa y el tiempo
    def pid_temp_masa_tiempo(self, thermal_profile, material, masa, T_e):
        rho_p = material[0]
        ce_p = material[1]
        v_p = masa / rho_p
        m_p = masa
        e_p = material[2]
        sigma = 5.67e-8

        # Calculo del area de la pieza
        r_p = np.sqrt(v_p/(np.pi * 0.03))
        A_p = (2 * np.pi * r_p**2) + (2 * np.pi * r_p * 0.03)

        # Capacitancia interna
        C_t = self.m_t * self.ce_t
        C_p = m_p * ce_p
        C_a = self.m_a * self.ce_a
        C_w = self.m_w_1 * self.ce_w
        C_f = self.m_w_2 * self.ce_w + self.m_f_1 * self.ce_f
        C_la = self.m_f_2 * self.ce_f + self.m_l_1 * self.ce_l
        C_lb = self.m_l_2 * self.ce_l + self.m_l_3 * self.ce_l
        C_lc = self.m_l_4 * self.ce_l

        # Calculando constantes
        B_1 = (e_p * sigma * A_p * self.dt) / C_p
        B_2 = (self.h_aip * A_p * self.dt) / C_p
        B_3 = (self.h_aiw * self.A_int * self.dt) / C_a
        B_4 = (self.h_aip * A_p * self.dt) / C_a
        B_5 = self.dt / C_w
        B_6 = (self.h_aiw * self.A_int * self.dt) / C_w
        B_7 = (e_p * sigma * A_p * self.dt) / C_w
        B_8 = self.dt / (C_w * self.R_i_f)
        B_9 = self.dt / (C_f * self.R_i_f)
        B_10 = self.dt / (C_f * self.R_f_la)
        B_11 = self.dt / (C_la * self.R_f_la)
        B_12 = self.dt / (C_la * self.R_la_lb)
        B_13 = self.dt / (C_lb * self.R_la_lb)
        B_14 = self.dt / (C_lb * self.R_lb_lc)
        B_15 = self.dt / (C_lc * self.R_lb_lc)
        B_16 = self.dt / (C_lc * self.R_lc_e)
        B_17 = (self.e_t * sigma * self.A_t * self.dt) / C_t
        B_18 = (self.h_aip * self.A_t * self.dt) / C_t

        SETPOINT_TOLERANCE = 2.5

        # Ganancias PID (¡Estos son los valores que vamos a encontrar!)
        P_max = 2500

        # Variables de estado del PID
        MV = 0.0  # Variable Manipulada (Salida PID, 0 a 1)
        e_k = 0.0  # Error actual
        e_k1 = 0.0  # Error en (k-1)
        e_k2 = 0.0  # Error en (k-2)
        MV_k1 = 0.0  # Salida PID en (k-1)

        t_max = 0  # Tiempo total de simulación (s)
        for row_setup in thermal_profile:
            if row_setup['tipo'] == 'rampa':
                t_max += (row_setup['temp_obj_C'] / row_setup['tasa_C_min']) * 60
            elif row_setup['tipo'] == 'meseta':
                t_max += row_setup['duracion_min'] * 60
            elif row_setup['tipo'] == 'normal':
                t_max += 3600

        n_steps = int(t_max / self.dt)  # Número de pasos (debe ser entero)
        T_amb = T_e + 273.15  # Temperatura ambiente (K)

        # np.arange es exclusivo en el límite superior, por lo que sumamos dt
        t = np.arange(self.dt, t_max + self.dt, self.dt)

        T_t = np.zeros(n_steps)
        T_p = np.zeros(n_steps)
        T_a = np.zeros(n_steps)
        T_i = np.zeros(n_steps)
        T_f = np.zeros(n_steps)
        T_la = np.zeros(n_steps)
        T_lb = np.zeros(n_steps)
        T_lc = np.zeros(n_steps)
        SP_history = np.zeros(n_steps)  # Guardará el SP en cada paso (en K)

        # === Variables de estado para el ciclo ===
        current_step_index = 0
        current_setpoint_K = T_amb  # El setpoint actual que el PID debe seguir
        step_start_time_s = 0.0     # El tiempo (en seg) en que comenzó el proceso actual
        step_start_temp_K = T_amb
        last_step = ''

        # Condiciones iniciales (Python usa indexado 0)
        T_t[0] = T_amb
        T_i[0] = T_amb
        T_p[0] = T_amb
        T_a[0] = T_amb
        T_f[0] = T_amb
        T_la[0] = T_amb
        T_lb[0] = T_amb
        T_lc[0] = T_amb
        SP_history[0] = T_amb  # Asumiendo que el SP inicial es T_amb
        SP_K = T_amb
        # Bucle principal de cálculos
        for k in range(n_steps - 1):
            # Obtener temperaturas del paso anterior (k)
            T_t_k = T_t[k]
            T_i_k = T_i[k]
            T_p_k = T_p[k]
            T_a_k = T_a[k]
            T_f_k = T_f[k]
            T_la_k = T_la[k]
            T_lb_k = T_lb[k]
            T_lc_k = T_lc[k]

            # Medir la variable de proceso
            PV_K = T_t_k
            current_time_s = (k + 1) * self.dt

            # --- INICIO: LÓGICA DE CICLO TÉRMICO (MÁQUINA DE ESTADOS) ---
            if len(thermal_profile) > current_step_index:
                step = thermal_profile[current_step_index]

                if step['tipo'] == 'rampa':
                    last_step = 'rampa'
                    tasa_K_s = step['tasa_C_min'] / 60.0
                    temp_obj_K = step['temp_obj_C'] + 273.15

                    # Calcular el tiempo total necesario para esta rampa
                    if tasa_K_s == 0:
                        time_to_complete_s = 0.0
                    else:
                        time_to_complete_s = abs(temp_obj_K - step_start_temp_K) / abs(tasa_K_s)
                    time_in_step_s = current_time_s - step_start_time_s

                    if time_in_step_s >= time_to_complete_s:
                        SP_K = temp_obj_K
                        current_step_index += 1
                        step_start_time_s = current_time_s
                        step_start_temp_K = SP_K
                    else:
                        SP_K = step_start_temp_K + (tasa_K_s * time_in_step_s)

                elif step['tipo'] == 'meseta':
                    last_step = 'meseta'
                    SP_K = current_setpoint_K
                    duracion_s = step['duracion_min'] * 60.0
                    time_in_step_s = current_time_s - step_start_time_s

                    if time_in_step_s >= duracion_s:
                        current_step_index += 1
                        step_start_time_s = current_time_s
                        step_start_temp_K = SP_K

                elif step['tipo'] == 'normal':
                    last_step = 'normal'
                    temp_obj_K = step['temp_obj_C'] + 273.15

                    # El PID SIEMPRE persigue el setpoint de este paso
                    SP_K = temp_obj_K
                    # Comprobar si la temperatura (PV) ha llegado al setpoint
                    if abs(PV_K - temp_obj_K) < SETPOINT_TOLERANCE:
                        current_step_index += 1
                        step_start_time_s = current_time_s
                        step_start_temp_K = SP_K

                current_setpoint_K = SP_K
            else:
                if last_step == 'normal':
                    pass
                else:
                    SP_K = 273.15


            # 2. Calcular el Error actual
            e_k = SP_K - PV_K
            # 3. Calcular el PID (Forma de Velocidad Discreta)
            P_term = self.Kp * (e_k - e_k1)
            I_term = self.Ki * self.dt * e_k
            D_term = (self.Kd / self.dt) * (e_k - 2 * e_k1 + e_k2)

            delta_MV = P_term + I_term + D_term

            # 4. Actualizar y Saturar la Salida del Controlador (MV)
            MV = MV_k1 + delta_MV

            if MV > 1.0:
                MV = 1.0  # Saturar a 100% potencia
            elif MV < 0.0:
                MV = 0.0  # Saturar a 0% potencia

            # 5. Actualizar estados del PID para el próximo ciclo
            e_k2 = e_k1
            e_k1 = e_k
            MV_k1 = MV

            # 6. Calcular la Potencia de Entrada REAL
            Q_in = MV * P_max

            T_t[k + 1] = T_t_k + B_17 * (T_i_k ** 4 - T_t_k ** 4) + B_18 * (T_a_k - T_t_k)
            T_p[k + 1] = T_p_k + B_1 * (T_i_k ** 4 - T_p_k ** 4) + B_2 * (T_a_k - T_p_k)
            T_a[k + 1] = T_a_k + B_3 * (T_i_k - T_a_k) - B_4 * (T_a_k - T_a_k)
            T_i[k + 1] = T_i_k + B_5 * Q_in - B_6 * (T_i_k - T_a_k) - B_7 * (T_i_k ** 4 - T_p_k ** 4) - B_8 * (
                        T_i_k - T_f_k)
            T_f[k + 1] = T_f_k + B_9 * (T_i_k - T_f_k) - B_10 * (T_f_k - T_la_k)
            T_la[k + 1] = T_la_k + B_11 * (T_f_k - T_la_k) - B_12 * (T_la_k - T_lb_k)
            T_lb[k + 1] = T_lb_k + B_13 * (T_la_k - T_lb_k) - B_14 * (T_lb_k - T_lc_k)
            T_lc[k + 1] = T_lc_k + B_15 * (T_lb_k - T_lc_k) - B_16 * (T_lc_k - T_amb)

            SP_history[k + 1] = SP_K

        T_t = T_t - 273.15
        T_p = T_p - 273.15
        return [T_t, T_p, t]

    def temp_setpoint(self, setpoint, T_e):
        t_max = 3600                    # Tiempo total de simulación (s)
        n_steps = int(t_max / self.dt)  # Número de pasos (debe ser entero)
        T_amb = T_e                     # Temperatura ambiente (C)

        t = np.arange(self.dt, t_max + self.dt, self.dt)
        T_sp = np.zeros(n_steps)
        T_sp[0] = T_amb

        for k in range(1, n_steps):
            T_sp[k] = setpoint

        return [T_sp, t]


if __name__ == '__main__':
    calculos = CalculosDatos()
    thermal_profile = [
        {'tipo': 'normal', 'temp_obj_C': 950.0},
        {'tipo': 'meseta', 'duracion_min': 30.0},
    ]
    material = [7850, 470, 0.75]
    [T_t, T_p, t] = calculos.pid_temp_masa_tiempo(thermal_profile, material, 0.36, 77.5)




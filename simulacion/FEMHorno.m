clear; clc; close all;

% Calculo de areas para el procedimiento con nodos FEM
h = [0.13 0.18 0.22 0.26 0.30];     % Alturas de las superficies
w = [0.13 0.18 0.22 0.26 0.30];     % Ancho de las superficies
l = [0.195 0.235 0.275 0.313 0.35]; % Profundidad de las superficies

Areas = [];
for i=1:5
    Areas(i) = 4*(h(i)*l(i)) + 2*(h(i)*w(i));
    fprintf("Area %d: %4.2f\n", [i Areas(i)]);
end

AreasM = [];
for i=1:4
    AreasM(i) = sqrt(Areas(i)*Areas(i+1));
    fprintf("Area Media %d = %.2f m2\n", [i AreasM(i)])
end

%% 1. CONFIGURACIÓN Y PARÁMETROS
L1 = 0.020;         % Espesor Capa 1(Ladrillo Refractario)
L2 = 0.020;         % Espesor Capa 2(Fibra Cerámica)
L3 = 0.020;         % Espesor Capa 3(Lana de Roca 1)
L4 = 0.020;         % Espesor Capa 4(Lana de Roca 2)

% --- Propiedades de los Materiales [Capa1, Capa2, Capa3]
% Conductividad térmica [W/m·K]
k = [1.2, 0.20, 0.075 0.075]; 
% Densidad [kg/m^3]
rho = [2300, 260, 100, 100];
% Calor específico [J/kg·K]
c = [1008, 950, 840, 840];

% --- Condiciones de Frontera e Iniciales
T_amb = 15;    % Temperatura ambiente exterior [°C]
h = 15;        % Coeficiente de convección exterior [W/m^2·K]
T_inicial = 15; % Temperatura inicial de toda la pared [°C]

% --- Perfil de Temperatura del Horno (Interior)
T_final_horno = 1000; % Temperatura objetivo del horno para el acero A36 [°C]
tiempo_rampa = 3600; % Tiempo para alcanzar T_final_horno (1 hora) [s]

% Parametros de la Simulación
t_total = 3*3600; % Tiempo total de simulación (2 horas) [s]
dt = 20;        % Paso de tiempo [s]
theta = 0.5;    % Método de Crank-Nicolson (0.5 es estable y preciso)

%% 2. DISCRETIZACIÓN Y MALLA
% Definimos 4 nodos, uno en cada interfaz
n_nodos = 5;
n_elem = 4;

% Coordenadas de los nodos
nodos_coord = [0, L1, L1+L2, L1+L2+L3, L1+L2+L3+L4];

% Conectividad de los elementos (qué nodos conecta cada elemento)
elem_conec = [1, 2;  % Elemento 1 conecta nodos 1 y 2
              2, 3;  % Elemento 2 conecta nodos 2 y 3
              3, 4;  % Elemento 2 conecta nodos 3 y 4
              4, 5]; % Elemento 3 conecta nodos 4 y 5
          

%% 3. CÁLCULO Y ENSAMBLAJE DE MATRICES GLOBALES
% Inicializamos las matrices globales con ceros
K_global = zeros(n_nodos, n_nodos);
C_global = zeros(n_nodos, n_nodos);

for i = 1:n_elem
    % Nodos del elemento actual
    nodo1 = elem_conec(i, 1);
    nodo2 = elem_conec(i, 2);
    
    % Longitud del elemento
    Le = nodos_coord(nodo2) - nodos_coord(nodo1);
    
    % Matriz de rigidez del elemento [k_e]
    ke = (AreasM(i) * k(i) / Le) * [1, -1; -1, 1];
    
    % Matriz de capacidad del elemento [c_e]
    ce = (rho(i) * c(i) * AreasM(i) * Le / 6) * [2, 1; 1, 2];
    
    % Ensamblaje en las matrices globales
    indices = [nodo1, nodo2];
    K_global(indices, indices) = K_global(indices, indices) + ke;
    C_global(indices, indices) = C_global(indices, indices) + ce;
end

%% 4. BUCLE DE SIMULACIÓN TRANSITORIA
% Vector de tiempo para graficar
tiempo = 0:dt:t_total;
n_pasos = length(tiempo);

% Matriz para guardar los resultados de temperatura
T_resultados = zeros(n_nodos, n_pasos);
T_resultados(:, 1) = T_inicial; % Condición inicial

% Vector de temperatura del paso anterior
T_anterior = T_resultados(:, 1);

% Matrices del esquema Theta (para no recalcularlas en cada paso)
A_izq_base = (C_global / dt) + theta * K_global;
A_der_base = (C_global / dt) - (1 - theta) * K_global;

% Bucle principal
for i = 2:n_pasos
    % --- Definir la temperatura interior del horno en este paso de tiempo
    t_actual = tiempo(i);
    if t_actual <= tiempo_rampa
        % Calentamiento en rampa lineal
        T_horno_actual = T_inicial + (T_final_horno - T_inicial) * (t_actual / tiempo_rampa);
    else
        % Mantenimiento de temperatura
        T_horno_actual = T_final_horno;
    end
    
    % --- Copiar las matrices base para aplicar condiciones de frontera
    A_izq = A_izq_base;
    b_der = A_der_base * T_anterior;
    
    % --- Aplicar Condiciones de Frontera
    % 1. Temperatura Fija (Dirichlet) en el Nodo 1 (Interior del horno)
    A_izq(1,:) = 0;
    A_izq(1,1) = 1;
    b_der(1) = T_horno_actual;
    
     % 2. Convección (Robin) en el Nodo 5 (Exterior)
    A_izq(n_nodos, n_nodos) = A_izq(n_nodos, n_nodos) + theta * h * Areas(5);
    b_der(n_nodos) = b_der(n_nodos) - (1-theta) * h * Areas(5) * T_anterior(n_nodos) + h * Areas(5) * T_amb;

    % --- Resolver el sistema de ecuaciones para el paso actual
    T_actual = A_izq \ b_der;
    
    % --- Guardar resultados y actualizar para el siguiente paso
    T_resultados(:, i) = T_actual;
    T_anterior = T_actual;
end

%% 5. VISUALIZACIÓN DE RESULTADOS
figure;
hold on;
plot(tiempo / 60, T_resultados(1,:), 'r-', 'LineWidth', 2); % Temperatura interior del horno
plot(tiempo / 60, T_resultados(2,:), 'b--', 'LineWidth', 2); % Temperatura Interfaz 1-2
plot(tiempo / 60, T_resultados(3,:), 'g-.', 'LineWidth', 2); % Temperatura Interfaz 2-3
plot(tiempo / 60, T_resultados(4,:), 'k:', 'LineWidth', 2);  % Temperatura exterior
plot(tiempo / 60, T_resultados(5,:), 'k-', 'LineWidth', 2);  % Temperatura exterior

title('Evolución de Temperaturas en las Paredes del Horno');
xlabel('Tiempo (minutos)');
ylabel('Temperatura (°C)');
legend('Interior (Nodo 1)', 'Refractario-Fibra (Nodo 2)', 'Fibra-Lana (Nodo 3)', 'Lana-Lana (Nodo 4)', 'Exterior (Nodo 5)', 'Location', 'southeast');
grid on;
box on;
hold off;

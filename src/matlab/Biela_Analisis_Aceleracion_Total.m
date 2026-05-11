%% Parámetros
% 1 g = 9.80665 m/s^2
G_TO_MMS2 = 9806.65;

% --- AJUSTE DE GRAVEDAD ---
% Restamos 1.0g (o 0.97g según tu calibración) al eje Y 
% para que el cálculo Total sea puramente cinemático (como Inventor).
GRAVEDAD_Y = 1.0; 
% --------------------------

%% Configuración Puerto Serie
PORT = "COM10"; BAUD = 115200; DURACION_SEG = 60;
if ~isempty(instrfind), fclose(instrfind); delete(instrfind); end
s = serialport(PORT, BAUD, "Timeout", 5);
configureTerminator(s,"CR/LF"); flush(s); pause(2);

% Esperar header
disp("Esperando datos del Arduino...");
t0 = tic; while toc(t0) < 10
    if s.NumBytesAvailable>0
        line = strtrim(readline(s));
        if startsWith(line,"#"), disp("Header: "+line); break; end
    else, pause(0.05); end
end

%% --- CONFIGURACIÓN DE GRÁFICAS (5 VENTANAS) ---

% Fig 1: Giroscopio
f_gz = figure('Name','Vel. Angular','NumberTitle','off');
ax_gz = gca; hGz = animatedline(ax_gz, 'Color', 'b'); grid(ax_gz,'on');
ylabel(ax_gz,'Vel [°/s]'); xlabel(ax_gz,'t [s]');
title(ax_gz, 'Velocidad Angular');

% Fig 2: Aceleración X
f_ax = figure('Name','Ac X','NumberTitle','off');
ax_ax = gca; hAx = animatedline(ax_ax, 'Color', '#D95319'); grid(ax_ax,'on'); % Naranja
ylabel(ax_ax,'Ax [mm/s^2]'); xlabel(ax_ax,'t [s]');
title(ax_ax, 'Aceleración en X');

% Fig 3: Aceleración Y (Corregida)
f_ay = figure('Name','Ac Y (Sin Gravedad)','NumberTitle','off');
ax_ay = gca; hAy = animatedline(ax_ay, 'Color', '#77AC30'); grid(ax_ay,'on'); % Verde
ylabel(ax_ay,'Ay [mm/s^2]'); xlabel(ax_ay,'t [s]');
title(ax_ay, 'Aceleración en Y');

% Fig 4: Aceleración Z
f_az = figure('Name','Ac Z','NumberTitle','off');
ax_az = gca; hAz = animatedline(ax_az, 'Color', '#7E2F8E'); grid(ax_az,'on'); % Morado
ylabel(ax_az,'Az [mm/s^2]'); xlabel(ax_az,'t [s]');
title(ax_az, 'Aceleración en Z');

% --- NUEVA: FIGURA 5 (ACELERACIÓN TOTAL) ---
f_total = figure('Name','Aceleración TOTAL (Magnitud)','NumberTitle','off');
ax_total = gca; hTotal = animatedline(ax_total, 'Color', 'r', 'LineWidth', 1.5); 
grid(ax_total,'on');
ylabel(ax_total,'|A| Total [mm/s^2]'); xlabel(ax_total,'t [s]');
title(ax_total, 'Aceleración Total');
% -------------------------------------------

% Buffers
t_ms = []; gz_dps = []; ax_g = []; ay_g = []; az_g = [];
tStart = tic;

disp("Capturando datos...");

while isvalid(f_gz) && isvalid(f_total) && (isinf(DURACION_SEG) || toc(tStart)<DURACION_SEG)
    if s.NumBytesAvailable==0, pause(0.005); continue; end
    line = strtrim(readline(s));
    if line=="" || startsWith(line,"#"), continue; end
    p = split(line,',');
    
    if numel(p) < 5, continue; end
    v = str2double(p(1:5)); if any(isnan(v)), continue; end
    
    t_ms(end+1,1) = v(1);
    gz_dps(end+1,1) = v(2);
    ax_g(end+1,1) = v(3);
    ay_g(end+1,1) = v(4);
    az_g(end+1,1) = v(5);
    
    if numel(t_ms) < 10, continue; end
    
    % Preparar datos actuales
    t = (t_ms - t_ms(1))/1000;      
    N = numel(t); 
    t_N = t(N);
    
    % 1. Obtener valores crudos en g
    raw_ax = ax_g(N);
    raw_ay = ay_g(N);
    raw_az = az_g(N);
    
    % 2. Calcular valores corregidos (Sin gravedad en Y)
    val_ax = raw_ax * G_TO_MMS2;
    val_ay = (raw_ay - GRAVEDAD_Y) * G_TO_MMS2; % Restamos gravedad
    val_az = raw_az * G_TO_MMS2;
    
    % 3. CALCULAR MAGNITUD TOTAL (La curva roja)
    % Pitágoras en 3D: sqrt(ax^2 + ay^2 + az^2)
    val_total = sqrt(val_ax^2 + val_ay^2);
    
    % 4. Graficar
    addpoints(hGz, t_N, gz_dps(N));
    addpoints(hAx, t_N, val_ax);
    addpoints(hAy, t_N, val_ay);
    addpoints(hAz, t_N, val_az);
    
    % Graficar la roja
    addpoints(hTotal, t_N, val_total);
    
    drawnow limitrate
end
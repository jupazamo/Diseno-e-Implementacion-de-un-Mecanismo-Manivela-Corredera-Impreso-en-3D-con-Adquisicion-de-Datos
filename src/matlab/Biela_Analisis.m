%% Parámetros
% 1 g = 9.80665 m/s^2
G_TO_MMS2 = 9806.65;

% --- AJUSTE MANUAL ---
% Como tu sensor mide la gravedad en Y, le restamos 1.0 g.
% Si ves que la gráfica queda un poco por debajo de cero, 
% cambia este 1.0 por 0.97 (que es lo que vimos en tu foto anterior).
GRAVEDAD_Y = 1.0; 
% ---------------------

%% Configuración Puerto Serie
PORT = "COM10"; BAUD = 115200; DURACION_SEG = 60;
if ~isempty(instrfind), fclose(instrfind); delete(instrfind); end
s = serialport(PORT, BAUD, "Timeout", 5);
configureTerminator(s,"CR/LF"); flush(s); pause(2);

% Esperar header
t0 = tic; while toc(t0) < 10
    if s.NumBytesAvailable>0
        line = strtrim(readline(s));
        if startsWith(line,"#"), disp("Header: "+line); break; end
    else, pause(0.05); end
end

% --- 4 Figuras ---
f_gz = figure('Name','Velocidad Angular Z','NumberTitle','off');
ax_gz = gca; hGz = animatedline(ax_gz, 'Color', 'b'); grid(ax_gz,'on');
ylabel(ax_gz,'Vel. [°/s]'); xlabel(ax_gz,'t [s]');

f_ax = figure('Name','Aceleración X','NumberTitle','off');
ax_ax = gca; hAx = animatedline(ax_ax, 'Color', 'r'); grid(ax_ax,'on');
ylabel(ax_ax,'Ac X [mm/s^2]'); xlabel(ax_ax,'t [s]');

f_ay = figure('Name','Aceleración Y (Sin Gravedad)','NumberTitle','off');
ax_ay = gca; hAy = animatedline(ax_ay, 'Color', 'g'); grid(ax_ay,'on');
ylabel(ax_ay,'Ac Y [mm/s^2]'); xlabel(ax_ay,'t [s]');
title(ax_ay, 'Comparativa Inventor (Offset aplicado)');

f_az = figure('Name','Aceleración Z','NumberTitle','off');
ax_az = gca; hAz = animatedline(ax_az, 'Color', 'm'); grid(ax_az,'on');
ylabel(ax_az,'Ac Z [mm/s^2]'); xlabel(ax_az,'t [s]');

% Buffers
t_ms = []; gz_dps = []; ax_g = []; ay_g = []; az_g = [];
tStart = tic;

while isvalid(f_gz) && isvalid(f_ax) && isvalid(f_ay) && isvalid(f_az) && (isinf(DURACION_SEG) || toc(tStart)<DURACION_SEG)
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
    
    t = (t_ms - t_ms(1))/1000;      
    N = numel(t); 
    
    % Valores actuales
    t_N = t(N);
    
    % GRAFICAR X y Z (Normales)
    addpoints(hGz, t_N, gz_dps(N));  
    addpoints(hAx, t_N, ax_g(N) * G_TO_MMS2);  
    addpoints(hAz, t_N, az_g(N) * G_TO_MMS2);  
    
    % --- GRAFICAR Y (CON RESTA) ---
    % Aquí hacemos la resta simple: (ValorLeido - 1.0) * 9806
    val_Y_corregido = (ay_g(N) - GRAVEDAD_Y) * G_TO_MMS2;
    addpoints(hAy, t_N, val_Y_corregido);  
    % ------------------------------
    
    drawnow limitrate
end
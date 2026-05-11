import serial
import numpy as np
import pyqtgraph as pg
from pyqtgraph import exporters
from pyqtgraph.Qt import QtWidgets, QtCore
import time
import csv
import os
from datetime import datetime
from collections import deque

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

PORT  = 'COM4'
BAUD  = 115200

GRAVEDAD_Y   = 1.0
G_TO_MMS2    = 9806.65

# --- EMA por eje (alpha: 0=muy suave, 1=sin filtro) --------------------------
EMA = {
    'gz': 0.30,   # gyro estaba bien → filtro liviano
    'ax': 0.20,
    'ay': 0.15,   # la más sucia → más suavizado
    'az': 0.20,
}

# --- Rechazo de outliers por eje (mm/s² para accel, °/s para gyro) -----------
# Un sample se descarta si se aleja más de este umbral del valor EMA previo.
# Ajustar según la dinámica real de tu mecanismo.
OUTLIER_THRESHOLD = {
    'gz': 60,      # °/s  — picos de gyro eran menores
    'ax': 8000,    # mm/s²
    'ay': 6000,
    'az': 8000,
}

# --- Ventana deslizante de visualización (s). None = mostrar todo ------------
DISPLAY_WINDOW_SEC = None

# --- Carpeta de salida -------------------------------------------------------
OUTPUT_DIR = "imu_exports"

# =============================================================================
# SERIAL
# =============================================================================

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)
print("Esperando datos del LSM6DS3...")

# =============================================================================
# FILTRO: EMA + OUTLIER REJECTION
# =============================================================================

ema_state = {k: None for k in ('gz', 'ax', 'ay', 'az')}
outlier_count = {k: 0 for k in ('gz', 'ax', 'ay', 'az')}

def filter_sample(key, raw):
    """
    1. Si el valor se aleja más de OUTLIER_THRESHOLD del EMA previo → descartar
       y devolver el último EMA (no contamina el filtro).
    2. Si pasa el test → actualizar EMA normalmente.
    """
    prev = ema_state[key]

    if prev is not None and abs(raw - prev) > OUTLIER_THRESHOLD[key]:
        outlier_count[key] += 1
        return prev                              # devuelve último valor válido

    alpha = EMA[key]
    if prev is None:
        ema_state[key] = raw
    else:
        ema_state[key] = alpha * raw + (1.0 - alpha) * prev

    return ema_state[key]

# =============================================================================
# APP QT
# =============================================================================

app = QtWidgets.QApplication([])

main_widget = QtWidgets.QWidget()
main_widget.setWindowTitle("IMU Monitor — LSM6DS3")
main_layout = QtWidgets.QVBoxLayout(main_widget)

# ── Barra de control ─────────────────────────────────────────────────────────
ctrl = QtWidgets.QHBoxLayout()

lbl_status = QtWidgets.QLabel("Esperando datos...")
ctrl.addWidget(lbl_status)

lbl_outliers = QtWidgets.QLabel("")
lbl_outliers.setStyleSheet("color: orange;")
ctrl.addWidget(lbl_outliers)

ctrl.addStretch()

btn_save = QtWidgets.QPushButton("💾  Guardar PNG + CSV")
btn_save.setFixedHeight(30)
ctrl.addWidget(btn_save)

main_layout.addLayout(ctrl)

# ── Gráficas 2×2 ─────────────────────────────────────────────────────────────
gw = pg.GraphicsLayoutWidget()
main_layout.addWidget(gw)

plots = {
    'gz': gw.addPlot(row=0, col=0, title="Velocidad Angular Z (°/s)"),
    'ax': gw.addPlot(row=0, col=1, title="Aceleración X (mm/s²)"),
    'ay': gw.addPlot(row=1, col=0, title="Aceleración Y (mm/s²)"),
    'az': gw.addPlot(row=1, col=1, title="Aceleración Z (mm/s²)"),
}

colors_filt = {'gz': 'b', 'ax': 'r', 'ay': 'g', 'az': 'm'}
colors_raw  = {
    'ax': (255, 80,  80,  60),
    'ay': (80,  255, 80,  60),
    'az': (200, 80,  255, 60),
}

curves_filt = {}
curves_raw  = {}

for key, p in plots.items():
    p.showGrid(x=True, y=True, alpha=0.3)
    p.setLabel('bottom', 'Tiempo (s)')
    curves_filt[key] = p.plot(pen=pg.mkPen(colors_filt[key], width=1.8),
                               name="filtrado")
    if key != 'gz':
        curves_raw[key] = p.plot(pen=pg.mkPen(colors_raw[key], width=1),
                                  name="crudo")

main_widget.resize(1280, 720)
main_widget.show()

# =============================================================================
# BUFFERS
# =============================================================================

t_data  = []
gz_f    = [];  ax_f  = [];  ay_f  = [];  az_f  = []
ax_raw  = [];  ay_raw = []; az_raw = []

t0 = None
n_samples = 0

# =============================================================================
# EXPORTACIÓN
# =============================================================================

def save_data():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # PNG — captura del widget completo
    exp = exporters.ImageExporter(gw.scene())
    exp.parameters()['width'] = 1920
    png_path = os.path.join(OUTPUT_DIR, f"imu_{stamp}.png")
    exp.export(png_path)
    print(f"PNG guardado: {png_path}")

    # CSV
    csv_path = os.path.join(OUTPUT_DIR, f"imu_{stamp}.csv")
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['t_s', 'gz_filt_dps',
                    'ax_filt_mms2', 'ay_filt_mms2', 'az_filt_mms2',
                    'ax_raw_mms2',  'ay_raw_mms2',  'az_raw_mms2'])
        for i in range(len(t_data)):
            w.writerow([
                f"{t_data[i]:.4f}",
                f"{gz_f[i]:.4f}",
                f"{ax_f[i]:.2f}", f"{ay_f[i]:.2f}", f"{az_f[i]:.2f}",
                f"{ax_raw[i]:.2f}", f"{ay_raw[i]:.2f}", f"{az_raw[i]:.2f}",
            ])
    print(f"CSV guardado: {csv_path}")

    total_out = sum(outlier_count.values())
    lbl_status.setText(
        f"✅ Guardado en '{OUTPUT_DIR}/'  |  "
        f"Outliers descartados: gz={outlier_count['gz']}  "
        f"ax={outlier_count['ax']}  ay={outlier_count['ay']}  az={outlier_count['az']}"
    )

btn_save.clicked.connect(save_data)

# =============================================================================
# LOOP DE ACTUALIZACIÓN
# =============================================================================

def update():
    global t0, n_samples

    while ser.in_waiting:
        line = ser.readline().decode(errors='ignore').strip()
        if not line or line.startswith('#'):
            if line:
                print(line)
            return

        parts = line.split(',')
        if len(parts) < 5:
            return
        try:
            vals = list(map(float, parts[:5]))
        except ValueError:
            return

        t_ms, gz_raw, ax_g, ay_g, az_g = vals

        if t0 is None:
            t0 = t_ms
        t = (t_ms - t0) / 1000.0

        # Conversión a mm/s²
        ax_mm = ax_g * G_TO_MMS2
        ay_mm = ay_g * G_TO_MMS2
        az_mm = az_g * G_TO_MMS2

        # Guardar crudo
        ax_raw.append(ax_mm)
        ay_raw.append(ay_mm)
        az_raw.append(az_mm)

        # Filtrar
        gz_fv = filter_sample('gz', gz_raw)
        ax_fv = filter_sample('ax', ax_mm)
        ay_fv = filter_sample('ay', ay_mm)
        az_fv = filter_sample('az', az_mm)

        t_data.append(t)
        gz_f.append(gz_fv)
        ax_f.append(ax_fv)
        ay_f.append(ay_fv)
        az_f.append(az_fv)

        n_samples += 1

    if not t_data:
        return

    # Vista (ventana deslizante opcional)
    if DISPLAY_WINDOW_SEC:
        ta = np.array(t_data)
        idx = np.where(ta >= ta[-1] - DISPLAY_WINDOW_SEC)[0]
        sl = slice(idx[0], None)
    else:
        sl = slice(None)

    tv = t_data[sl] if isinstance(sl, slice) else [t_data[i] for i in idx]

    def v(lst): return lst[sl] if isinstance(sl, slice) else [lst[i] for i in idx]

    curves_filt['gz'].setData(tv if not isinstance(tv, list) else tv,
                               v(gz_f) if not isinstance(tv, list) else v(gz_f))

    for key, filt, raw in [('ax', ax_f, ax_raw),
                             ('ay', ay_f, ay_raw),
                             ('az', az_f, az_raw)]:
        # numpy para el slice limpio
        ta = np.array(t_data)
        tf = np.array(filt)
        tr = np.array(raw)
        if DISPLAY_WINDOW_SEC:
            idx2 = ta >= ta[-1] - DISPLAY_WINDOW_SEC
            curves_filt[key].setData(ta[idx2], tf[idx2])
            curves_raw[key].setData(ta[idx2], tr[idx2])
        else:
            curves_filt[key].setData(ta, tf)
            curves_raw[key].setData(ta, tr)

    if DISPLAY_WINDOW_SEC:
        ta2 = np.array(t_data)
        idx2 = ta2 >= ta2[-1] - DISPLAY_WINDOW_SEC
        curves_filt['gz'].setData(ta2[idx2], np.array(gz_f)[idx2])
    else:
        curves_filt['gz'].setData(np.array(t_data), np.array(gz_f))

    # Status bar
    total_out = sum(outlier_count.values())
    lbl_status.setText(
        f"{n_samples} muestras  |  t = {t_data[-1]:.1f}s  |  "
        f"Outliers: gz={outlier_count['gz']} "
        f"ax={outlier_count['ax']} ay={outlier_count['ay']} az={outlier_count['az']}"
    )

# =============================================================================
# TIMER + RUN
# =============================================================================

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)

QtWidgets.QApplication.instance().exec()

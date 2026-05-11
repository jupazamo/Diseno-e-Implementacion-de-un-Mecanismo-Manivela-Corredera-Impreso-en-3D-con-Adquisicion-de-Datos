#include "SparkFunLSM6DS3.h"
#include "Wire.h"

LSM6DS3 imu(I2C_MODE, 0x6B);
float gBiasZ = 0;

// ─────────────────────────────────────────────
// REGISTRO CTRL1_XL (0x10) del LSM6DS3
//
//  bits [7:4]  ODR_XL  → 0101 = 208 Hz
//  bits [3:2]  FS_XL   → 01   = ±16g   ← CAMBIO CLAVE
//  bits [1:0]  LPF     → 00
//
//  0101 01 00 = 0x54
// ─────────────────────────────────────────────
#define CTRL1_XL        0x10
#define ODR_208HZ_16G   0x54   // 208 Hz + ±16g

void calibrateGyroZ(unsigned long ms = 2000) {
  double sum = 0;
  unsigned long n = 0;
  unsigned long t0 = millis();
  while (millis() - t0 < ms) {
    sum += imu.readFloatGyroZ();
    n++;
    delay(2);
  }
  gBiasZ = sum / n;
  Serial.print("# Bias gyro Z: ");
  Serial.print(gBiasZ, 4);
  Serial.println(" °/s");
}

void setup() {
  Serial.begin(115200);
  delay(1500);

  if (imu.begin() != 0) {
    Serial.println("# ERROR: LSM6DS3 no encontrado");
    while (1);
  }

  // Configurar acelerómetro: 208 Hz + ±16g
  imu.writeRegister(CTRL1_XL, ODR_208HZ_16G);
  delay(100);

  // Verificar que se escribió correctamente
  uint8_t reg_val = 0;
  imu.readRegister(&reg_val, CTRL1_XL);
  Serial.print("# CTRL1_XL = 0x");
  Serial.print(reg_val, HEX);
  if (reg_val == ODR_208HZ_16G) {
    Serial.println("  ✓ Rango ±16g confirmado");
  } else {
    Serial.println("  ✗ ERROR: valor inesperado");
  }

  delay(200);
  Serial.println("# Calibrando gyro Z, mantener en reposo...");
  calibrateGyroZ(2000);

  Serial.println("# Rango accel : ±16g");
  Serial.println("# ODR         : 208 Hz");
  Serial.println("# Gyro rango  : ±2000 °/s (default)");
  Serial.println("# Formato     : t_ms,gz_dps,ax_g,ay_g,az_g");
  Serial.println("# ready");
}

void loop() {
  unsigned long t = millis();

  float gz = imu.readFloatGyroZ() - gBiasZ;
  float ax = imu.readFloatAccelX();
  float ay = imu.readFloatAccelY();
  float az = imu.readFloatAccelZ();

  Serial.print(t);
  Serial.print(",");
  Serial.print(gz, 4);
  Serial.print(",");
  Serial.print(ax, 4);
  Serial.print(",");
  Serial.print(ay, 4);
  Serial.print(",");
  Serial.println(az, 4);

  delay(5); // ~200 Hz
}

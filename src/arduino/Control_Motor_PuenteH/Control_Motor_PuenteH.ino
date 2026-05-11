// Pines
const int ENB = 3;   // PWM
const int IN3 = 5;
const int IN4 = 4;

void setup() {
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop() {

  // Adelante
  adelante(200);
  delay(3000);

  // Stop
  detener();
  delay(1000);

  // Atrás
  atras(200);
  delay(3000);

  // Stop
  detener();
  delay(1000);
}

// =======================

void adelante(int velocidad) {
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, velocidad);
}

void atras(int velocidad) {
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, velocidad);
}

void detener() {
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 0);
}
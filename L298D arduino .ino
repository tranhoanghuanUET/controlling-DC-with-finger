int motorPin1 = 9;  // Chân nối với IN1 trên module L298N
int motorPin2 = 10; // Chân nối với IN2 trên module L298N
int enablePin = 8;  // Chân nối với ENA trên module L298N (có thể nối trực tiếp với VCC)

void setup() {
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(enablePin, OUTPUT);
  digitalWrite(enablePin, HIGH);  // Bật module L298N
  Serial.begin(9600); // Khởi động giao tiếp Serial với baud rate 9600
  Serial.println("Arduino is ready"); // In ra thông báo khi Arduino sẵn sàng
}

void loop() {
  if (Serial.available() > 0) {  // Kiểm tra nếu có dữ liệu tới từ cổng Serial
    char data = Serial.read();   // Đọc dữ liệu từ cổng Serial
    if (data == '1') {
      digitalWrite(motorPin1, HIGH); // Bật motor
      digitalWrite(motorPin2, LOW);  // Đảo chiều motor nếu cần
      Serial.println("Motor ON");    // In ra thông báo khi bật motor
    } else if (data == '0') {
      digitalWrite(motorPin1, LOW);  // Tắt motor
      digitalWrite(motorPin2, LOW);  // Đảm bảo motor tắt
      Serial.println("Motor OFF");   // In ra thông báo khi tắt motor
    }
  }
}

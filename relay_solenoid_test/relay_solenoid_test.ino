int relayPin = 8; 

void setup() {
  pinMode(relayPin, OUTPUT);
  Serial.begin(9600);
  Serial.println("系统启动，开始测试...");
}

void loop() {
  digitalWrite(relayPin, HIGH); // 
  Serial.println("阀门打开");
  delay(1000); //
  
  digitalWrite(relayPin, LOW);  //
  Serial.println("阀门关闭");
  delay(1000); // 
}

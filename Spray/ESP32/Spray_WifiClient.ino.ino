#include "WiFi.h"
#include "AsyncUDP.h"
#include <WiFiAP.h>


const char * ssid = "TP-Link_C1B5";
const char * password = "56991765";
int PORT = 8893;

IPAddress local_IP(10,170,43,10);    
// Set your Gateway IP address
IPAddress gateway(10,170,43,1);
IPAddress subnet(255, 255, 255, 0);
IPAddress primaryDNS(8, 8, 8, 8);   //optional
IPAddress secondaryDNS(8, 8, 4, 4); //optional

/*
//request:
My:x y(motorID):x(pwm)
Py:x y(motorID):y(pos)

//response
My:pos,pwm,current
*/

//BOARD SETTINGS
//GRIPPER MOTOR1:
//ADC motor: D32
//ADC pos:D35
//DIR: D21
//PWM: D19
//GRIPPER MOTOR2:
//ADC motor: VN
//ADC pos:D34
//DIR: D18
//PWM: D5
//PUMP MOTOR
//ADC pos:VP
//DIR:D23
//PWM:D22
//SUCTION MOTOR
//ADC motor: D33
//DIR: RX0
//PWM: TX0


#define PWM_Res   8
#define PWM_Freq  1000

#define POSITION_THRESHOLD 20       //2mm is the max position threshold to move the motor
#define TIMER_THRESHOLD 2000      //a single command can run for 1 seconds max
#define CURRENT_THRESHOLD (0xFFFFFFFF)   //Is 1.6Ampere

#define FORWARD HIGH
#define BACKWARD LOW

#define PINDIR 23
#define PINPWM 22

//4095 is 3.3Volt
//DRV8801 current is 500mV/A
//MAX DRV current is 2.8Ampere, that is a 1.4V
//1.4V is 4096/3.3*1.4 = 1737count

AsyncUDP udp;

unsigned long timeFire = 0;

void UDPCallBack(AsyncUDPPacket packet)
{
  int iTmp;
  //Turn incoming data into a max 64byte string
  char tBuffer[64];
  memset(tBuffer,0,64);
  memcpy(tBuffer,packet.data(),packet.length());
  String myString = tBuffer;
  String myResponse = "error";  

  Serial.print(myString);

  //Now we can manipulate the string

  //Suction CUP
  if (myString.startsWith("G:") == true)
  {
    myString.replace("G:","");
    iTmp = myString.toInt();
    timeFire = iTmp;
    Serial.print("trimmed string");
    Serial.println(myString);
    Serial.print("dec value:");
    Serial.println(iTmp);
    myResponse = "gH:0";
  }
  
  Serial.println(myResponse);
  
  //reply to the client
  memset(tBuffer,0,64);
  myResponse.toCharArray(tBuffer, 64);
  packet.printf(tBuffer); 
}

void(* resetFunc) (void) = 0; //declare reset function @ address 0

void setup()
{
   
    Serial.begin(115200);
    
    WiFi.mode(WIFI_STA);    
    //WiFi.config(ip);
    

    // Configures static IP address
    if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
      Serial.println("STA Failed to configure");
    }    
    WiFi.begin(ssid, password);
    if (WiFi.waitForConnectResult() != WL_CONNECTED) {
        Serial.println("WiFi Failed");
        while(1) {
            delay(10000);
            resetFunc();  //call reset
            delay(1000);
        }
    }

/*

  WiFi.softAP("ESP32_gripper");
  Serial.print("Access point running. IP address: ");
  Serial.print(WiFi.softAPIP());
  Serial.println("");
*/
    if(udp.listen(8893)) {
        Serial.print("UDP Listening on IP: ");
        Serial.println(WiFi.localIP());
        udp.onPacket(UDPCallBack);
    }

      pinMode(14, INPUT_PULLUP);
      
  pinMode(2, OUTPUT);
  pinMode(PINDIR, OUTPUT);
  //To have 12v on the inside of the connector
  digitalWrite(PINDIR, HIGH);
  pinMode(PINPWM, OUTPUT);

}

unsigned long LoopTimer = 0;

void loop()
{
  if ((millis()%100)==0)
  {
    Serial.print("\nTime Fire:");
    Serial.println(timeFire);
    Serial.print("Loop Time:");
    Serial.println(LoopTimer);
    Serial.print("millis:");
    Serial.println(millis());
  }
  if ((timeFire != 0) and (LoopTimer == 0))
  {
    LoopTimer = millis();
    LoopTimer += timeFire;
    //Turn Digital output HIGH
    digitalWrite(2, HIGH);
    digitalWrite(PINDIR, HIGH);
    digitalWrite(PINPWM, HIGH);
    Serial.println("ON");
  }
  else if ((timeFire != 0) and (LoopTimer < millis()) and (LoopTimer != 0))
  {
    timeFire = 0;
    LoopTimer = 0;
    //Turn Digital output LOW
    digitalWrite(2, LOW);
    digitalWrite(PINDIR, LOW);
    digitalWrite(PINPWM, LOW);    
    Serial.println("OFF");
  }
}

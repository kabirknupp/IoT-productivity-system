// Sound sensor is connected to GPIO 34 (Analog ADC1_CH6) 

#include <WiFi.h>
#include <HTTPClient.h>
// Sound sensor is connected to GPIO 34 (Analog ADC1_CH6) 


const char* ssid = "KABCOMPUTER";
const char* password =  "ILOVEIOT";

//EMAIL BIT
String GOOGLE_SCRIPT_ID = "AKfycbxuhwsiAjHw7VpyEKrmR1YzqPBUNhp_W9JUL7WBk12qaWSuue0KIQ20HXFFRH6W5Urv";
const int sendInterval = 500; 
int importance = 0;

WiFiClientSecure client;
// the number of the LED pin
const int ledPin = 26;  // 16 corresponds to GPIO16
const int ledPin2 = 14; // 17 corresponds to GPIO17
const int ledPin3 = 16;  // 5 corresponds to GPIO5

// setting PWM properties
const int freq = 5000;
const int ledChannel = 0;
const int ledChannel2 = 1;
const int ledChannel3 = 2;
const int resolution = 8;






//Your Domain name with URL path or IP address with path
////https://script.google.com/macros/s/AKfycbzMAVN7ZzKoqPezBWSKHvbpuChRBUnOzKpm2mJ4ggi_3ZNSIEZ2GPN0gN8AEWoo_yD-Ow/exec?id=Sensor_Data&Sensor1=100&Sensor2=100
String serverName = "https://script.google.com/macros/s/AKfycbzMAVN7ZzKoqPezBWSKHvbpuChRBUnOzKpm2mJ4ggi_3ZNSIEZ2GPN0gN8AEWoo_yD-Ow/exec?id=Sensor_Data&Sensor1=";

//0HTTP Response code: 302

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastTime = 0;
//unsigned long timerDelay = 60000;


unsigned long timerDelay = 2000;




const int numReadings = 2000;     //number of averages to be taken
int readings[numReadings];      // the readings from the analog input
int readIndex = 0;              // the index of the current reading
int total = 0;                  // the running total
int average = 0;                // the average

const int sensorPin = 34;

// variable for storing the potentiometer value
int sensorValue = 0;
int absoluteSound = 0;


long initialValue = 0;
const int NValues = 20;
long values[NValues] = {0};
long transitionValue = 0;



const int numFluctuations = 1000;     //number of averages to be taken
int fluctuations[numFluctuations];      // the readings from the analog input
int readFluctuationIndex = 0;              // the index of the current reading
int totalFluctuations = 0;                  // the running total
int averageFluctuations = 0;                // the average


int thresholdOne = 40;
int thresholdTwo = 65;
int thresholdThree = 105;

int counter = 0;

const int numLoops = 5000;





void shiftValueIndex(int c) {                           
  for (int i = NValues - 1; i > 0; i--) {          
    values[i] = values[i - 1];      //shifts position value of the specific time in the array to the previous one
  }
  values[0] = c;               //first time value obtained becomes function input c
}





int smoothToRemoveNoise(){
      total = total - readings[readIndex];
      sensorValue = analogRead(sensorPin);
      sensorValue = map(sensorValue, 1800, 4000, 0, 100);
      absoluteSound = abs(sensorValue);
      //Serial.println(absoluteSound);

      readings[readIndex] = absoluteSound; //read the Sound sensor value
      // add the reading to the total:
  total = total + readings[readIndex];
  // advance to the next position in the array:
  readIndex = readIndex + 1;
  delay(0.1);

  // if we're at the end of the array...
  if (readIndex >= numReadings) {
    // ...wrap around to the beginning:
    readIndex = 0;
  }

  // calculate the average:
  average = total;
  // send it to the computer as ASCII digit
  return average;
  }





int getDifference(){
  transitionValue = values[0]-values[1];   
  initialValue = smoothToRemoveNoise();
  shiftValueIndex(smoothToRemoveNoise());
  return abs(transitionValue);
 }




int getcounter(){
counter = 0;
for (int thisLoop = 0; thisLoop < numLoops; thisLoop++) {
if (getDifference() > thresholdThree) 
{
      counter = counter + 16;
}
else if (getDifference() > thresholdTwo) 
{
      counter = counter + 4;
}
else if (getDifference() > thresholdOne) 
{
      counter = counter + 2;
}
else {
  counter = counter;
}
delay(1);
}
return counter;
}



void setup() {
  Serial.begin(115200); 

//LED
  // configure LED PWM functionalitites
  ledcSetup(ledChannel, freq, resolution);
  ledcSetup(ledChannel2, freq, resolution);
  ledcSetup(ledChannel3, freq, resolution);

  // attach the channel to the GPIO to be controlled
  ledcAttachPin(ledPin, ledChannel);
  ledcAttachPin(ledPin2, ledChannel2);
  ledcAttachPin(ledPin3, ledChannel3);
  
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");

}



  
void loop() {
  if ((millis() - lastTime) > timerDelay) {
    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      HTTPClient http;
      String serverPath = serverName + (getcounter()/5);
      //Serial.println(serverPath);
      // Your Domain name with URL path or IP address with path

       if ((getcounter()/5)>100) {
          for(int dutyCycle = 0; dutyCycle <= 50; dutyCycle++){   
    // changing the LED brightness with PWM
    ledcWrite(ledChannel, dutyCycle);
     ledcWrite(ledChannel2, dutyCycle); 
    delay(15);
  }

      }
      else {
    ledcWrite(ledChannel, 0);  
     ledcWrite(ledChannel2, 0);
         ledcWrite(ledChannel3, 0);        
         delay(500); // wait for half a second or 500
      }


      
      http.begin(serverPath.c_str());
      
      // Send HTTP GET request
      int httpResponseCode = http.GET();



      Serial.println(spreadsheet_comm());
      delay(sendInterval);
        if (spreadsheet_comm()>5) {
          for(int dutyCycle = 0; dutyCycle <= 255; dutyCycle++){   
    // changing the LED brightness with PWM
    ledcWrite(ledChannel, dutyCycle);
     ledcWrite(ledChannel2, dutyCycle);
         ledcWrite(ledChannel3, dutyCycle);   
    delay(1);
  }
      }
      else {
      
    ledcWrite(ledChannel, 0);  
     ledcWrite(ledChannel2, 0);
         ledcWrite(ledChannel3, 0);   
      }



  


      
      if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        Serial.println(payload);
      }
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      // Free resources
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}





int spreadsheet_comm(){
   HTTPClient http;
   String url="https://script.google.com/macros/s/"+GOOGLE_SCRIPT_ID+"/exec?read";
 // Serial.print("Making a request");
  http.begin(url.c_str()); //Specify the URL and certificate
  http.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS);
  int httpCode = http.GET();
  String payload;
    if (httpCode > 0) { //Check for the returning code
        payload = http.getString();
        importance = payload.toInt();
        return importance;
      }
    else {
      Serial.println("Error on HTTP request");
    }
  http.end();
}

//tune the sound code in general
//take the average for longer than 10
//Get average of like 5 consecutive sound values to cancel the noise no delay) (function called cancelnoise)
//do this 5 times, subtract the two values next to each other and then take absolute value of this difference, (gizmo code)
//add each of these differences to a value
//this will get the fluctuations of noise
//note how before I considered doing this as number of times above threshold but this would give a much richer result
//in the main code I can run this straight after the get average

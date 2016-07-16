#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPUpdateServer.h>
#include <TinyGPS++.h>

const char* host = "IP";
const int httpPort = 3000;
String url = "/api/save/";

const char* gpsSN = "1234"; // GPS S/N

int found = 0;

ESP8266WebServer httpServer(80);
ESP8266HTTPUpdateServer httpUpdater;

TinyGPSPlus gps;

long interval = 50000; // in ms 
// Generally, you should use "unsigned long" for variables that hold time
// The value will quickly become too large for an int to store
unsigned long previousMillis = 0; // will store last time was updated

void gpsWeb(){
  String message = "GPS ........\n\n";
  message += "Location: ";
  if(gps.location.isValid()){
    message += String(gps.location.lat(), 6);
    message += ",";
    message += String(gps.location.lng(), 6);
  }else{
    message += "INVALID";
  }
  message += "\nTime: ";
  if (gps.time.isValid())
  {
    message += gps.time.hour();
    message += ":";
    message += gps.time.minute();
    message += ":";
    message += gps.time.second();
  }else{
    message += "INVALID";
  }
  httpServer.send(200, "text/plain", message);
}

void post(){
  unsigned long currentMillis = millis();
  
  if(gps.location.isValid()){
    if(currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;  
      
      WiFiClient client;
      if (!client.connect(host, httpPort)) {
        Serial.println("connection failed");
        return;
      }
    
      String data = "sn=";
      data += gpsSN;
      data += "&lat=";
      data += String(gps.location.lat(), 6);
      data += "&lon=";
      data += String(gps.location.lng(), 6);
  
      client.print(String("POST ") + url + " HTTP/1.1\r\n" +
                 "Host: "+host+":"+ httpPort +"\r\n" +
                 "Content-Type: application/x-www-form-urlencoded\r\n" +
                 "Content-Length: " + data.length() + "\r\n\r\n" +
                 data);
      while(client.available()){
       // wait to receive data from client
      }
      if (client.connected()) {
        client.stop();
      }
    }
  }
}

void hotspots(int i){
  if(WiFi.SSID(i) == "ssid" && found == 0){
    WiFi.begin("ssid", "password");
    delay(5000);
    found = 1;
  }
  if(WiFi.encryptionType(i) == ENC_TYPE_NONE && found == 0){
    char* result = new char[WiFi.SSID(i).length()+1];
    strcpy(result,WiFi.SSID(i).c_str());
    WiFi.begin(result);
    delay(2000);
    found = 1;
  }
}

void scan_function(){
  // WiFi.scanNetworks will return the number of networks found
  int n = WiFi.scanNetworks();
  if (n == 0){
    //no networks found
  }
  else {
    found = 0;
    for (int i = 0; i < n; ++i)
    {
      if(WiFi.status() != WL_CONNECTED){
        hotspots(i);
      }
      delay(10);
    }
  }
}


void setup(){

  Serial.begin(9600);
  Serial.println();
  Serial.println("Booting Sketch...");
  WiFi.mode(WIFI_AP_STA);
  
  while (WiFi.status() != WL_CONNECTED) {
    scan_function();
    delay(5000);
  }
  
//  WiFi.begin(ssid, password);
//
//  while (WiFi.status() != WL_CONNECTED) {
//    delay(500);
//    Serial.print(".");
//  }

  httpUpdater.setup(&httpServer);

  httpServer.on("/gps", gpsWeb);
  
  httpServer.begin();

  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop(){
  while (WiFi.status() != WL_CONNECTED) {
    scan_function();
    delay(5000);
  }
  
  httpServer.handleClient();

  while (Serial.available() > 0){
    if (gps.encode(Serial.read())){
      httpServer.handleClient();
      post();
    }
  }
}

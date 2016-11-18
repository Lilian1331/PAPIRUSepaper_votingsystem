#include <CapacitiveSensor.h>
#include<SPI.h>
#include<RF24.h>

RF24 radio(9,10);
boolean printStatus=0;
CapacitiveSensor   cs_3_2 = CapacitiveSensor(3,2);
CapacitiveSensor   cs_5_4 = CapacitiveSensor(5,4);
CapacitiveSensor   cs_7_6 = CapacitiveSensor(7,6);
CapacitiveSensor   cs_14_15 = CapacitiveSensor(14,15);      

void setup()                    
{
  //NRF24L01+ configuration
  Serial.begin(9600);
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  radio.enableDynamicPayloads();
  radio.powerUp();
}

void loop()                    
{
    long total[5]={0};
    int result,i,showResult = 0;
	
	total[0] =  cs_14_15.capacitiveSensorRaw(30);
    total[1] =  cs_7_6.capacitiveSensorRaw(30);
    total[2] =  cs_5_4.capacitiveSensorRaw(30);
    total[3] =  cs_3_2.capacitiveSensorRaw(30);
    
    
    for(i=0;i<4;i++)
    {
      if(total[i]>600)
      {
        result=i;
        printStatus=1;
        break;
      }
      else
      {
        printStatus=0;
      }
      //debug
      Serial.print(total[i]);
      Serial.print("    ");
    }
    Serial.println("");
    
        
   if(printStatus==1)
   {
    Serial.println("StartScan.....");
    do
    {
      total[1] = cs_7_6.capacitiveSensorRaw(30);
      total[2] =  cs_5_4.capacitiveSensorRaw(30);
      total[3] =  cs_3_2.capacitiveSensorRaw(30);
      total[0] =  cs_14_15.capacitiveSensorRaw(30);
      Serial.println("Debug Mode    ");
      delay(10);
      Serial.print(i);
      Serial.println(total[i]);
    }while(total[i]>600);
    Serial.println("End");
    Serial.println(result+1);
    printStatus=0;
    radio.write(&result,sizeof(result)); //send out the data to pi
   }
    delay(100);                             // arbitrary delay to limit data to serial port 
}


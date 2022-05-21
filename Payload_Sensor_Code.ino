#include "bsec.h"

// Helper functions declarations
void checkIaqSensorStatus(void);
void errLeds(void);

// Create an object of the class Bsec
Bsec iaqSensor;

String output;

// Entry point for the example
void setup(void)
{
  Serial.begin(115200);
  while (!Serial) delay(10); // wait for console
  Wire.begin();

  iaqSensor.begin(BME680_I2C_ADDR_SECONDARY, Wire);
  //output = "\nBSEC library version " + String(iaqSensor.version.major) + "." + String(iaqSensor.version.minor) + "." + String(iaqSensor.version.major_bugfix) + "." + String(iaqSensor.version.minor_bugfix);
  //Serial.println(output);
  checkIaqSensorStatus();

  bsec_virtual_sensor_t sensorList[10] = {
    BSEC_OUTPUT_RAW_TEMPERATURE,
    BSEC_OUTPUT_RAW_PRESSURE,
    BSEC_OUTPUT_RAW_HUMIDITY,
    BSEC_OUTPUT_RAW_GAS,
    BSEC_OUTPUT_IAQ,
    BSEC_OUTPUT_STATIC_IAQ,
    BSEC_OUTPUT_CO2_EQUIVALENT,
    BSEC_OUTPUT_BREATH_VOC_EQUIVALENT,
    BSEC_OUTPUT_SENSOR_HEAT_COMPENSATED_TEMPERATURE,
    BSEC_OUTPUT_SENSOR_HEAT_COMPENSATED_HUMIDITY,
  };

  iaqSensor.updateSubscription(sensorList, 10, BSEC_SAMPLE_RATE_LP);
  checkIaqSensorStatus();
}

// Function that is looped forever
void loop(void)
{
  unsigned long time_trigger = millis();
  if (iaqSensor.run()) { // If new data is available
    /*
    Default Sensor Output Code
    
    output = "Time [s]: "; 
    output += String(time_trigger/1000);

    output += "    Pressure [hPa]: ";
    output +=  String(iaqSensor.pressure/100);


    output += "    Temperature [°C]: ";
    output +=  String(iaqSensor.temperature);

    output += "     Relative Humidity [%] ";
    output +=  String(iaqSensor.humidity);

    output += "     CO2 Equivalent[PPM] ";
    output +=  String(iaqSensor.co2Equivalent);

    output += "     Static IAQ ";
    output +=  String(iaqSensor.staticIaq);
    Serial.println(output);
    */

    //Custom Sensor Output Code

    /*
    output += String(time_trigger/1000);

    output += "\\n";
    */
    output = "";//"Temperature [°C]: ";
    output +=  String(iaqSensor.temperature);
    Serial.println(output);

    //output += "|Humidity [%]: ";
    output = "";
    output +=  String(iaqSensor.humidity);
    Serial.println(output);

    //output += "|Pressure [hPa]: ";
    output = "";
    output +=  String(iaqSensor.pressure/100);
    Serial.println(output);

    //output += "|CO2 [PPM]: ";
    output = "";
    output +=  String(iaqSensor.co2Equivalent);
    
    //output +=  String(iaqSensor.staticIaq);
    Serial.println(output);
    
    
  } else {
    checkIaqSensorStatus();
  }
}

// Helper function definitions
void checkIaqSensorStatus(void)
{
  if (iaqSensor.status != BSEC_OK) {
    if (iaqSensor.status < BSEC_OK) {
      output = "BSEC error code : " + String(iaqSensor.status);
      Serial.println(output);
      for (;;)
        errLeds(); /* Halt in case of failure */
    } else {
      output = "BSEC warning code : " + String(iaqSensor.status);
      Serial.println(output);
    }
  }

  if (iaqSensor.bme680Status != BME680_OK) {
    if (iaqSensor.bme680Status < BME680_OK) {
      output = "BME680 error code : " + String(iaqSensor.bme680Status);
      Serial.println(output);
      for (;;)
        errLeds(); /* Halt in case of failure */
    } else {
      output = "BME680 warning code : " + String(iaqSensor.bme680Status);
      Serial.println(output);
    }
  }
}

void errLeds(void)
{
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(100);
  digitalWrite(LED_BUILTIN, LOW);
  delay(100);
}

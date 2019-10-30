import random
import time

from sense_hat import SenseHat
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=pihub-test.azure-devices.net;DeviceId=rasp-pi;SharedAccessKey=EnhKuGyDpqu25+JCw8bG+BqNkMFonkAHGTgg4QWvFIU="

# Define the JSON message to send to IoT Hub.

sense = SenseHat()

MSG_TXT = '{{"temperature": {temperature},"humidity": {humidity}}}'

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # Emulate a sense hat
            temperature = sense.get_temperature()
            humidity = sense.get_humidity()
            msg_txt_formatted = MSG_TXT.format(temperature=temperature, humidity=humidity)
            message = Message(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            if temperature > 30:
              message.custom_properties["temperatureAlert"] = "true"
            else:
              message.custom_properties["temperatureAlert"] = "false"

            # Send the message.
            print( "Sending message: {}".format(message) )
            sense.show_message(temperature)
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(1)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()
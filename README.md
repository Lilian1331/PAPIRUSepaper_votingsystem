# PAPIRUSepaper_votingsystem
Blog for e-paper voting system:https://www.rs-online.com/designspark/e-paper-voting-system<br>
Refer to the papirus set-up:https://www.rs-online.com/designspark/papirus-an-epaper-display-for-the-raspberry-pi

<p><b>This e-paper voting system is composed by three main module:</b><br>
(1) Arduino UNO with atmega328p<br>
(2) Raspberry Pi 1<br>
(3) Raspberry Pi 2 with e-paper<br></p>

<p><b>(1)Program run on Arduino UNO:</b><br>
<l>NRF/4pins_CapacitiveSensor_Send_Arduino_keep_/4pins_CapacitiveSensor_Send_Arduino_keep_.ino</l><br>
<b>(2)Program run on Raspberry Pi 1:</b><br>
<l>NRF/NRF_receive.py</l><br>
<b>(3)Program run on Raspberry Pi 2 with E-paper:</b><br>
<l>papirus.py</l>
</p>
Flow of the voting system:
Arduino detect the capacitance change->Send to Raspberry Pi 1 via NRF24L01+ module->Raspberry Pi 1 send data to Raspberry Pi 2 via internet->Raspberry Pi 2 receive and display the result.

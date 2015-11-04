# dryer
A quick-and-dirty project that sends e-mails when the dryer's buzzer goes off.
`
This script uses GPIO pin 18 on a Raspberry Pi connected to a relay's normally open contacts, and whose coil is wired in parallel with the buzzer on a dryer to detect when the buzzer goes off and to send e-mails when it does. The project is designed to be run using supervisor, and the file dryerMonitor.conf is the config file for supervisor. It assumes this project is pulled under /opt/dryer.

# PiCar
A robotic PiCar that can be controlled from you phone

===========================

### THIS IS IN EARLY DEVELOPMENT

It is nowhere near feature complete, or even working slightly.

It's currently meant to work on a car that has one irsensor (to warn if something is detected behind the car)
A motor controller that can drive two channels. I wire two motors to the left and two to the right. For voltage
reporting an ADC is needed for the pi.

I use a 7.4v 2ah Li-Ion battery pack. Wired into a bucker adjusted to output 5.1v to the pi usb power input
and a booster configured to send 11v into a motor controller.

- [Step-up Voltage converter](https://www.amazon.com/XL6009E1-Adjustable-Step-up-Voltage-Converter/dp/B07Q2QT83T)
- [Step-down Voltage Bucker](https://www.amazon.com/Valefod-Efficiency-Voltage-Regulator-Converter/dp/B076H3XHXP/ref=sr_1_1_sspa?dchild=1&keywords=lm2596&qid=1595770964&s=electronics&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExVURMTDQ4U09XT01NJmVuY3J5cHRlZElkPUEwMDMzNzE0M0NNVlRZRjAyUFA1SiZlbmNyeXB0ZWRBZElkPUEwODg3OTIwM0hKSVFKMlM5UkYyUiZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=)
- [Motor Driver](https://www.amazon.com/Controller-Stepper-Arduino-Electric-Projects/dp/B07PFC4RRB/ref=sr_1_1_sspa?dchild=1&keywords=motor+driver&qid=1595771023&s=electronics&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzNlFPN0JBTVgxWElBJmVuY3J5cHRlZElkPUEwODEzNzkzM1Q0WkZEUlAwRUtZQiZlbmNyeXB0ZWRBZElkPUEwODk0MDk4MllLVlZUNjFHSjVJUiZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=)


### TODO:
- [ ] Parse angle and percent strenght into usable horizontal and vertical strengths.
- [ ] Implement logic to use these values to drive the car.
- [ ] Add config file parsing ability
- [ ] Add setup.py so that dependencies are pulled in automatically
- [ ] Add battery voltage reporting

# The-UNO-NANO
A python script for sumalting UNO NANOs

To first start add all your components add it between the main loop and Arduino class to add a Arduino do ardio.append(arduino(x, y, loopcode, startupcode, len(ardinos)))
here loop codes is the code that loops every iteration make Shure that it has a while loop as it need that to LOOP
startup code is code for starting up and can not loop

now LEDs for them u can do 
item.append(LED(x, y, len(items))).BindToPin(component, pinname)
here
BindToPin allows the led ot read the pin it is Binded to 
component is the component it wans to Binded to
pinname is the name of the pin in the component

now programing it
it is just python so nothing special other wise but let say u want to turn on pin1
u do
self.pins['Pin1'] = True
this apples to al digital pins but for analog use floats plz

that is it that is how u use my UNO NANO

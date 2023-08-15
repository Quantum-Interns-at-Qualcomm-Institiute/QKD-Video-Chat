import controlP5.*; 
import processing.serial.*;
Serial port;
ControlP5 cp5; //create ControlP5 object
PFont font, font2;
int ratio = 2000;
int stateP1, stateP2, stateP3;

void setup(){
  size(1000,775);
  //port = new Serial(this, "COM3", 9600); //declare port
  cp5 = new ControlP5(this);
  font = createFont("calibri light bold", 20); //custom font
  font2 = createFont("calibri light bold", 45); //custom font
  pixelDensity(1);
  cp5.setAutoDraw(false);
  drawCircle(0.15);
  cp5.draw();
  
  cp5.addButton("state1")            //the -45 button
  .setPosition(75, 475)                          //(x,y) top left corner
  .setSize(100, 100)                             //(width, height)
  .setColorBackground(color(252, 58, 58))
  ////.setFont(font2)
  //.setColorCaptionLabel(color(252, 58, 58))
  .setCaptionLabel("-45")
  .setColorForeground(color(0, 0, 0))

  ;
  cp5.addButton("state2")                             //the 0 button
  .setPosition(200, 475)                          //(x,y) top left corner
  .setSize(100, 100)                             //(width, height)
  .setColorBackground(color(252, 58, 136))
  //.setFont(font2)
  //.setColorCaptionLabel(color(252, 58, 136))
  .setCaptionLabel("0")
  .setColorForeground(color(0, 0, 0))
  ;
  cp5.addButton("state3")                            //the 45 button
  .setPosition(75, 600)                          //(x,y) top left corner
  .setSize(100, 100)                             //(width, height)
  .setColorBackground(color(252, 97, 58))
  //.setFont(font2)
  //.setColorCaptionLabel(color(252, 97, 58))
  .setCaptionLabel("45")
  .setColorForeground(color(0, 0, 0))
  ;
  cp5.addButton("state4")                             //the 90 button
  .setPosition(200, 600)                          //(x,y) top left corner
  .setSize(100, 100)                             //(width, height)
  .setColorBackground(color(252, 136, 58))
  //.setFont(font2)
  //.setColorCaptionLabel(color(252, 136, 58))
  .setCaptionLabel("90")
  .setColorForeground(color(0, 0, 0))
  ;
  cp5.addButton("state1p2")            //the -45 button polarizer 2
  .setPosition(375, 475)                          //(x,y) top left corner
  .setSize(100, 100)                             //(width, height)
  .setColorBackground(color(155, 58, 252))
  //.setFont(font2)
  .setCaptionLabel("-45")
  .setColorForeground(color(0, 0, 0))
  ;
  cp5.addButton("state2p2")                             //the 0 button polarizer 2
  .setPosition(500, 475)                          //(x,y) top left corner
  .setSize(100, 100)                             //(width, height)
  .setColorBackground(color(77, 58, 252))
  //.setFont(font2)
  .setCaptionLabel("0")
  .setColorForeground(color(0, 0, 0))
  ;
  cp5.addButton("state3p2")                            //the 45 button polarizer 2
  .setPosition(375, 600)                          //(x,y) top left corner
  .setSize(100, 100)                             //(width, height)
  .setColorBackground(color(116, 58, 252))
  //.setFont(font2)
  .setCaptionLabel("45")
  .setColorForeground(color(0, 0, 0))
  ;
  cp5.addButton("state4p2")                             //the 90 button polarizer 2
  .setPosition(500, 600)                          //(x,y) top left corner
  .setSize(100, 100)                             //(width, height)
  .setColorBackground(color(155, 58, 252))
  //.setFont(font2)
  .setCaptionLabel("90")
  .setColorForeground(color(0, 0, 0))
  ;
    cp5.addButton("state1p3")            //the -45 button polarizer 3
  .setPosition(675, 475)                          //(x,y) top left corner
  .setSize(100, 100)                             //(width, height)
  .setColorBackground(color(58, 252, 252))
  //.setFont(font2)
  .setCaptionLabel("-45")
  .setColorForeground(color(0, 0, 0))
  ;
  cp5.addButton("state2p3")                             //the 0 button polarizer 3
  .setPosition(800, 475)                          //(x,y) top left corner
  .setSize(100, 100)                             //(width, height)
  .setColorBackground(color(58, 252, 174))
  //.setFont(font2)
  .setCaptionLabel("0")
  .setColorForeground(color(0, 0, 0))
  ;
  cp5.addButton("state3p3")                            //the 45 button polarizer 3
  .setPosition(675, 600)                          //(x,y) top left corner
  .setSize(100, 100)                             //(width, height)
  .setColorBackground(color(58, 213, 252))
  //.setFont(font2)
  .setCaptionLabel("45")
  .setColorForeground(color(0, 0, 0))
  ;
  cp5.addButton("state4p3")                             //the 90 button polarizer 3
  .setPosition(800, 600)                          //(x,y) top left corner
  .setSize(100, 100)                    //(width, height)
  .setColorBackground(color(58, 174, 252))
  //.setFont(font2)
  .setCaptionLabel("90")
  .setColorForeground(color(0, 0, 0))
  ;
}

double d(double x, double y) {
  return Math.sqrt(x*x + y*y);
}

double wavelength = 520e-9;
double laser(double x) {
  return Math.sin(2 * Math.PI * x / wavelength);
}

// distance from light source to target in meters
double d1 = 1.000, d2 = 1.001;
// dampening constant, how quickly should the light dim as it gets further away from the center
int damp = 10;
// optics scuffed
//double luminosity(double x) {
//  double l1 = laser(d(x, d1)) / 2;
//  double l2 = laser(d(x, d2)) / 2;
  
//  double p1 = Math.toRadians(stateP1);
//  double p2 = Math.toRadians(stateP2);
//  double p3 = Math.toRadians(stateP3);
  
  
//  double h_comp = Math.cos(p3) * (Math.cos(p1) * l1 + Math.cos(p2) * l2);
//  double v_comp = Math.sin(p3) * (Math.sin(p1) * l1 + Math.sin(p2) * l2);
  
//  //return Math.exp(-damp * x) * l2(x);
//  return Math.exp(-damp * x) * d(h_comp, v_comp);
//}

// quantum version (amplitude calculations)
double luminosity(double x) {
  double p1 = Math.toRadians(stateP1);
  double p2 = Math.toRadians(stateP2);
  double p3 = Math.toRadians(stateP3);
  
  double pa = 2 * Math.PI * d(x, d1) / wavelength;
  double pb = 2 * Math.PI * d(x, d2) / wavelength;
  
  // |0>
  //double r0 = 1/sqrt(2) * (Math.cos(pa) * Math.cos(p1 - Math.toRadians(45)) * Math.cos(p1) + Math.cos(pb) * Math.cos(p2 - Math.toRadians(45)) * Math.cos(p2));
  //double i0 = 1/sqrt(2) * (Math.sin(pa) * Math.cos(p1 - Math.toRadians(45)) * Math.cos(p1) + Math.sin(pb) * Math.cos(p2 - Math.toRadians(45)) * Math.cos(p2));
  
  // |1>
  //double r1 = 1/sqrt(2) * (Math.cos(pa) * Math.cos(p1 - Math.toRadians(45)) * Math.sin(p1) + Math.cos(pb) * Math.cos(p2 - Math.toRadians(45)) * Math.sin(p2));
  //double i1 = 1/sqrt(2) * (Math.sin(pa) * Math.cos(p1 - Math.toRadians(45)) * Math.sin(p1) + Math.sin(pb) * Math.cos(p2 - Math.toRadians(45)) * Math.sin(p2));
  
  // without C
  // Math.sqrt(r0*r0 + i0*i0 + r1*r1 + i1*i1)
  
  double rc = Math.cos(pa) * Math.cos(p3-p1) * Math.cos(p1 - Math.toRadians(45)) + Math.cos(pb) * Math.cos(p3-p2) * Math.cos(p2 - Math.toRadians(45));
  double ic = Math.sin(pa) * Math.cos(p3-p1) * Math.cos(p1 - Math.toRadians(45)) + Math.sin(pb) * Math.cos(p3-p2) * Math.cos(p2 - Math.toRadians(45));
  
  return Math.exp(-damp * x) * Math.sqrt(rc * rc + ic * ic) / 2;
}

// Difference in radius in meters before next evaluation of luminosity
//double precision = 1.007e-3;
void drawCircle(int centerX, int centerY, float R) {
   //this is less compute-heavy but it's weird for some reason
   loadPixels();
   for (int x = (int)(centerX-R*ratio/2); x < centerX+R*ratio/2; x++) {
     for (int y = (int)(centerY-R*ratio/2); y < centerY+R*ratio/2; y++) {
       double r = dist(centerX, centerY, x, y) / ratio;
       int index = x + y * width;
       pixels[index] = color(0, (int)(Math.pow(luminosity(r), 2) * 255), 0);
     }
   }
   updatePixels();
  
  //colorMode(RGB, 255, 255, 255);
  //noStroke();
  //for (float r = R; r >= 0; r -= precision) {
  //  stroke(0, (float)(luminosity(r) * 255), 0);
  //  ellipse(centerX, centerY, r*ratio, r*ratio);
  //  //System.out.println(r + " " + luminosity(r));
  //}
  //System.exit(0);
}

void drawCircle(float R) {
  drawCircle(490, 250, R);
}

void draw() {
  background(0, 0, 0);                        //background color
  //fill(255, 255, 255);
  textFont(font);
  fill(255, 255, 255);
  text("QUANTUM ERASER DEMO",365, 50);
  // circle
  stroke(0, 255, 0);
  //drawCircle(0.15); //3rd value = radius = 0.15 x 2000
  noFill();
  text("Polarizer 1 position: " + stateP1, 75, 450);
  text("Polarizer 2 position: " + stateP2, 375, 450);
  text("Polarizer 3 position: " + stateP3, 675, 450);
  cp5.draw();
  drawCircle(0.15);
}

  
void state1(){
  stateP1 = -45;
  //port.write(1);
  cp5.draw();
}
void state2(){
  stateP1 = 0;
  //port.write(2);
}
void state3(){
  stateP1 = 45;
  //port.write(3);
}
void state4(){
  stateP1 = 90;
  //port.write(4);
}
void state1p2(){
  stateP2 = -45;
}
void state2p2(){
  stateP2 = 0;
}
void state3p2(){
  stateP2 = 45;
}
void state4p2(){
  stateP2 = 90;
}
void state1p3(){
  stateP3 = -45;
}
void state2p3(){
  stateP3 = 0;
}
void state3p3(){
  stateP3 = 45;
}
void state4p3(){
  stateP3 = 90;
}
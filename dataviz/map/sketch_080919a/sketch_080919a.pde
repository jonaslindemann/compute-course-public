Record[] records;  // Declares an object (records) from the class Record
String[] plines;   // Declares a String array to read lines of a shape file
String[] clines;   // Declares a String array to read lines of a CSV data file
String[] cnames;   // Declares a String array of names of each columns in a CSV data file 
int cnum = 0;      // Declares a variable for a number of cities
int xnum = 0;      // Declares a variable of x-axis for scatterplot
int ynum = 1;      // Declares a variable of y-axis for scatterplot

void setup() {
  size(600, 700);  // Sets a size of the display window to (width=600, height=700)
  noLoop();        // Stops Processing from continuously executing the code within draw() 

  // Reads the contents of a file and creates a String array of its individual lines
  plines = loadStrings("datahaven_all.trimmed.pixels.dat"); 
  clines = loadStrings("Connecticut.csv");

  PFont fontA = loadFont("ScalaSans-Caps-32.vlw"); // Loads a font into a variable of type PFont
  textFont(fontA, 14);  // Sets the font and its size in units of pixels

  int pnum = 0;  // starting index of each cities
  int vnum = 0;  // a number of vertices for each cities
  String str1 = "VERTICES";  

  cnames = split(clines[0], ',');

  for (int i = 0; i < plines.length; i++) {
    String[] types = split(plines[i], ' ');  // Reads each lines in shape file loaded
    if (str1.equals(types[0]) == true)       // Counts a number of cities
      cnum = cnum + 1;    
  } 
  records = new Record[cnum];     // Constructs one object (records) from the class Record
  for (int i = 0; i < cnum; i++) {
    int inum = pnum + 4; // Sets a starting index of vertices for each regions
    for (int j = pnum; j < inum; j++) {  // Counts a number of vertices of each regions
      String[] types = split(plines[j], ' ');
      if (str1.equals(types[0]) == true)  // Sets a variable (vnum) to a number of vertices of a region
        vnum = int(types[1]);
    }
    int[] xx = new int[vnum];  // Declares and construct an array of x axis for vertices
    int[] yy = new int[vnum];  // Declares and construct an array of y axis for vertices
    for (int j = inum; j < inum + vnum; j++) {  // Sets two arrays for pixels of vertices of a region
      String[] types = split(plines[j], ' ');  
      xx[j-inum] = int(types[0]) - 30;    // move 30 pixels to the left
      yy[j-inum] = int(types[1]) + 300;   // move 300 pixels to the bottom
    }
    records[i] = new Record(vnum, xx, yy, clines[i+1]); // Records all information to an object (records)
    pnum = inum + vnum; // Sets an index of vertices for the next region
  }  
}

void draw() {
  background(0);  // Sets the color used for the background to black
  fill(255);      // Sets the color used to fill text      
  
  // Displays the information specified in the stringdata parameters
  for (int i = 0; i < cnames.length; i++) {
    text("[" + i + "] " + cnames[i], 380, ((i * 20) + 80));
  }
  text("* Click the Left Mouse to change a variable on the x-axis", 40, 20);
  text("* Click the Right Mouse to change a variable on the y-axis", 40, 40);
  text("X : [" + xnum + "] " + cnames[xnum], 40, 340);
  text("Y : [" + ynum + "] " + cnames[ynum], 40, 360);
  text("[ Connecticut Map ]", 250, 640);
  int num = (mouseButton == LEFT) ? xnum : ynum;
  text(": colored by " + cnames[num], 150, 660);

  // Draws a scatterplot
  rect (30, 70, 320, 250); 

  float[] nvx = new float[cnum];   // Declares a list of normalized values on the x-axis
  float[] nvy = new float[cnum];   // Declares a list of normalized values on the y-axis
  float[] xaxis = new float[cnum]; // Declares a list of all data in the stringdata for the x-axis
  float[] yaxis = new float[cnum]; // Declares a list of all data in the stringdata for the y-axis 
  float clr = 0;  // Declares a variable for color

  // Reads and stores data in CSV data file
  for (int i = 0; i < cnum; i++) {
    String[] ccdata = split(records[i].csvdata, ','); // Reads each lines in CSV data file
    xaxis[i] = (xnum != 0) ? abs(float(ccdata[xnum])) : i + 1;  // Stores a value of each data to the list for the x-axis
    yaxis[i] = (ynum != 0) ? abs(float(ccdata[ynum])) : i + 1;  // Stores a value of each data to the list for the y-axis 
    if (xaxis[i] == 0) xaxis[i] = 0.0001;  // Avoids a value of the x-axis being zero
    if (yaxis[i] == 0) yaxis[i] = 0.0001;  // Avoids a value of the y-axis being zero
  }

  for (int i = 0; i < cnum; i++) {
    // Normalizes a number from the data range into a value between 0 to 1
    nvx[i] = (xnum == 0 || xnum == 7) ? norm1(xaxis[i], xaxis) : norm2(xaxis[i], xaxis);
    nvy[i] = (ynum == 0 || ynum == 7) ? norm1(yaxis[i], yaxis) : norm2(yaxis[i], yaxis);
    
    clr = (mouseButton == LEFT) ? nvx[i] : nvy[i];
    // Draws a point(rectangle) for two values in scatterplot
    int x = int(nvx[i] * 300) + 35;
    int y = int((1 - nvy[i]) * 230) + 75;
    fill(int(clr * 255), 60, 0);
    rect(x, y, 10, 10);

    // Draws a shape for each regions with a color for a normalized value in map
    beginShape();
    for (int j = 0; j < records[i].vnum; j++) {
      fill(int(clr * 255), 60, 0); 
      vertex(records[i].xs[j], records[i].ys[j]);
    }
    endShape(CLOSE);
  }
}

// Normalization (linear)
float norm1(float value, float[] lists) {  
  return (value - min(lists)) / (max(lists) - min(lists)); 
}

// Normalization (logarithmic)
float norm2(float value, float[] lists) {
  return (log(value) - log(min(lists))) / (log(max(lists)) - log(min(lists))); 
}

// Clicks the Mouse to change a variable on the x-axis or the y-axis
void mousePressed() {
  if (mouseButton == LEFT) { xnum = ( xnum < 12 ) ? xnum + 1 : 0; } 
  else { ynum = ( ynum < 12 ) ? ynum + 1 : 0; }   
  redraw();  // Executes the code within draw() one time by pressing the Mouse
}

class Record {
  int vnum;  // number of vertices
  int[] xs;  // array of x positions for a region
  int[] ys;  // array of y positions for a region
  String csvdata;  // information of a region in a csv file
  public Record(int num, int[] xlist, int[] ylist, String csvline) {
    vnum = num; 
    xs = xlist;
    ys = ylist;
    csvdata = csvline;
  }
}


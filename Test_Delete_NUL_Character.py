
String="0\00,2,14.99,24.00,2.40,1654986736,1654987080"
print(String)
String = String.replace('\0', '')
print(String)
floats = [float(x) for x in String.split(",")]
print(floats[0])
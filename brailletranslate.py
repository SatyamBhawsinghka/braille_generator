import numpy as np
import braille_lib.alphaToBraille2 as alphaToBraille

string = "ssups"
a = alphaToBraille.translate(string)
print(a)
n_a = np.array(a[0][1:])
print(n_a.shape)
print(a[2])
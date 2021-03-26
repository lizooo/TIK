import math
import copy
from matplotlib import pyplot as plt

# Pre-defined values
T = 0.0166
A = 0.5
delta_Fk = 700

# Calculated values
ti = 0.0083
F1 = 60.24
w1 = 378.505


def S_from_t(t: float) -> float:
    '''
    Basic approximation of a periodic function representing a digital signal
    '''
    time = copy.deepcopy(t)
    time = time - time // T * T
    if time < ti/2:
        return A * time / (ti / 2)
    elif time < ti:
        return A * (1 - (time - ti / 2) / (ti / 2))
    else:
        return 0


def calculate_harmonics_via_integrating(bottom_limit: float, top_limit: float, math_expression: float, k_harmonics_no: int):
    '''
    Calculating of the harmonics by following a formula given in the description and via implementing a classic
    integrating method of rectangles
    '''
    pace_unit = 0.0001
    current_position = bottom_limit
    resulting_value = 0
    while current_position < top_limit:
        resulting_value += pace_unit * math_expression(current_position, k_harmonics_no)
        current_position += pace_unit
    return resulting_value


def ak_intergating_val_cos(t: float, k_harmonics_no: int) -> float:
    '''
    A function that is used to integrate a cosine signal function
    '''
    return S_from_t(t) * math.cos(t * k_harmonics_no * w1)


def bk_integrating_val_sin(t: float, k_harmonics_no: int) -> float:
    '''
    A function that is used to integrate a sine signal function
    '''
    return S_from_t(t) * math.sin(t * k_harmonics_no * w1)


def signal_to_the_second_power(t: float, k_harmonics_no=0) -> float:
    '''
    A squared function
    '''
    return S_from_t(t) * S_from_t(t)


def trigonometrical_coeffs(k_harmonics_no: int, param: str) -> float:
    if param == 'sin':
        return 2 / T * calculate_harmonics_via_integrating(0, T, bk_integrating_val_sin, k_harmonics_no)
    elif param == 'cos':
        return 2 / T * calculate_harmonics_via_integrating(0, T, ak_intergating_val_cos, k_harmonics_no)


a0 = 2 / T * calculate_harmonics_via_integrating(0, T, ak_intergating_val_cos, k_harmonics_no=0)
A0 = a0/2

'''
for table

'''
ak, bk, phsii, harmonics = ([] for _ in range(4))

ak = [trigonometrical_coeffs(k, 'cos') for k in range(1, 21)]
bk = [trigonometrical_coeffs(k, 'sin') for k in range(1, 21)]
harmonics = [("%.3f" % math.sqrt(bk[n] ** 2 + ak[n] ** 2)) for n in range(len(bk))]
phsii = ["%.3f" % math.atan(bk[n] / ak[n]) for n in range(len(bk))]

print('\nharmonics: {} \nphsii:     {} \nak:        {} \nbk:        {}'.format(harmonics, phsii, ak, bk))


numb_of_harmonics = math.ceil(delta_Fk / F1)
energetic_powee_spectrum = A0 ** 2 + 0.5 * sum([bk[i] ** 2 + ak[i] ** 2 for i in range(numb_of_harmonics)])
full_average_power = 1 / T * calculate_harmonics_via_integrating(0, T, signal_to_the_second_power, k_harmonics_no=0)
absolute_error = (abs(full_average_power - energetic_powee_spectrum))
relative_error = absolute_error/ full_average_power


print("")
print("Number of harmonics ................................ {}".format(numb_of_harmonics))
print("Power of signal (energetic spectrum).................{}".format(energetic_powee_spectrum))
print("Average power of signal..............................{}".format(full_average_power))
print("Absolute error.......................................{}".format(absolute_error))
print("Relative error.......................................{}".format(relative_error))


'''
plotter
'''
row =[a0]


time_points = [(t * 0.00001 - 0.02) for t in range(4000)]
voltages = [S_from_t(t) for t in time_points]

plt.figure(1)
plt.plot(time_points, voltages)
plt.xlabel('Time, s')
plt.ylabel('Signal, V')
# plt.xlim(xmin=time_points[0])
plt.grid()



plt.figure(2)
plt.plot([harm_n for harm_n in range( 21)],
          row+([math.sqrt(bk[i] ** 2 + ak[i] ** 2) for i in range(20)]))
plt.xlim()
plt.xlabel('No. of Harmonics')
plt.ylabel('Amplitude of Harmonics, В')
# plt.xlim(xmin=1)
plt.grid()

plt.figure(3)
plt.plot([harm_n for harm_n in range(21)],
         row+([bk[i] ** 2 + ak[i] ** 2 for i in range(20)]))
plt.xlabel('No. of Harmonics')
plt.ylabel('Power of signal, watt')
# plt.xlim(xmin=1)
plt.grid()


plt.figure(4)
plt.plot([harm_n for harm_n in range(1, 21)],
         [math.atan(bk[i] / ak[i]) for i in range(20)])
# plt.xlim(xmin=1)
plt.xlabel('Т')
plt.ylabel('Ψk')
plt.grid()


plt.show()


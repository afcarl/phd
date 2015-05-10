a = [('dov_tube40_80_0.s', [ 247,  7518]),
     ('dov_cube45_0.s',    [1523, 49992]),
     ('dov_ball25_0.s',    [  61, 10043]),
     ('dov_ball45_0.s',    [1130, 57508]),
     ('dov_cube25_0.s',    [  96, 10047]),
     ('dov_ball45_4.s',    [  70,  9998])]

for name, hits in a:
    print('{}:  {:.2f}'.format(name, 100.0*hits[0]/hits[1]))

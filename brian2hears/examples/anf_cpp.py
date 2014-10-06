from brian2 import *
from brian2hears import *
set_device('cpp_standalone')

duration = 10.*second
dt = defaultclock.dt
N = int(duration/dt)

sound = TimedArray(np.random.randn(N), dt = defaultclock.dt)

cf = np.array(erbspace(20*Hz, 20000.*Hz, 3000))
cochlea = GammatoneFilterbank(sound, cf)

# Leaky integrate-and-fire model with noise and refractoriness
eqs = '''
dv/dt = (I_in-v)/(1*ms)+0.2*xi*(2/(1*ms))**.5 : 1
I_in = 3*clip(I, 0, Inf)**(1./3.) : 1
'''
anf = NeuronGroup(len(cf), eqs, reset='v=0', threshold='v>1')#, refractory=5*ms)
anf.variables.add_reference('I', cochlea, 'out')

M = SpikeMonitor(anf)

run(duration)
device.build(project_dir = './anf_cpp/', compile_project = True)

#i, t = M.it
#plot(np.array(t), i, '.', color = 'k')
#show()
print M.name

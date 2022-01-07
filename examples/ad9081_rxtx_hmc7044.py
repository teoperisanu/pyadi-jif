# Determine AD9081+ZCU102 Configuration For RX and TX contrained together

import adijif
import pprint

vcxo = 100e6

sys = adijif.system("ad9081", "hmc7044", "xilinx", vcxo, solver="CPLEX")
sys.fpga.setup_by_dev_kit_name("zcu102")
sys.fpga.sys_clk_select = "GTH34_SYSCLK_QPLL0"  # Use faster QPLL
sys.Debug_Solver = True
sys.converter.clocking_option = "integrated_pll"
sys.fpga.request_fpga_core_clock_ref = True  # force reference to be core clock rate
sys.converter.adc.sample_clock = 2900000000 / (8 * 6)
sys.converter.dac.sample_clock = 5800000000 / (4 * 12)

sys.converter.adc.decimation = 8 * 6
sys.converter.dac.interpolation = 4 * 12

mode_tx = "0"
mode_rx = "1.0"

sys.converter.dac.set_quick_configuration_mode(mode_tx)
sys.converter.adc.set_quick_configuration_mode(mode_rx)

assert sys.converter.adc.M == 8
assert sys.converter.adc.F == 12
assert sys.converter.adc.K == 64
assert sys.converter.adc.Np == 12
assert sys.converter.adc.CS == 0
assert sys.converter.adc.L == 1
assert sys.converter.adc.S == 1

print(sys.converter.adc.bit_clock)
print(sys.converter.dac.bit_clock)

sys.converter.adc._check_clock_relations()
sys.converter.dac._check_clock_relations()

cfg = sys.solve()

pprint.pprint(cfg)

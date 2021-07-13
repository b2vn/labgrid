from importlib import import_module
import attr

from ..factory import target_factory
from .common import Driver


@target_factory.reg_driver
@attr.s(eq=False)
class ModbusRTUDriver(Driver):
    bindings = {"resource": "ModbusRTU"}

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._modbus = import_module('minimalmodbus')
        self.instrument = None

    def on_activate(self):
        self.instrument = self._modbus.Instrument(
            self.resource.port,
            self.resource.address,
            debug=False)
        self.instrument.serial.baudrate = self.resource.speed
        self.instrument.serial.timeout = self.resource.timeout

        self.instrument.mode = self._modbus.MODE_RTU
        self.instrument.clear_buffers_before_each_transaction = True

    def on_deactivate(self):
        self.instrument = None

    # TODO: Is it ok to use kwargs in a driver? Would it be better to add
    # default values for e.g. 'signed'?
    # TODO: Should we implement read_input_register() and read_holding
    # register() or just have and option to provide the functioncode (either 3
    # or 4) to the read_register() function?
    def read_register(self, registeraddress, number_of_decimals=0,
                      functioncode=3, signed=False):
        return self.instrument.read_register(
            registeraddress, number_of_decimals, functioncode, signed)

    # TODO: Add the rest of the functionality
    def write_register(self, registeraddress, value, number_of_decimals=0,
                       functioncode=16, signed=False):
        return self.instrument.write_register(
            registeraddress, value, number_of_decimals, functioncode, signed)

    def read_registers(self, registeraddress, number_of_registers,
                       functioncode=3):
        return self.instrument.read_registers(
            registeraddress, number_of_registers, functioncode)

    def write_registers(self, registeraddress, values):
        return self.instrument.write_registers(registeraddress, values)

    def read_bit(self, registeraddress, functioncode=2):
        return self.instrument.read_bit(registeraddress, functioncode)

    def write_bit(self, registeraddress, value, functioncode=5):
        return self.instrument.write_bit(registeraddress, value, functioncode)

    def read_string(self, registeraddress, number_of_registers=16,
                    functioncode=3):
        return self.instrument.read_string(
            registeraddress, number_of_registers, functioncode)

    def write_string(self, registeraddress, textstring,
                     number_of_registers=16):
        return self.instrument.write_string(
            registeraddress, textstring, number_of_registers)

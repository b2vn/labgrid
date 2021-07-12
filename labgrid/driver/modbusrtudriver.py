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

    def read_register(self, addr, decimals, **kwargs):
        return self.instrument.read_register(addr, decimals, **kwargs)

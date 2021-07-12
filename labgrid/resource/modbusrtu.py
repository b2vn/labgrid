import attr

from ..factory import target_factory
from .common import Resource
from .base import SerialPort


@target_factory.reg_resource
@attr.s(eq=False)
class ModbusRTU(SerialPort, Resource):
    """This resource describes Modbus RTU instrument.

    Args:
        port (str): tty the instrument is connected to, e.g. '/dev/ttyUSB0'
        address (int): slave address on the modbus, e.g. 16
        baudrate (bool): optional, default is 115200
        timeout (bool): optional, timeout in seconds. Default is 0.25 s"""
    port = attr.ib(validator=attr.validators.instance_of(str))
    address = attr.ib(validator=attr.validators.instance_of(int))
    speed = attr.ib(default=115200,
                    validator=attr.validators.instance_of(int))
    timeout = attr.ib(default=0.25,
                      validator=attr.validators.instance_of(float))

# -*- encoding: utf-8 -*-
#
# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""
Fake driver interfaces used in testing.

This is also an example of some kinds of things which can be done within
drivers.  For instance, the MultipleVendorInterface class demonstrates how to
load more than one interface and wrap them in some logic to route incoming
vendor_passthru requests appropriately. This can be useful eg. when mixing
functionality between a power interface and a deploy interface, when both rely
on seprate vendor_passthru methods.
"""

from ironic.common import boot_devices
from ironic.common import exception
from ironic.common.i18n import _
from ironic.common import states
from ironic.drivers import base


class FakePower(base.PowerInterface):
    """Example implementation of a simple power interface."""

    def get_properties(self):
        return {}

    def validate(self, task):
        pass

    def get_power_state(self, task):
        return task.node.power_state

    def set_power_state(self, task, power_state):
        if power_state not in [states.POWER_ON, states.POWER_OFF]:
            raise exception.InvalidParameterValue(_("set_power_state called "
                    "with an invalid power state: %s.") % power_state)
        task.node.power_state = power_state

    def reboot(self, task):
        pass


class FakeDeploy(base.DeployInterface):
    """Class for a fake deployment driver.

    Example imlementation of a deploy interface that uses a
    separate power interface.
    """

    def get_properties(self):
        return {}

    def validate(self, task):
        pass

    def deploy(self, task):
        return states.DEPLOYDONE

    def tear_down(self, task):
        return states.DELETED

    def prepare(self, task):
        pass

    def clean_up(self, task):
        pass

    def take_over(self, task):
        pass


class FakeVendorA(base.VendorInterface):
    """Example implementation of a vendor passthru interface."""

    def get_properties(self):
        return {'A1': 'A1 description. Required.',
                'A2': 'A2 description. Optional.'}

    def validate(self, task, method, **kwargs):
        if method == 'first_method':
            bar = kwargs.get('bar')
            if not bar:
                raise exception.MissingParameterValue(_(
                    "Parameter 'bar' not passed to method 'first_method'."))

    @base.passthru(['POST'],
                   description=_("Test if the value of bar is baz"))
    def first_method(self, task, http_method, bar):
        return True if bar == 'baz' else False


class FakeVendorB(base.VendorInterface):
    """Example implementation of a secondary vendor passthru."""

    def get_properties(self):
        return {'B1': 'B1 description. Required.',
                'B2': 'B2 description. Required.'}

    def validate(self, task, method, **kwargs):
        if method in ('second_method', 'third_method_sync'):
            bar = kwargs.get('bar')
            if not bar:
                raise exception.MissingParameterValue(_(
                    "Parameter 'bar' not passed to method '%s'.") % method)

    @base.passthru(['POST'],
                   description=_("Test if the value of bar is kazoo"))
    def second_method(self, task, http_method, bar):
        return True if bar == 'kazoo' else False

    @base.passthru(['POST'], async=False,
                   description=_("Test if the value of bar is meow"))
    def third_method_sync(self, task, http_method, bar):
        return True if bar == 'meow' else False


class FakeConsole(base.ConsoleInterface):
    """Example implementation of a simple console interface."""

    def get_properties(self):
        return {}

    def validate(self, task):
        pass

    def start_console(self, task):
        pass

    def stop_console(self, task):
        pass

    def get_console(self, task):
        return {}


class FakeManagement(base.ManagementInterface):
    """Example implementation of a simple management interface."""

    def get_properties(self):
        return {}

    def validate(self, task):
        pass

    def get_supported_boot_devices(self):
        return [boot_devices.PXE]

    def set_boot_device(self, task, device, persistent=False):
        if device not in self.get_supported_boot_devices():
            raise exception.InvalidParameterValue(_(
                "Invalid boot device %s specified.") % device)

    def get_boot_device(self, task):
        return {'boot_device': boot_devices.PXE, 'persistent': False}

    def get_sensors_data(self, task):
        return {}

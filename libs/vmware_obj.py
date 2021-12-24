# !/usr/bin/env python
# -*- coding: utf-8 -*-

r""" pyVmomi API functions
https://www.vmware.com/support/developer/vc-sdk/visdk41pubs/ApiReference/index-properties.html
"""

from pyVim.connect import SmartConnect, Disconnect
from pyVim.task import WaitForTask
from concurrent.futures import ThreadPoolExecutor, as_completed
import ssl
from pyVmomi import vim
from libs.log_obj import LogObj
import traceback
from utils import util
from utils.decorator import retry, lock, print_for_call

logger = LogObj().get_logger()


class VMwareObj(object):
    _content = None
    _session = None

    def __init__(self, vc_ip, vc_user, vc_pwd, vc_port):
        super(VMwareObj, self).__init__()
        self.vc_ip = vc_ip
        self.vc_user = vc_user
        self.vc_pwd = vc_pwd
        self.vc_port = vc_port

    def __del__(self):
        try:
            Disconnect(self._session)
            del self._session
        except Exception:
            pass

    @property
    @retry(tries=120, delay=5)
    @lock
    def session(self):
        if self._session is None:
            logger.info('Init vcenter session for {vc_ip}'.format(vc_ip=self.vc_ip))
            if hasattr(ssl, '_create_unverified_context'):
                _context = ssl._create_unverified_context()
            try:
                self._session = SmartConnect(host=self.vc_ip, user=self.vc_user, pwd=self.vc_pwd, port=self.vc_port,
                                             sslContext=_context)
            except Exception as e:
                logger.error('Exception occured, error is {0}'.format(traceback.format_exc()))
                self._session = None
                raise e

        return self._session

    def deploy_ovf(self, network, ds, vmname, hostname, eth0, netmask, eth1, gw, dns, ovf_path, dc, host=None,
                   cluster=None, respool=None):
        pre_cmd = '"{ovftool}" --noSSLVerify --acceptAllEulas \
            --network="{network}" \
            --datastore="{ds}" \
            --name={vmname} \
            --prop:VIZION.hostname.setup={hostname} \
            --prop:VIZION.eth0.setup={eth0} \
            --prop:VIZION.eth0_netmask.setup={netmask0} \
            --prop:VIZION.eth1.setup={eth1} \
            --prop:VIZION.eth1_netmask.setup={netmask1} \
            --prop:VIZION.gateway.setup={gw} \
            --prop:VIZION.dns.setup={dns} \
            {ovf_path} \
            vi://{vc_user}:{vc_pwd}@{vc_ip}'.format(ovftool=OVFTOOL, network=network, ds=ds, vmname=vmname,
                                                    hostname=hostname, eth0=eth0,
                                                    netmask0=netmask, eth1=eth1,
                                                    netmask1=netmask, gw=gw,
                                                    dns=dns, ovf_path=ovf_path,
                                                    vc_user=self.vc_user, vc_pwd=self.vc_pwd,
                                                    vc_ip=self.vc_ip)

        if respool is not None and cluster is not None:
            cmd = '{pre_cmd}/{dc}/host/{cluster}/Resources/{respool}'.format(pre_cmd=pre_cmd, dc=dc, cluster=cluster,
                                                                             respool=respool)
        elif respool is None and cluster is not None:
            cmd = '{pre_cmd}/{dc}/host/{cluster}'.format(pre_cmd=pre_cmd, dc=dc, cluster=cluster,
                                                         respool=respool)
        elif respool is None and cluster is None:
            cmd = '{pre_cmd}/{dc}/host/{host}'.format(pre_cmd=pre_cmd, dc=dc, host=host)
        elif respool is not None and cluster is None:
            cmd = '{pre_cmd}/{dc}/host/{host}/Resources/{respool}'.format(pre_cmd=pre_cmd, dc=dc, host=host, respool=respool)

        rtn_dict = util.run_cmd(cmd)
        if 'Completed successfully' in rtn_dict['stdout'] and rtn_dict['rc'] == 0:
            logger.info(rtn_dict['stdout'])
        else:
            logger.error(rtn_dict)
            raise Exception('Deploy ovf failed.')

    @property
    @lock
    def content_obj(self):
        if self._content is None:
            self._content = self.session.RetrieveContent()

        return self._content

    def is_vm_exist(self, vm_name):
        for child in self.content_obj.rootFolder.childEntity:
            vm_obj = self.content_obj.searchIndex.FindChild(child.vmFolder, vm_name)
            if vm_obj:
                break
        else:
            raise Exception('VM {0} is not exist!'.format(vm_name))

    def get_vm_dc(self, vm_obj):
        for dc_obj in self.dcs_obj:
            if self.content_obj.searchIndex.FindChild(dc_obj.vmFolder, vm_obj.name):
                return dc_obj.name

    def get_vm_cluster(self, vm_obj):
        for cluster_obj in self.clusters_obj:
            for host_obj in cluster_obj.host:
                if vm_obj in host_obj.vm:
                    return cluster_obj.name

    @property
    def dcs_obj(self):
        dcs_view_obj = self.content_obj.viewManager.CreateContainerView(self.content_obj.rootFolder, [vim.Datacenter],
                                                                        True)
        return dcs_view_obj.view

    @property
    def clusters_obj(self):
        clusters_view_obj = self.content_obj.viewManager.CreateContainerView(self.content_obj.rootFolder,
                                                                             [vim.ClusterComputeResource], True)
        return clusters_view_obj.view

    @property
    def esxs_obj(self):
        esxs_view_obj = self.content_obj.viewManager.CreateContainerView(self.content_obj.rootFolder, [vim.HostSystem],
                                                                         True)
        return esxs_view_obj.view

    def get_dc_obj(self, dc_name):
        for dc_obj in self.dcs_obj:
            if dc_obj.name == dc_name:
                return dc_obj
        else:
            raise Exception('Cannot find data center {name}!'.format(name=dc_name))

    def get_cluster_obj(self, cluster_name):
        for cluster_obj in self.clusters_obj:
            if cluster_obj.name == cluster_name:
                return cluster_obj
        else:
            raise Exception('Cannot find cluster {name}!'.format(name=cluster_name))

    def get_esx_obj(self, esx_host):
        for esx_obj in self.esxs_obj:
            if esx_obj.name == esx_host:
                return esx_obj
        else:
            raise Exception('Cannot find esxi host {esx} obj!'.format(esx=esx_host))

    @retry(tries=10, delay=1)
    def get_vm_obj_by_name(self, vm_name):
        for esx_obj in self.esxs_obj:
            for vm_obj in esx_obj.vm:
                if vm_obj.name == vm_name:
                    return vm_obj
        else:
            raise Exception('VM {vm_name} is not found.'.format(vm_name=vm_name))

    @retry(tries=10, delay=1)
    def get_vm_obj_by_ip(self, vm_ip):
        vm_obj = self.content_obj.searchIndex.FindByIp(None, vm_ip, True)
        if vm_obj is None:
            raise Exception('VM {ip} is not found.'.format(ip=vm_ip))
        return vm_obj

    def get_vm_name_by_ip(self, vm_ip):
        return self.get_vm_obj_by_ip(vm_ip).name

    # def get_vm_obj_by_name(self, vm_name):
    #     for dc_obj in self.dcs_obj:
    #         vm_obj = self.content_obj.searchIndex.FindChild(dc_obj.vmFolder, vm_name)
    #         if vm_obj is not None:
    #             return vm_obj
    #     else:
    #         raise Exception('VM {vm_name} is not found.'.format(vm_name=vm_name))

    def get_vm_network(self, vm_obj):
        return vm_obj.network[0].name

    def get_vm_resource_pool(self, vm_obj):
        return vm_obj.resourcePool.summary.name

    def get_vm_name(self, vm_obj):
        return vm_obj.name

    def get_vm_hostname(self, vm_obj):
        return vm_obj.guest.hostName

    def get_vm_ip(self, vm_obj):
        return vm_obj.guest.ipAddress

    def get_vm_memory(self, vm_obj):
        return vm_obj.config.hardware.memoryMB

    def get_vm_cpu(self, vm_obj):
        return vm_obj.config.hardware.numCPU

    @retry(tries=120, delay=10)
    def wait_vm_poweroff(self, vm_obj):
        vm_state = vm_obj.runtime.powerState
        vm_name = vm_obj.name
        if vm_state == 'poweredOff':
            logger.info('{0} have been power off, vm status is {1}'.format(vm_name, vm_state))
        else:
            raise Exception('Wait {0} is powered off, vm status is {1}'.format(vm_name, vm_state))

    @retry(tries=120, delay=10)
    def wait_vm_bootup(self, vm_obj):
        vm_state = vm_obj.runtime.powerState
        vm_tools_status = vm_obj.guest.toolsStatus
        vm_tools_running_status = vm_obj.guest.toolsRunningStatus
        vm_name = vm_obj.name
        if vm_state == 'poweredOn' and vm_tools_status == 'toolsOk' and vm_tools_running_status == 'guestToolsRunning':
            logger.info(
                '{vm_name} have been boot up, vm tools status is {status}, vm tools running status is {r_status}'.format(
                    vm_name=vm_name, status=vm_tools_status, r_status=vm_tools_running_status))
        else:
            raise Exception(
                'Wait {vm_name} is boot up, vm tools status is {status}, vm tools running status is {r_status}'.format(
                    vm_name=vm_name, status=vm_tools_status, r_status=vm_tools_running_status))

    def suspend_vm(self, vm_obj):
        vm_name = vm_obj.name
        if vm_obj.runtime.powerState == 'poweredOff':
            raise Exception('Exception occurred: {state} can not be suspend.'.format(state=vm_obj.runtime.powerState))

        if vm_obj.runtime.powerState == 'suspended':
            logger.info('Suspend {vm_name} success'.format(vm_name=vm_name))

        task = vm_obj.SuspendVM_Task()

        try:
            task_rtn = WaitForTask(task)
        except Exception as e:
            logger.error('Suspend {vm_name} fail'.format(vm_name=vm_name))
            raise e
        else:
            if (vm_obj.runtime.powerState == 'suspended') and (task_rtn == vim.TaskInfo.State.success):
                logger.info('Suspend {vm_name} success'.format(vm_name=vm_name))
            else:
                logger.error('Suspend {vm_name} fail, vm status is {status}, result is {result}'.format(
                    vm_name=vm_name, status=vm_obj.runtime.powerState, result=task_rtn))
                raise Exception('Exception occurred: Suspend {vm_name} fail.'.format(vm_name=vm_name))

    def destroy_vm(self, vm_obj):
        vm_name = vm_obj.name

        task = vm_obj.Destroy_Task()

        try:
            task_rtn = WaitForTask(task)
        except Exception as e:
            logger.error('Destroy {vm_name} fail, {err}'.format(vm_name=vm_name, err=e))
            raise e
        else:
            if task_rtn == vim.TaskInfo.State.success:
                logger.info('Destroy {vm_name} success'.format(vm_name=vm_name))
            else:
                logger.error('Destroy {vm_name} fail, result is {result}'.format(vm_name=vm_name, result=task_rtn))
                raise Exception('Exception occurred: Destroy {vm_name} fail.'.format(vm_name=vm_name))

    def poweroff_vm(self, vm_obj):
        vm_name = vm_obj.name
        if vm_obj.runtime.powerState == 'poweredOff':
            logger.info('Power off {vm_name} success'.format(vm_name=vm_name))

        task = vm_obj.PowerOffVM_Task()

        try:
            task_rtn = WaitForTask(task)
        except Exception as e:
            logger.error('Power off {vm_name} fail, {err}'.format(vm_name=vm_name, err=e))
            raise e
        else:
            if task_rtn == vim.TaskInfo.State.success:
                try:
                    self.wait_vm_poweroff(vm_obj)
                except Exception as e:
                    raise e
                else:
                    logger.info('Power off {vm_name} success'.format(vm_name=vm_name))
            else:
                logger.error('Power off {vm_name} fail, vm status is {status}, result is {result}'.format(
                    vm_name=vm_name, status=vm_obj.runtime.powerState, result=task_rtn))
                raise Exception('Exception occurred: Power off {vm_name} fail.'.format(vm_name=vm_name))

    def shutdown_vm(self, vm_obj):
        vm_name = vm_obj.name
        if vm_obj.runtime.powerState == 'poweredOff':
            logger.info('Shutdown {vm_name} success'.format(vm_name=vm_name))

        vm_obj.ShutdownGuest()

        try:
            self.wait_vm_poweroff(vm_obj)
        except Exception as e:
            raise e
        else:
            logger.info('Shutdown {vm_name} success'.format(vm_name=vm_name))

    @retry(tries=5, delay=10)
    def poweron_vm(self, vm_obj):
        vm_name = vm_obj.name
        if vm_obj.runtime.powerState == 'poweredOn':
            logger.info('Power on {vm_name} success'.format(vm_name=vm_name))

        task = vm_obj.PowerOnVM_Task()

        try:
            task_rtn = WaitForTask(task)
        except Exception as e:
            logger.error('Power on {vm_name} fail'.format(vm_name=vm_name))
            raise e
        else:
            if (vm_obj.runtime.powerState == 'poweredOn') and (task_rtn == vim.TaskInfo.State.success):
                logger.info('Power on {vm_name} success'.format(vm_name=vm_name))
                self.wait_vm_bootup(vm_obj)
            else:
                logger.error('Power on {vm_name} fail, vm status is {status}, result is {result}'.format(
                    vm_name=vm_name, status=vm_obj.runtime.powerState, result=task_rtn))
                raise Exception('Exception occurred: Power on {vm_name} fail.'.format(vm_name=vm_name))

    def reset_vm(self, vm_obj):
        vm_name = vm_obj.name
        if vm_obj.runtime.powerState == 'poweredOff' or vm_obj.runtime.powerState == 'suspended':
            raise Exception('Exception occurred: {state} can not be reset.'.format(state=vm_obj.runtime.powerState))

        task = vm_obj.ResetVM_Task()

        try:
            task_rtn = WaitForTask(task)
        except Exception as e:
            logger.error('Reset {vm_name} fail'.format(vm_name=vm_name))
            raise e
        else:
            if (vm_obj.runtime.powerState == 'poweredOn') and (task_rtn == vim.TaskInfo.State.success):
                logger.info('Reset {vm_name} success'.format(vm_name=vm_name))
                self.wait_vm_bootup(vm_obj)
            else:
                logger.error('Reset {vm_name} fail, vm status is {status}, result is {result}'.format(
                    vm_name=vm_name, status=vm_obj.runtime.powerState, result=task_rtn))
                raise Exception('Exception occurred: Reset {vm_name} fail.'.format(vm_name=vm_name))

    def reboot_vm(self, vm_obj):
        vm_name = vm_obj.name
        if vm_obj.runtime.powerState == 'poweredOff' or vm_obj.runtime.powerState == 'suspended':
            raise Exception('Exception occurred: {state} can not be reset.'.format(state=vm_obj.runtime.powerState))

        vm_obj.RebootGuest()

        if vm_obj.runtime.powerState == 'poweredOn':
            logger.info('Reboot {vm_name} success'.format(vm_name=vm_name))
            self.wait_vm_bootup(vm_obj)
        else:
            logger.error('Reboot {vm_name} fail, vm status is {status}'.format(
                vm_name=vm_name, status=vm_obj.runtime.powerState))
            raise Exception('Exception occurred: Reboot {vm_name} fail.'.format(vm_name=vm_name))

    def operate_vm(self, vm_obj, operation):
        operate = {
            "poweroff": self.poweroff_vm,
            "shutdown": self.shutdown_vm,
            "poweron": self.poweron_vm,
            "reboot": self.reboot_vm,
            "reset": self.reset_vm,
            "suspend": self.suspend_vm,
            "destroy": self.destroy_vm
        }
        try:
            return operate[operation](vm_obj)
        except Exception as e:
            logger.error('Exception occurred: {err}, please enter right operate type'
                         '(poweroff,poweron,suspend,reset,reboot,standby,shutdown)'.format(err=traceback.format_exc()))
            raise e

    def batch_opreate_vms(self, vm_names, operation):
        pool = ThreadPoolExecutor(max_workers=10)
        futures = []
        for vm_name in vm_names:
            vm_obj = self.get_vm_obj_by_name(vm_name)
            futures.append(pool.submit(self.operate_vm, vm_obj, operation))
        pool.shutdown()
        for future in as_completed(futures):
            future.result()

    def get_vm_root_snapshot(self, vm_obj):
        return vm_obj.snapshot.rootSnapshotList

    def _get_child_snap_obj(self, snaps_info, snap_name):
        snap_obj = None
        for snap_info in snaps_info:
            if snap_info.name == snap_name:
                snap_obj = snap_info
                break
            else:
                snap_obj = self._get_child_snap_obj(snap_info.childSnapshotList, snap_name)
                if snap_obj is not None:
                    break

        return snap_obj

    def get_snap_obj_by_name(self, snaps_info, snap_name):
        for snap_info in snaps_info:
            if snap_info.name == snap_name:
                snap_obj = snap_info
                break
        else:
            for snap_info in snaps_info:
                snap_obj = self._get_child_snap_obj(snap_info.childSnapshotList, snap_name)
                if snap_obj is not None:
                    break
            else:
                raise Exception('Snapshot {0} is not exist.'.format(snap_name))

        return snap_obj

    def create_snapshot(self, vm_obj, snap_name, description='', dump_memory=False, quiesce=False):
        task = vm_obj.CreateSnapshot_Task(snap_name, description, dump_memory, quiesce)

        try:
            task_rtn = WaitForTask(task)
        except Exception as e:
            raise e
        else:
            if task_rtn == vim.TaskInfo.State.success:
                logger.info('{0} create snapshot {1} done!'.format(vm_obj.name, snap_name))
            else:
                raise Exception('{0} create snapshot {1} fail, error is {2}'.format(vm_obj.name, snap_name, task_rtn))

    def revert_snapshot(self, snap_obj):
        task = snap_obj.snapshot.RevertToSnapshot_Task()
        try:
            task_rtn = WaitForTask(task)
        except Exception as e:
            raise e
        else:
            if task_rtn == vim.TaskInfo.State.success:
                logger.info('Revert snapshot {0} done!'.format(snap_obj.name))
            else:
                raise Exception('Revert snapshot {0} fail, error is {1}'.format(snap_obj.name, task_rtn))

    @print_for_call
    def update_nic_state(self, vm_obj, nic_name='Network adapter 1', nic_state='connect'):
        nic_device = None
        for dev in vm_obj.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualEthernetCard) and dev.deviceInfo.label == nic_name:
                nic_device = dev
        if not nic_device:
            raise RuntimeError('NIC {} could not be found.'.format(nic_name))

        virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
        if nic_state == 'delete':
            virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
        else:
            virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
        virtual_nic_spec.device = nic_device
        virtual_nic_spec.device.key = nic_device.key
        virtual_nic_spec.device.macAddress = nic_device.macAddress
        virtual_nic_spec.device.backing = nic_device.backing
        virtual_nic_spec.device.wakeOnLanEnabled = nic_device.wakeOnLanEnabled
        connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        if nic_state == 'connect':
            connectable.connected = True
            connectable.startConnected = True
        elif nic_state == 'disconnect':
            connectable.connected = False
            connectable.startConnected = False
        else:
            connectable = nic_device.connectable
        virtual_nic_spec.device.connectable = connectable
        device_changes = []
        device_changes.append(virtual_nic_spec)
        spec = vim.vm.ConfigSpec()
        spec.deviceChange = device_changes
        task = vm_obj.ReconfigVM_Task(spec=spec)
        try:
            rtn = WaitForTask(task)
        except Exception as e:
            raise e
        else:
            if rtn == vim.TaskInfo.State.success:
                logger.info('Update VM {0} network to {1} done!'.format(vm_obj.name, nic_state))
            else:
                raise Exception('Update VM {0} network to {1} fail, error is {2}'.format(vm_obj.name, nic_state, rtn))

    def set_vm_network(self, vm_obj, vm_ip, vm_subnet, vm_gateway, vm_dns, vm_hostname):
        nic_num = 0
        for device in vm_obj.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard):
                nic_num += 1

        adapter_map_list = []

        adapter_map = vim.vm.customization.AdapterMapping()
        adapter_map.adapter = vim.vm.customization.IPSettings()
        adapter_map.adapter.ip = vim.vm.customization.FixedIp()
        adapter_map.adapter.ip.ipAddress = vm_ip
        adapter_map.adapter.subnetMask = vm_subnet
        adapter_map.adapter.gateway = vm_gateway

        adapter_map_list.append(adapter_map)

        if nic_num == 2:
            ip_num = vm_ip.split('.')
            vm_ip1 = '192.168.{ip_num1}.{ip_num2}'.format(ip_num1=ip_num[2], ip_num2=ip_num[3])
            adapter_map1 = vim.vm.customization.AdapterMapping()
            adapter_map1.adapter = vim.vm.customization.IPSettings()
            adapter_map1.adapter.ip = vim.vm.customization.FixedIp()
            adapter_map1.adapter.ip.ipAddress = vm_ip1
            adapter_map1.adapter.subnetMask = vm_subnet

            adapter_map_list.append(adapter_map1)

        global_ip = vim.vm.customization.GlobalIPSettings()
        global_ip.dnsServerList = vm_dns

        ident = vim.vm.customization.LinuxPrep(hostName=vim.vm.customization.FixedName(name=vm_hostname))

        customspec = vim.vm.customization.Specification()
        customspec.nicSettingMap = adapter_map_list
        customspec.globalIPSettings = global_ip
        customspec.identity = ident

        task = vm_obj.Customize(spec=customspec)
        try:
            task_rtn = WaitForTask(task)
        except Exception as e:
            raise e
        else:
            if task_rtn == vim.TaskInfo.State.success:
                logger.info('Set vm {0} network done!'.format(vm_obj.name))
            else:
                raise Exception('Set vm {0} network fail, error is {1}'.format(vm_obj.name, task_rtn))

    def set_vm_cpu(self, vm_obj, cpu_num, core_num=None):
        if core_num is None:
            core_num = cpu_num

        vm_spec = vim.vm.ConfigSpec()
        vm_spec.numCPUs = cpu_num
        vm_spec.numCoresPerSocket = core_num

        task = vm_obj.ReconfigVM_Task(spec=vm_spec)
        try:
            task_rtn = WaitForTask(task)
        except Exception as e:
            logger.error('Exception occurred: {err}'.format(err=traceback.format_exc()))
            raise e
        else:
            if task_rtn == vim.TaskInfo.State.success:
                logger.info('Set vm {0} cpu done!'.format(vm_obj.name))
            else:
                raise Exception('Set vm {0} cpu fail, error is {1}'.format(vm_obj.name, task_rtn))

    def set_vm_memory(self, vm_obj, memory_size):
        vm_spec = vim.vm.ConfigSpec()
        vm_spec.memoryMB = memory_size

        task = vm_obj.ReconfigVM_Task(spec=vm_spec)
        try:
            task_rtn = WaitForTask(task)
        except Exception as e:
            raise e
        else:
            if task_rtn == vim.TaskInfo.State.success:
                logger.info('Set vm {0} memory to {1} done!'.format(vm_obj.name, memory_size))
            else:
                raise Exception('Set vm {0} memory fail, error is {1}'.format(vm_obj.name, task_rtn))

    def reserve_vm_memory(self, vm_obj, reserve_memory=None):
        vm_spec = vim.vm.ConfigSpec()
        if reserve_memory is None:
            reserve_memory = self.get_vm_memory(vm_obj)
        vm_spec.memoryAllocation = vim.ResourceAllocationInfo(reservation=reserve_memory)

        task = vm_obj.ReconfigVM_Task(spec=vm_spec)
        try:
            task_rtn = WaitForTask(task)
        except Exception as e:
            raise e
        else:
            if task_rtn == vim.TaskInfo.State.success:
                logger.info('Reserve vm {0} memory done!'.format(vm_obj.name, task_rtn))
            else:
                raise Exception('Reserve vm {0} memory fail, error is {1}'.format(vm_obj.name, task_rtn))

    def reserve_vm_cpu(self, vm_obj, reserve_cpu):
        vm_spec = vim.vm.ConfigSpec()
        vm_spec.cpuAllocation = vim.ResourceAllocationInfo(reservation=reserve_cpu)

        task = vm_obj.ReconfigVM_Task(spec=vm_spec)
        try:
            task_rtn = WaitForTask(task)
        except Exception as e:
            raise e
        else:
            if task_rtn == vim.TaskInfo.State.success:
                logger.info('Reserve vm {0} cpu done!'.format(vm_obj.name))
            else:
                raise Exception('Reserve vm {0} cpu fail, error is {1}'.format(vm_obj.name, task_rtn))

    def get_esx_by_vm(self, vm_obj):
        return vm_obj.summary.runtime.host.name

    def get_largest_free_ds(self, esx_host, ds_type):
        ds_obj_list = []
        largest_free = 0
        view_obj = self.content_obj.viewManager.CreateContainerView(self.content_obj.rootFolder, [vim.Datastore], True)
        all_ds_obj_list = view_obj.view
        for each_ds_obj in all_ds_obj_list:
            for host_obj in each_ds_obj.host:
                if host_obj.key == self.get_esx_obj(esx_host):
                    ds_obj_list.append(each_ds_obj)

        for each_ds in ds_obj_list:
            if not each_ds.summary.accessible:
                logger.debug('{ds} is not accessible, ignore.'.format(ds=each_ds.name))
                continue

            if each_ds.summary.type != 'VMFS':
                print(each_ds)
                logger.debug('{ds} is not VMFS type, ignore.'.format(ds=each_ds.name))
                continue

            try:
                ssd_enable = each_ds.info.vmfs.ssd
            except:
                ssd_enable = False

            if ds_type == 'SSD':
                if not ssd_enable:
                    logger.warning('{ds} is not SSD drive, ignore.'.format(ds=each_ds.name))
                    continue
            elif ds_type == 'HDD':
                if ssd_enable:
                    logger.warning('{ds} is SSD drive, ignore.'.format(ds=each_ds.name))
                    continue
            else:
                raise Exception('Please enter the correct type: HDD, SSD')

            try:
                free_space = each_ds.summary.freeSpace
                if free_space > largest_free:
                    largest_free = free_space
                    ds_obj = each_ds
            except Exception as e:
                logger.warning('Exception occurred on get free ds: {err}. Ignore'.format(err=e))

        limit_size = 100 * 1024 * 1024 * 1024
        if int(largest_free) < limit_size:
            raise Exception('The largest datastore space {largest_free} byte is less than {limit_size} byte.'.format(
                largest_free=largest_free, limit_size=limit_size))

        logger.debug('Largest free ds name: {ds_name}, size: {size}GB'.format(ds_name=ds_obj.name,
                                                                              size=int(
                                                                                  largest_free) / 1024 / 1024 / 1024))
        return ds_obj

    def add_disk(self, vm_obj, ds_type, disk_size):
        vm_name = vm_obj.name
        logger.info("Add disk to {vm} start.".format(vm=vm_name))
        vm_spec = vim.vm.ConfigSpec()
        esx_host = self.get_esx_by_vm(vm_obj)
        ds_obj = self.get_largest_free_ds(esx_host, ds_type)

        unit_number = 0
        pre_controller_key = 0
        for dev in vm_obj.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualDisk):
                unit_number = int(dev.unitNumber) + 1

                # unit_number 7 reserved for scsi controller
                if unit_number == 7:
                    unit_number += 1
                if unit_number >= 16:
                    logger.error('Not support more than 15 disks.')

            if isinstance(dev, vim.vm.device.VirtualSCSIController):
                if pre_controller_key == 0:
                    pre_controller_key = dev.key
                if dev.key > pre_controller_key:
                    continue
                controller = dev

        disk_path = '[{ds_name}] {vmname}/{vmname}_{lun_id}.vmdk'.format(
            ds_name=ds_obj.name, vmname=vm_name, lun_id=unit_number)

        dev_changes = []
        disk_spec = vim.vm.device.VirtualDeviceSpec()
        disk_spec.fileOperation = "create"
        disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        disk_spec.device = vim.vm.device.VirtualDisk()
        disk_spec.device.backing = vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
        disk_spec.device.backing.diskMode = 'persistent'
        disk_spec.device.backing.datastore = ds_obj
        disk_spec.device.backing.fileName = disk_path
        disk_spec.device.unitNumber = unit_number
        disk_spec.device.capacityInKB = int(disk_size) * 1024 * 1024
        disk_spec.device.controllerKey = controller.key
        dev_changes.append(disk_spec)
        vm_spec.deviceChange = dev_changes
        task = vm_obj.ReconfigVM_Task(spec=vm_spec)
        try:
            task_rtn = WaitForTask(task)
        except Exception as e:
            raise e
        else:
            if task_rtn == vim.TaskInfo.State.success:
                logger.info('Add disk {0} to {1} done.'.format(ds_obj.name, vm_name))
            else:
                raise Exception('Add disk to {0} fail, error is {1}'.format(vm_name, task_rtn))

    def linked_clone_vm(self, vm_obj, new_vm_name):
        vm_name = vm_obj.name
        snapshot = self.get_vm_root_snapshot(vm_obj)[0].snapshot
        vm_folder = self.get_dc_obj(self.get_vm_dc(vm_obj)).vmFolder

        relocate_spec = vim.vm.RelocateSpec(
            diskMoveType='createNewChildDiskBacking'
        )

        clone_spec = vim.vm.CloneSpec(
            powerOn=False,
            template=False,
            location=relocate_spec,
            snapshot=snapshot
        )

        task = vm_obj.CloneVM_Task(name=new_vm_name, spec=clone_spec, folder=vm_folder)
        try:
            task_rtn = WaitForTask(task)
        except Exception as e:
            raise e
        else:
            if task_rtn == vim.TaskInfo.State.success:
                logger.info('Linked clone {0} success'.format(vm_name))
            else:
                raise Exception('Linked clone {0} fail, error is {1}'.format(vm_name, task_rtn))


if __name__ == '__main__':
    vmware_obj = VMwareObj('192.168.5.6', 'administrator@vsphere.local', 'P@ssw0rd', 443)
    vm_ip = '192.168.5.116'
    print(vmware_obj.get_vm_obj_by_ip(vm_ip).name)

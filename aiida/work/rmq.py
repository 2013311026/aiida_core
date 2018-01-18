import json
import plum
import plum.rmq

from aiida.utils.serialize import serialize_data, deserialize_data
from aiida.common.setup import get_profile_config, RMQ_PREFIX_KEY
from aiida.backends import settings

from . import events

__all__ = ['new_blocking_control_panel', 'BlockingProcessControlPanel',
           'RemoteException', 'DeliveryFailed']

RemoteException = plum.RemoteException
DeliveryFailed = plum.DeliveryFailed

_MESSAGE_EXCHANGE = 'messages'
_LAUNCH_QUEUE = 'process.queue'


def _get_prefix():
    """Get the queue prefix from the profile."""
    return 'aiida-' + get_profile_config(settings.AIIDADB_PROFILE)[RMQ_PREFIX_KEY]


def encode_response(response):
    serialized = serialize_data(response)
    return json.dumps(serialized)


def decode_response(response):
    response = json.loads(response)
    return deserialize_data(response)


def get_launch_queue_name(prefix=None):
    if prefix is not None:
        return "{}.{}".format(prefix, _LAUNCH_QUEUE)

    return _LAUNCH_QUEUE


def create_communicator():
    pass


def get_message_exchange_name(prefix):
    return "{}.{}".format(prefix, _MESSAGE_EXCHANGE)


class ProcessControlPanel(object):
    """
    RMQ control panel for launching, controlling and getting status of
    Processes over the RMQ protocol.
    """

    def __init__(self, prefix, rmq_connector, testing_mode=False):
        self._connector = rmq_connector

        message_exchange = get_message_exchange_name(prefix)
        self.communicator = plum.rmq.RmqCommunicator(
            rmq_connector,
            exchange_name=message_exchange)

        task_queue_name = "{}.{}".format(prefix, _LAUNCH_QUEUE)
        self._launch = plum.rmq.ProcessLaunchPublisher(
            self._connector,
            exchange_name=get_message_exchange_name(prefix),
            task_queue_name=task_queue_name,
            testing_mode=testing_mode
        )

    def ready_future(self):
        return plum.gather(
            self._launch.initialised_future(),
            self.communicator.initialised_future())

    def pause_process(self, pid):
        return self.execute_action(plum.PauseAction(pid))

    def play_process(self, pid):
        return self.execute_action(plum.PlayAction(pid))

    def kill_process(self, pid, msg=None):
        return self.execute_action(plum.CancelAction(pid))

    def request_status(self, pid):
        return self.execute_action(plum.StatusAction(pid))

    def launch_process(self, process_class, init_args=None, init_kwargs=None):
        action = plum.rmq.LaunchProcessAction(process_class, init_args, init_kwargs)
        action.execute(self._launch)
        return action

    def continue_process(self, pid):
        action = plum.rmq.ContinueProcessAction(pid)
        action.execute(self._launch)
        return action

    def execute_process(self, process_class, init_args=None, init_kwargs=None):
        action = plum.rmq.ExecuteProcessAction(process_class, init_args, init_kwargs)
        action.execute(self._launch)
        return action

    def execute_action(self, action):
        action.execute(self.communicator)
        return action


class BlockingProcessControlPanel(ProcessControlPanel):
    """
    A blocking adapter for the ProcessControlPanel.
    """

    def __init__(self, prefix, rmq_config=None, testing_mode=False):
        if rmq_config is None:
            rmq_config = {
                'url': 'amqp://localhost',
                'prefix': prefix,
            }

        self._loop = events.new_event_loop()
        self._connector = plum.rmq.RmqConnector(amqp_url=rmq_config['url'], loop=self._loop)
        super(BlockingProcessControlPanel, self).__init__(prefix, self._connector, testing_mode)

        self._connector.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def execute_process_start(self, process_class, init_args=None, init_kwargs=None):
        action = plum.rmq.ExecuteProcessAction(process_class, init_args, init_kwargs)
        action.execute(self._launch)
        return events.run_until_complete(action.get_launch_future(), self._loop)

    def execute_action(self, action):
        action.execute(self.communicator)
        return events.run_until_complete(action, self._loop)

    def close(self):
        self._connector.close()


def new_blocking_control_panel():
    """
    Create a new blocking control panel based on the current profile configuration

    :return: A new control panel instance
    :rtype: :class:`BlockingProcessControlPanel`
    """
    return BlockingProcessControlPanel(_get_prefix())

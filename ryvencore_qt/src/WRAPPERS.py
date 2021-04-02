"""These classes wrap the default ryvencore classes by adding Qt signals used by the front end.
Notice also the Node subclass in Node.py which, besides other things, also adds that to the default implementation.
Same for Session."""

from qtpy.QtCore import QObject, Signal

from .ryvencore.logging.Log import Log as RC_Log
from .ryvencore.logging.Logger import Logger as RC_Logger

from .ryvencore.Flow import Flow as RC_Flow
from .ryvencore.Node import Node
from .ryvencore.NodePort import NodePort
from .ryvencore.Connection import Connection, DataConnection as RC_DataConnection

from .ryvencore.script_variables.Variable import Variable
from .ryvencore.script_variables.VarsManager import VarsManager as RC_VarsManager


class Log(RC_Log, QObject):

    enabled = Signal()
    disabled = Signal()
    wrote = Signal(str)
    cleared = Signal()

    def __init__(self, title: str):
        QObject.__init__(self)
        RC_Log.__init__(self, title=title)

    def write(self, *args):
        RC_Log.write(self, args)
        self.wrote.emit(self.current_lines[-1])

    def clear(self):
        RC_Log.clear(self)
        self.cleared.emit()

    def disable(self):
        RC_Log.disable(self)
        self.disabled.emit()

    def enable(self):
        RC_Log.enable(self)
        self.enabled.emit()


class Logger(RC_Logger, QObject):

    new_log_created = Signal(Log)

    def __init__(self, script, create_default_logs=True):
        QObject.__init__(self)
        RC_Logger.__init__(self, script=script, create_default_logs=create_default_logs)

    def new_log(self, title: str) -> Log:
        log = RC_Logger.new_log(self, title=title)
        self.new_log_created.emit(log)
        return log


class VarsManager(RC_VarsManager, QObject):

    new_var_created = Signal(Variable)
    var_deleted = Signal(Variable)
    var_val_changed = Signal(Variable, object)

    def __init__(self, script, config=None):
        QObject.__init__(self)
        RC_VarsManager.__init__(self, script=script, config=config)

    def create_new_var(self, name: str, val=None) -> Variable:
        """Creates and returns a new script variable and emits new_var_created"""

        v = RC_VarsManager.create_new_var(self, name=name, val=val)
        self.new_var_created.emit(v)
        return v

    def delete_variable(self, var: Variable):
        """Deletes a variable and triggers the var_deleted signal."""

        RC_VarsManager.delete_variable(self, var=var)
        self.var_deleted.emit(var)

    def set_var(self, name, val) -> bool:
        """Sets the value of an existing script variable.
        Returns true in case of success, false if the var couldn't be found and set."""

        b = RC_VarsManager.set_var(self, name=name, val=val)
        if b:
            var = self.variables[self._get_var_index_from_name(name)]
            self.var_val_changed.emit(var, var.val)
        return b


class Flow(RC_Flow, QObject):

    node_added = Signal(Node)
    node_removed = Signal(Node)
    connection_added = Signal(Connection)
    connection_removed = Signal(Connection)
    connection_request_valid = Signal(bool)
    nodes_created_from_config = Signal(list)
    connections_created_from_config = Signal(list)

    algorithm_mode_changed = Signal(str)

    def __init__(self, session, script):
        QObject.__init__(self)
        RC_Flow.__init__(self, session=session, script=script)

    def add_node(self, node: Node):
        """Stores a node object and emits node_added"""

        RC_Flow.add_node(self, node=node)
        self.node_added.emit(node)

    def remove_node(self, node: Node):
        """Removes a node from internal list without deleting it; emits node_removed"""

        RC_Flow.remove_node(self, node=node)
        self.node_removed.emit(node)

    def add_connection(self, c: Connection):
        """Adds a connection object and emits connection_added"""

        RC_Flow.add_connection(self, c=c)
        self.connection_added.emit(c)

    def remove_connection(self, c: Connection):
        """Removes a connection object without deleting it and emits connection_removed"""

        RC_Flow.remove_connection(self, c=c)
        self.connection_removed.emit(c)

    def check_connection_validity(self, p1: NodePort, p2: NodePort, emit=False) -> bool:
        """Checks whether a considered connect action is legal and emits connection_request_valid if emit=True"""

        valid = RC_Flow.check_connection_validity(self, p1=p1, p2=p2)
        if emit:
            self.connection_request_valid.emit(valid)
        return valid

    def create_nodes_from_config(self, nodes_config: list):
        """Creates Nodes from nodes_config, previously returned by config_data"""

        nodes = RC_Flow.create_nodes_from_config(self, nodes_config=nodes_config)
        self.nodes_created_from_config.emit(nodes)
        return nodes

    def connect_nodes_from_config(self, nodes: [Node], config: list):
        connections = RC_Flow.connect_nodes_from_config(self, nodes=nodes, config=config)
        self.connections_created_from_config.emit(connections)
        return connections

    def set_algorithm_mode(self, mode: str):
        """Sets the algorithm mode of the flow, possible values are 'data' and 'exec'"""

        RC_Flow.set_algorithm_mode(self, mode=mode)
        self.algorithm_mode_changed.emit(self.algorithm_mode())


class DataConnection(RC_DataConnection, QObject):

    activated = Signal(object)

    def __init__(self, params):
        QObject.__init__(self)
        RC_DataConnection.__init__(self, params=params)

    def activate(self, data=None):
        self.activated.emit(data)
        RC_DataConnection.activate(self, data=data)

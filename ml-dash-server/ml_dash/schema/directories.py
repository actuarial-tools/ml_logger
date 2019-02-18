from os import listdir
from os.path import isfile, join, split

from graphene import ObjectType, relay, String, List
from ml_dash import schema


class Directory(ObjectType):
    class Meta:
        interfaces = relay.Node,

    name = String(description='name of the directory')

    # description = String(description='string serialized data')
    # experiments = List(lambda: schema.Experiments)
    # children = List(lambda: schema.DirectoryAndFiles)

    directories = relay.ConnectionField(lambda: schema.directories.DirectoryConnection)
    files = relay.ConnectionField(lambda: schema.files.FileConnection)

    def resolve_directories(self, info, **kwargs):
        from ml_dash.config import Args
        root_dir = join(Args.logdir, self.id[1:])
        return [schema.Directory(id=join(self.id, _), name=_)
                for _ in listdir(root_dir) if not isfile(join(root_dir, _))]

    def resolve_files(self, info, **kwargs):
        from ml_dash.config import Args
        root_dir = join(Args.logdir, self.id[1:])
        return [schema.Directory(id=join(self.id, _), name=_)
                for _ in listdir(root_dir) if isfile(join(root_dir, _))]

    @classmethod
    def get_node(cls, info, id):
        return get_directory(id)


class DirectoryConnection(relay.Connection):
    class Meta:
        node = Directory


def get_directory(id):
    # path = os.path.join(Args.logdir, id[1:])
    return Directory(id=id, name=split(id[1:])[1])
import logging

class BaseStorageAdapter(object):
    """
    This is an abstract class that represents the interface
    that all storage adapters should implement.
    """
    def __init__(self, *args, **kwargs):

            """
            Initialize common attributes shared by all storage adapters.
            :param str tagger_language: The language that the tagger uses to remove stopwords.
            """
            self.logger = kwargs.get('logger', logging.getLogger(__name__))

    def create_container(self,container_name):
             """
               Creates container with given container name.
               container_name is case insensitive.
             """

             raise self.AdapterMethodNotImplementedError(
                'The `create_container` method is not implemented by this adapter.'
             )

    def remove_container(self,container_name):
         """
           deletes container with given container name.
           container_name is case insensitive.
         """

         raise self.AdapterMethodNotImplementedError(
             'The `remove_container` method is not implemented by this adapter.'
         )

    def remove_file(self,container_name,file_name):
        """
        Drop the database attached to a given adapter.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `remove_file` method is not implemented by this adapter.'
        )

    def get_container_list(self):
        """
            lists all  containers.
        """
        get_container_list=[]
        return get_container_list

    def get_all_files(self,container_name):
        """
            lists all  files for given container_name.
        """
        get_file_list = []
        return get_file_list

    def upload_file(self,container_name,file_name,file_path):
        """
            uploads file mentioned in file_path to container specified by container_name with name as given file_name
        """
        raise self.AdapterMethodNotImplementedError(
            'The `upload_file` method is not implemented by this adapter.'
        )

    def upload_data_stream(self,container_name,file_name,data_stream,data_type):
        """
            uploads data stream directly to given container_name
        """
        raise self.AdapterMethodNotImplementedError(
            'The `upload_data_stream` method is not implemented by this adapter.'
        )

    def download_all_files(self,container_name,download_path):
        """
            downloads all files inside container specified by container_name to specified path
        """
        raise self.AdapterMethodNotImplementedError(
            'The `download_all_files` method is not implemented by this adapter.'
        )

    def download_n_files(self,container_name,download_path, num_of_files):
        """
            downloads n number of files inside container specified by container_name to specified path
        """
        raise self.AdapterMethodNotImplementedError(
            'The `download_n_files` method is not implemented by this adapter.'
        )

    def set_policy(self,container_name,policy):
        """
            you can set policy to specific container
        """
        raise self.AdapterMethodNotImplementedError(
            'The `set_policy` method is not implemented by this adapter.'
        )

    def get_policy(self, container_name):
        """
            you can get policy to specific container
        """
        raise self.AdapterMethodNotImplementedError(
            'The `get_policy` method is not implemented by this adapter.'
        )

    def get_meta_data(self,container_name,file_name):
        """
            get meta_data of container
        """
        raise self.AdapterMethodNotImplementedError(
            'The `get_meta_data` method is not implemented by this adapter.'
        )

    def count_files(self,container_name):
        """
            count number of files of container
        """

        raise self.AdapterMethodNotImplementedError(
            'The `count` method is not implemented by this adapter.'
        )

    class AdapterMethodNotImplementedError(NotImplementedError):
        """
        An exception to be raised when a storage adapter method has not been implemented.
        Typically this indicates that the method should be implement in a subclass.
        """
        pass

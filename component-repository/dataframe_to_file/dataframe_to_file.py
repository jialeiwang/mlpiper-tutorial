from __future__ import print_function

import argparse
import sys
import time
import os
import pandas

from parallelm.components import ConnectableComponent

class MCenterWriteDFComponentAdapter(ConnectableComponent):
    """
    Adapter for write_df_to_file 
    """

    def __init__(self, engine):
        super(self.__class__, self).__init__(engine)

    def _materialize(self, parent_data_objs, user_data):
        file_path = self._params["sinkfilename"]
        df_data = parent_data_objs[0]
        return [self._write_df_to_file(df_data, file_path)]

    def _write_df_to_file(self, df_data, filepath):
        """
        Save DataFrame to file
        """
        suffix_time_stamp = str(int(time.time()))
        save_file = str(filepath) + '.' + suffix_time_stamp
        with open(save_file, 'w+', encoding='utf-8') as sfile:
            pandas.DataFrame(df_data).to_csv(path_or_buf=sfile)

        if not os.path.exists(save_file):
            self._logger.error("stderr- failed to write {}".format(save_file), file=sys.stderr)
            raise Exception("failed writing to file: {}".format(save_file))
        return save_file


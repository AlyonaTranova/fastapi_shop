import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from orm import SyncOrm

SyncOrm.create_tables()
SyncOrm.insert_workers()
SyncOrm.select_workers()
SyncOrm.update_workers()


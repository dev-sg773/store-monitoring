import database
import pytz
from datetime import datetime, time, timedelta
from pprint import pprint

DEFAULT_TIMEZONE = "America/New_York"
DEFAULT_START_TIME = time(0,0)
DEFAULT_END_TIME = time(23, 59, 59)

class Store:
    def __init__(self, store_id):
        '''
        '''
        self.store_id = store_id
        self._set_store_operation_time()
        self._set_store_timezone()
        self._set_store_statuses()

    def _get_current_local_time(self):
        '''
        '''
        local_timezone = pytz.timezone(self.local_timezone)
        now_utc = datetime.now(pytz.UTC)
        now_local = now_utc.astimezone(local_timezone)
        return now_local.replace(tzinfo=None)

    def _set_store_operation_time(self):
        '''
        '''
        operation_time = database.get_store_operation_time(self.store_id)
        # set defaults
        for i in range(0, 7):
            if not operation_time[i]:
                operation_time[i].append({
                    "start_time_local": DEFAULT_START_TIME,
                    "end_time_local": DEFAULT_END_TIME
                })
        self.operation_time = dict(operation_time)
    
    def _set_store_timezone(self):
        '''
        '''
        self.local_timezone = database.get_local_timezone(self.store_id) or DEFAULT_TIMEZONE
    
    def _set_store_statuses(self):
        '''
        '''
        statuses = database.get_store_statuses(self.store_id, self.local_timezone)
        # make date as key
        self.statuses = {
            status["local_date"]: status["local_time_list"]
            for status in statuses
        }
    
    def get_stats_for_last_day(self):
        '''
        '''
        current_datetime = self._get_current_local_time()
        last_date = (current_datetime - timedelta(days=1))
        last_day_statuses = self.statuses.get(last_date.date())
        last_day_operation_time = self.operation_time.get(last_date.weekday())
        print(last_day_statuses, last_day_operation_time)

        active_hours = []
        activity = []
        for operational_hour in last_day_operation_time:
            for i, status_log in last_day_statuses: 
                if status_log['local_timestamp'] > operational_hour['start_time_local']:
                    pre_status = last_day_statuses[i-1]['status']
                    activity.push(pre_status)
                    break

        for operational_hour in last_day_operation_time:
            for i, status_log in last_day_statuses: 
                interval = operational_hour['end_time_local'] - operational_hour['start_time_local']
                if status_log['local_timestamp'] in interval:




    



# local testing
if __name__ == "__main__":
    store = Store("3345190510668585029")
    # print(store.local_timezone)
    # print(store.operation_time.keys())
    store.get_stats_for_last_day()
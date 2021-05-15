import dateutil.parser
from tqdm import tqdm
import numpy as np
import pandas as pd
import concurrent.futures as cf

# CONSTANTS
# tqdm kwargs
rec_kwargs = {'bar_format': '{l_bar}{bar:10}{r_bar}{bar:-10b}', 
              'unit': 'rec', 
              'position': 0, 
              'mininterval': 0.5}
wrk_kwargs = {'bar_format': '{l_bar}{bar:10}{r_bar}{bar:-10b}', 
              'unit': 'wrk', 
              'position': 0, 
              'mininterval': 0.5}

class HKRecord:
    
    def __init__(self, xml_element):
        """
        Health Kit Record object.

        Parameters
        ----------
        xml_element : ElementTree child
            ElementTree child for Apple's Health Kit Workout tag.

        Returns
        -------
        None.

        """
        
        self.rec_type = xml_element.get('type')
        self.source_name = xml_element.get('sourceName')
        self.source_version = xml_element.get('sourceVersion')
        self.device = xml_element.get('device')
        self.unit = xml_element.get('unit')
        self.creation_date = dateutil.parser.parse(xml_element.attrib['creationDate'])
        self.start_date = dateutil.parser.parse(xml_element.attrib['startDate'])
        self.end_date = dateutil.parser.parse(xml_element.attrib['endDate'])
        
        # If unit is non then is a categorical value, otherwise convert to float
        if self.unit is None:
            self.value = xml_element.get('value')
        else:
            self.value = float(xml_element.get('value'))
        
    def __repr__(self):
        return f'<HKRecord - type: {self.rec_type}, src: {self.source_name}, created: {self.creation_date}>'

    def __str__(self):
        if isinstance(self.value, float):
            ret_str = \
            f'''
            RECORD - {self.creation_date}\n
            {self.rec_type} from {self.source_name}\n
            ======================================================================\n
            From {self.start_date} to {self.end_date}\n
            Value: {self.value:.3f} {self.unit}\n
            '''
        else:
            f'''
            RECORD - {self.creation_date}\n
            {self.rec_type} from {self.source_name}\n
            ======================================================================\n
            From {self.start_date} to {self.end_date}\n
            Value: {self.value} {self.unit}\n
            '''
        return ret_str

class HKWorkout:
    
    def __init__(self, xml_element):
        """
        Health Kit Workout object.

        Parameters
        ----------
        xml_element : ElementTree child
            ElementTree child for Apple's Health Kit Workout tag.

        Returns
        -------
        None.

        """
        
        self.activity_type = xml_element.get('workoutActivityType')
        self.duration = float(xml_element.get('duration'))
        self.duration_unit = xml_element.get('durationUnit')
        self.total_distance = float(xml_element.get('totalDistance'))
        self.total_distance_unit = xml_element.get('totalDistanceUnit')
        self.total_energy_burned = float(xml_element.get('totalEnergyBurned'))
        self.total_energy_burned_unit = xml_element.get('totalEnergyBurnedUnit')
        self.source_name = xml_element.get('sourceName')
        self.source_version = xml_element.get('sourceVersion')
        self.device = xml_element.get('device')
        self.creation_date = dateutil.parser.parse(xml_element.attrib['creationDate'])
        self.start_date = dateutil.parser.parse(xml_element.attrib['startDate'])
        self.end_date = dateutil.parser.parse(xml_element.attrib['endDate'])
        
    def __repr__(self):
        return f'<HKWorkout - type: {self.activity_type}, src: {self.source_name}, created: {self.creation_date}>'
    
    def __str__(self):
        ret_str = \
        f'''
        WORKOUT - {self.creation_date}\n
        {self.activity_type} from {self.source_name}\n
        ======================================================================\n
        From {self.start_date} to {self.end_date}\n
        Duration:\t{self.duration:.2f}\t{self.duration_unit}\n
        Distance:\t{self.total_distance:.3f}\t{self.total_distance_unit}\n
        Energy:\t\t{self.total_energy_burned:.2f}\t{self.total_energy_burned_unit}
        '''
        return ret_str
    
def load_xml_tag(xml_root, selected_tag, output_class, n_threads=None, tqdm_kwargs={'unit': 'it'}):
    """
    Utility function used by health kit classes to load data from xml tags.

    Parameters
    ----------
    xml_root : ElementTree root
        ElementTree root for the xml element.
    selected_tag : string
        Tag name, used by ElementTree findall to search for the selcted tag.
    output_class : health kit class (HKRecord, HKWorkout)
        class used for creating the output list.
    n_threads : int, optional
        Number of thread used by concurrent.futures to run multiple threads 
        for loading the xml. The default is None (use default number of 
        threads).
    tqdm_kwargs : dict, optional
        dict with tqdm kwargs. The default is {'unit': 'it'}.

    Returns
    -------
    tags_object : list
        list of object of the output class (HKRecord, HKWorkout) described 
        into the xml.

    """
    
    # Convert tags to Python class
    with cf.ThreadPoolExecutor(max_workers=n_threads) as executor:
        future_tags = [executor.submit(lambda x: output_class(x), tag) 
                        for tag in tqdm(xml_root.findall(selected_tag), 
                                        postfix='Submit jobs for ' + selected_tag, **tqdm_kwargs)]
        for f in tqdm(cf.as_completed(future_tags), postfix='Convert ' + selected_tag, 
                      total=len(future_tags), **tqdm_kwargs):
            pass
    # Return results
    tags_object = [f.result() for f in future_tags]
    return tags_object

def load_records(xml_root, n_threads=None):
    """
    Load Record tags from xml root.

    Parameters
    ----------
    xml_root : ElementTree root
        ElementTree root for the xml element.
    n_threads : int, optional
        Number of thread used by concurrent.futures to run multiple threads 
        for loading the xml. The default is None (use default number of 
        threads).

    Returns
    -------
    records : list
        list of records (HKRecord) described into the xml.

    """
    
    # Return list of records
    records = load_xml_tag(xml_root, 'Record', HKRecord, n_threads=n_threads, tqdm_kwargs=rec_kwargs)
    return records

def load_workouts(xml_root, n_threads=None):
    """
    Load Workout tags from xml root.

    Parameters
    ----------
    xml_root : ElementTree root
        ElementTree root for the xml element.
    n_threads : int, optional
        Number of thread used by concurrent.futures to run multiple threads 
        for loading the xml. The default is None (use default number of 
        threads).

    Returns
    -------
    workouts : list
        list of workouts (HKWorkout) described into the xml.

    """
    
    # Return list of workouts
    workouts = load_xml_tag(xml_root, 'Workout', HKWorkout, n_threads=n_threads, tqdm_kwargs=wrk_kwargs)
    return workouts


def build_single_workout_timeseries(workout, records, rem_duplicates=True, ts_source=None):
    """
    Build a dict collecting timeseries of records grouped by type.
    The original workout is available inside the resulting dict, as well as 
    records units (grouped by types).

    Parameters
    ----------
    workout : healthkit.HKWorkout
        single workout (HKWorkout) from workouts list as given by 
        load_workouts function.
    records : list
        list of records (HKRecord) as given by load_records function.
    rem_duplicates : bool, optional
        remove duplicated timestampes from timeseries if set to True.
        Duplicated records are not removed from dict 'records' keyword.
        The default is True.
    ts_source : list of strings, optional
        use record from selected data source (see HKRecord.source).
        Records from different sources are not removed from dict 'records' 
        keyword. Always use a list, even if only one source is requested.
        The default is None.

    Returns
    -------
    workout_data : dict
        dictionary with the following keys:
            - workout: HKWorkout given as input
            - records: dict of healthkit.HKRecord objects, each key of the 
            dict is a record type
            - timeseries: dict of pandas timeseries, each key of the dict is a 
            record type
            - units: dictionary of units, each key of the dict is a 
            record type
        This data structure is suitable for operation with pandas dataframes.

    """
    
    # Timesreies source (ts_source) shall be a list
    if not isinstance(ts_source, list):
        raise TypeError('ts_source shall be a list')
    
    # Find records that belong to a certain workout (based on date) and sort them by date
    s_date = workout.start_date
    e_date = workout.end_date
    records_of_workout = sorted([r for r in records if (s_date <= r.start_date <= e_date)], key=lambda x: x.start_date.isoformat())
    
    # Find all unique records type (which are keys for the output dict)
    keys = set([r.rec_type for r in records_of_workout])
    
    # Group records, timeseries and units of measurement based on types
    records_by_type = {}
    ts_by_type = {}
    units = {}
    for key in keys:
        # RECORDS
        # Create a dict of records for the selected type
        records_by_type[key] = [r for r in records_of_workout if (key in r.rec_type)]
        
        # UNITS
        # Assign unit to unit dict
        units[key] = records_by_type[key][0].unit
        
        # TIMESERIES
        # Create an array for timseries, each row is a timestamp-value couple 
        # and collect data from one single source if requested
        if ts_source is not None:
            ts_array = np.array([[r.start_date, r.value] for r in records_of_workout 
                                 if (key in r.rec_type) and (r.source_name in ts_source)])
        else:
            ts_array = np.array([[r.start_date, r.value] for r in records_of_workout 
                                 if (key in r.rec_type)])
        # If the array is empty there is no record that match the source condition
        # Jump to next iteration since there is nothing to add
        if ts_array.size == 0:
            continue        
        # Otherwise select the appropriate data type for timeseries (if not categorical convert to float)
        if 'category' not in key.lower():
            data_type = float
        else:
            data_type = None
        # Convert to timeseries
        ts = pd.Series(ts_array[:,1].ravel(), index=ts_array[:,0].ravel(), name=key, dtype=data_type)
        # Since different sources may store the same infromation twice keep only non-duplicated timestamps
        # Both records are kept in 'records' anyway
        if rem_duplicates:
            ts_by_type[key] = ts[~ts.index.duplicated()]
        else:
            ts_by_type[key] = ts
    
    # Return results
    workout_data = {'workout': workout, 'records': records_by_type, 'timeseries': ts_by_type, 'units': units}
    return workout_data

def build_workouts_timeseries(workouts, records, n_threads=None, rem_duplicates=True, ts_source=None):
    """
    Build a list of dicts that collect timeseries for each workout.
    Timeseries of records for each workout are grouped by type.
    The original workout is available inside each dict of the list, as well as 
    records units (grouped by types).

    Parameters
    ----------
    workouts : list
        list of workouts (HKWorkout) as given by load_workouts.
    records : list
        list of records (HKRecord) as given by load_records function.
    n_threads : int, optional
        Number of thread used by concurrent.futures to run multiple threads 
        for processing data. The default is None (use default number of 
        threads).
    rem_duplicates : bool, optional
        remove duplicated timestampes from timeseries if set to True.
        Duplicated records are not removed from dict 'records' keyword.
        The default is True.
    ts_source : list of strings, optional
        use record from selected data source (see HKRecord.source).
        Records from different sources are not removed from dict 'records' 
        keyword. Always use a list, even if only one source is requested.
        The default is None.

    Returns
    -------
    workouts_data : list
        is a list of dictionaries returned by build_single_workout_timeseries
        Each dictionary has the following keys:
            - workout: HKWorkout given as input
            - records: dict of healthkit.HKRecord objects, each key of the 
            dict is a record type
            - timeseries: dict of pandas timeseries, each key of the dict is a 
            record type
            - units: dictionary of units, each key of the dict is a 
            record type
        This data structure is suitable for operation with pandas dataframes.

    """
    
    # Initiate collecting variable
    workouts_data = []
    
    # Multi-threads for assigning records to workouts
    with cf.ThreadPoolExecutor(max_workers=n_threads) as executor:
        future_data = [executor.submit(lambda x: build_single_workout_timeseries(x, records, rem_duplicates=rem_duplicates, ts_source=ts_source), workout) 
                        for workout in tqdm(workouts, postfix='Submit jobs for building timeseries', **wrk_kwargs)]
        for f in tqdm(cf.as_completed(future_data), postfix='Build timeseries for each workout', 
                        total=len(future_data), **wrk_kwargs):
            pass
        
    # Return results
    workouts_data = [f.result() for f in future_data]
    return workouts_data
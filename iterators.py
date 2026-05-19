from pathlib import Path;
import mne;

#needed for now will be removed in later
input_folder = input("PATH : ");

eeg_data_list = [];

#for processing summary file
def process_summary(file_item_obj) :

    with open(file_item_obj, 'r', encoding='utf-8') as f:

        current_file_dict = None
        
        for line in f :
            line = line.strip();

            if line.startswith("File Name:"):
                current_file_dict = {
                    "file_name": line.split(':')[1].strip(),
                    "num_seizures": 0,
                    "seizures": []
                };
            
                eeg_data_list.append(current_file_dict);

            elif current_file_dict and line.startswith("Number of Seizures in File:") :
                current_file_dict["num_seizures":int(line.split(':')[1].strip())];

            elif current_file_dict and line.startswith("Seizure") and "Start Time" in line:
                start_time = int(line.split(':')[1].replace('seconds', '').strip());
                # Append a new seizure dictionary into this file's seizure list
                current_file_dict["seizures"].append({"start": start_time});
                
            # 4. Seizure End Time
            elif current_file_dict and line.startswith("Seizure") and "End Time" in line:
                end_time = int(line.split(':')[1].replace('seconds', '').strip());
                current_file_dict["seizures"][-1]["end"] = end_time;
            
def epoching(raw) :
    chunk_duration =4.0;

    epochs = mne.make_fixed_length_epochs(raw,chunk_duration,preload=True);
        



#for reading edf file
def process_edf(folder) :
    
    for file in eeg_data_list :

        edf_path = folder / file["file_name"];

        raw = mne.io.read_raw_edf(edf_path, preload=True);
        raw.notch_filter(freqs=60.0);
        raw.filter(l_freq=0.5,h_freq=50.0);
        if(file["siezures"] == 0) :
            pass
        else :
            for seizure_timing in file["seizure"] :

                start = seizure_timing["start"];
                end = seizure_timing["end"];

                interictal_crop1 = raw.copy().crop(tmax=start);
                ictal_crop = raw.copy().crop(tmin=start,tmax=end);
                interictal_crop2 = raw.copy().crop(tmin=end);



#for iterating the files inside the folder
def folder_iterator(path) :
    eeg_data_list = [];
    folder = Path(path);
    summary_file = f"{folder.name}-summary.txt";

    process_summary(Path(summary_file));
    process_edf(folder);


        







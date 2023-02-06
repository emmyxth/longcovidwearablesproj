import os
import sys



if __name__ == "__main__":
    # 
    size, model_name, file_path, index = sys.argv
    participant_id = os.path.basename(file_path)
    print("participant_id: ", participant_id)
    
    print("Done setting up the data: ", participant_id)
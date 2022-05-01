"""

standardize the uttrans

"""
from os import listdir
import os
import glob
import pandas as pd
"""
# This part puts all text transcripts to one, which has been processed already
def process_apy(apy_dir):
    
    apy_name = listdir(apy_dir)
    
    apy_ids = []
    apy_transcripts = []
    
    for category in apy_name:
      
        fpath = os.path.join(apy_dir , category, 'session01')
        textfiles = listdir(fpath)
  
    
        for fname in textfiles:

            audio_id = fname.split('.')[0]
           
            
            if fname.endswith(".txt"):
                
                cur_path =os.path.join(fpath, fname)
                with open(cur_path, 'r', encoding='utf-8') as f:
                    
                    context = f.readlines()
                    
                    apy_ids.append(audio_id)
                    apy_transcripts.append(context)
                    
    return apy_ids, apy_transcripts
"""
def get_spk_utr(apy_modified_dir):

    apy_modi_name = listdir(apy_modified_dir)
    
    spk_ids = []
    spk_genders = {}
    utr_ids = [] 
    
    
    for fname in apy_modi_name:
        
        if fname.endswith(".metadata"):
            
            cur_path = os.path.join(apy_modified_dir, fname)
           
            
            with open(cur_path, 'r', encoding='utf-8') as f:
                    
                    context = f.read().split('\n')
                    spk_id = context[17].split('\t')[1]
                    spk_gender = context[18].split('\t')[1]
                    utr_id = fname.split('.')[0] #context[2].split('\t')[1]
                    
            
            spk_ids.append(spk_id)
            utr_ids.append(utr_id)
            
            if spk_id not in spk_genders:
                
                if spk_gender == 'Female':
                    
                    spk_genders[spk_id] = 'f'
                
                else:
                    
                    spk_genders[spk_id] = 'm'
                
            
            
    return spk_ids, utr_ids, spk_genders
    

 
def get_utt_spk(utt_spk_format, spk_ids, utr_ids, utt_to_spk  = True):
    
    if utt_to_spk == True:
        
        utt2spk = []
        
        for spk, utr in zip(spk_ids, utr_ids):
            
            
            add_line = utt2spk_format % (spk, utr, spk)
            
            utt2spk.append(add_line)
            
        return utt2spk
        
    else:
        
        spk2utt = []
        spk2utt_dict = {}
        
        for spk, utr in zip(spk_ids, utr_ids):
            
            if spk not in spk2utt_dict:
                
                spk2utt_dict[spk] = [utr]
                
            else:
                
                spk2utt_dict[spk].append(utr)

        
        for spk, utrs in spk2utt_dict.items():
            
            spk2utt.append(spk + '\n')
            
            for u in utrs:
                
                
                add_line = spk2utt_format % (spk, u)
                
                spk2utt.append(add_line)
        

        return spk2utt
    

    

def write_file(fname, list_doc):
    
    with open(fname, 'w', encoding = 'utf-8') as f:
        
        for l in list_doc:
            
            f.write(l)
            

if __name__ == '__main__':
    
  
    
    # process apy
    apy_dir = 'APY_modified/data'
    apy_modified_dir = 'APY_modified/downloads'
    apy_trans_dir = 'APY_modified/apy_transcripts.txt'
    dev_pct = 0.1
    test_pct = 0.1
    """"""
    
    spk_ids, utr_ids, spk_genders = get_spk_utr(apy_modified_dir)
    
    
    
    ########### text ############

    
    with open(apy_trans_dir,'r', encoding = 'utf-8') as f:
        texts = f.readlines()
    texts = [s + '-' + t for s, t in zip(spk_ids, texts)]
    texts = [t.replace('<NON>','').replace('<STA>','').replace('<SPK>','').replace('<NPS>','')  for t in texts]

    
    ########### wav scp ############
    
    scp_format = '%s-%s ffmpeg -i downloads/%s.wav -f wav -ar 16000 -ab 16 -ac 1 - |\n'
    
    #wav_scp_doc = wav_scp(scp_format, spk_ids, utr_ids)
    wav_scp_doc = [scp_format % (spk_id, utr_id, utr_id) for spk_id, utr_id in zip(spk_ids, utr_ids) ]
    
    
      
    ########### spk2utt #############
    
    # This part will be processed later
    spk2utt_format = '%s-%s \n'
    

    
    
    ########### utt2spk ##############
    
    utt2spk_format = '%s-%s %s \n'
    
    utt2spk = [utt2spk_format % (spk, utr, spk) for spk, utr in zip(spk_ids, utr_ids)]

    
    
    ########### spk_gender ############
    
    utt_gender_format = '%s-%s %s \n'
    
    utt_gender_list = [utt_gender_format % (spk_id, utr_id, spk_genders[spk_id]) for spk_id, utr_id in zip(spk_ids, utr_ids)]
  
    ########### train_test_split ############
    num_train = int(len(utt_gender_list) * (1 - dev_pct - test_pct))
    num_dev = int(len(utt_gender_list) * dev_pct)
    num_test = int(len(utt_gender_list) * test_pct)
    
    train_idx = [0, num_train]
    dev_idx = [num_train, num_train + num_dev]
    test_idx = [num_train + num_dev, len(utt_gender_list)]
    
    text_path = 'text'
    wav_scp_path = 'wav.scp'
    utt_to_gender_path = 'utt2gender'
    utt_to_spk_path = 'utt2spk'
    spk_to_utt_path = 'spk2utt'
    
    for folder in ['train', 'dev', 'test']:
        

        save_folder = os.path.join(apy_dir, folder)
        
        
        if folder == 'train':
            
            start_idx = train_idx[0]
            end_idx = train_idx[1]
            
        elif folder == 'dev':
            
            start_idx = dev_idx[0]
            end_idx = dev_idx[1]
            
        elif folder == 'test':
            
            start_idx = test_idx[0]
            end_idx = test_idx[1]
            
            
        # write text
        write_file(os.path.join(save_folder, text_path), texts[ start_idx : end_idx])
        
        # write wav scp
        write_file(os.path.join(save_folder, wav_scp_path), wav_scp_doc[ start_idx : end_idx])
        
        # write utt2gender
        write_file(os.path.join(save_folder, utt_to_gender_path), utt_gender_list[ start_idx : end_idx])
        
        # write utt2spk
        write_file(os.path.join(save_folder, utt_to_spk_path), utt2spk[ start_idx : end_idx])
        
        
        # write spk2utt
        spk_ids_cur = [t.split('-')[0] for t in texts[ start_idx : end_idx]]
        utr_ids_cur = [t.split('-')[1].split(' ')[0] for t in texts[ start_idx : end_idx]]
        
        spk2utt = get_utt_spk(spk2utt_format, spk_ids_cur, utr_ids_cur, utt_to_spk  = False)
        
        write_file(os.path.join(save_folder, spk_to_utt_path), spk2utt)
        
        
        
        
        
        
        
            
        
    

    
    
     
    
    
    
    
"""

preprocess_transcripts Sichuan dialect

"""

from os import listdir
import os



 
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
        #print(spk2utt_dict)
        
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
    sc_dir = 'Sichuan_Dialect_Scripted_Speech_Corpus_Daily_Use_Sentence'
    sc_wav_dir = 'Sichuan_Dialect_Scripted_Speech_Corpus_Daily_Use_Sentence/downloads'
    sc_spk_dir = 'SPKINFO.txt'
    sc_utt_dir = 'UTTRANSINFO.txt'
    
    sc_name = listdir(sc_dir)
    sc_wav = listdir(sc_wav_dir)
    
    dev_pct = 0.1
    test_pct = 0.1
    
    # get the texts

    texts = []
    with open(os.path.join(sc_dir, sc_utt_dir), 'r', encoding = 'utf-8') as f:
        
        context = f.readlines()
    
    
    context = [c.split('\t') for c in context][1:]
    
    raw_txt = [c[4] for c in context] 
    spk_ids = [c[2] for c in context]
    utr_ids = [c[1].split('.')[0] for c in context]
    
    ########### text ############
    txt_format = '%s-%s %s'
    texts = [txt_format % (s, u ,t) for s, u, t in zip(spk_ids, utr_ids, raw_txt)]
    
    ########### wav scp ############
    
    scp_format = '%s-%s ffmpeg -i downloads/%s.wav -f wav -ar 16000 -ab 16 -ac 1 - |\n'
    
    #wav_scp_doc = wav_scp(scp_format, spk_ids, utr_ids)
    wav_scp_doc = [scp_format % (spk_id, utr_id, utr_id) for spk_id, utr_id in zip(spk_ids, utr_ids) ]
    
    ########### spk2utt #############
    
    spk2utt_format = '%s-%s \n'
    
    ########### utt2spk ##############
    
    utt2spk_format = '%s-%s %s \n'
    
    #utt2spk = get_utt_spk(utt2spk_format, spk_ids, utr_ids, utt_to_spk  = True)
    utt2spk = [utt2spk_format % (spk, utr, spk) for spk, utr in zip(spk_ids, utr_ids)]

    
    
    ########### utt_gender ############
    with open(os.path.join(sc_dir, sc_spk_dir), 'r', encoding = 'utf-8') as f:
        
        context = f.readlines()
        
    context = [c.split('\t') for c in context][1:]
    
    spk_gender_dict = {c[1]: c[2].lower() for c in context}
    
    utt_gender_format = '%s-%s %s \n'
    #utt_gender = [uttgender_format % (i, spk_gender_dict[g]) for i, g in zip(utr_ids, spk_ids)]
    
    
    
    utt_gender = [utt_gender_format % (spk_id, utr_id, spk_gender_dict[spk_id]) for spk_id, utr_id in zip(spk_ids, utr_ids)]
  
    
    
    ########### train_test_split ############
    num_train = int(len(utt_gender) * (1 - dev_pct - test_pct))
    num_dev = int(len(utt_gender) * dev_pct)
    num_test = int(len(utt_gender) * test_pct)
    
    train_idx = [0, num_train]
    dev_idx = [num_train, num_train + num_dev]
    test_idx = [num_train + num_dev, len(utt_gender)]
    
    text_path = 'text'
    wav_scp_path = 'wav.scp'
    utt_to_gender_path = 'utt2gender'
    utt_to_spk_path = 'utt2spk'
    spk_to_utt_path = 'spk2utt'
    
    for folder in ['train', 'dev', 'test']:
        
        save_folder = os.path.join(sc_dir, 'data',  folder)
        
        
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
        write_file(os.path.join(save_folder, utt_to_gender_path), utt_gender[ start_idx : end_idx])
        
        # write utt2spk
        write_file(os.path.join(save_folder, utt_to_spk_path), utt2spk[ start_idx : end_idx])
        
        
        # write spk2utt
        spk_ids_cur = [t.split('-')[0] for t in texts[ start_idx : end_idx]]
        utr_ids_cur = [t.split('-')[1].split(' ')[0] for t in texts[ start_idx : end_idx]]
        
        spk2utt = get_utt_spk(spk2utt_format, spk_ids_cur, utr_ids_cur, utt_to_spk  = False)
        
        write_file(os.path.join(save_folder, spk_to_utt_path), spk2utt)
        
        
        
        
        
        
        
            
        
    

    
    
     
    
    
    
    

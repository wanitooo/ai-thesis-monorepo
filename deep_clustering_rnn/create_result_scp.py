import os

result_s1_scp = 'result_rnn_jusper_speaker1.scp'
result_s2_scp = 'result_rnn_jusper_speaker2.scp'

result_s1 = './result/DPCL_optim_jusper/spk1'
result_s2 = './result/DPCL_optim_jusper/spk2'

result_s1_file = open(result_s1_scp, 'w')
for root, dirs, files in os.walk(result_s1):
    files.sort()
    for file in files:
        result_s1_file.write(file+" "+root+'/'+file)
        result_s1_file.write('\n')


result_s2_file = open(result_s2_scp, 'w')
for root, dirs, files in os.walk(result_s2):
    files.sort()
    for file in files:
        result_s2_file.write(file+" "+root+'/'+file)
        result_s2_file.write('\n')
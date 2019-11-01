import remote_context
import math

class S_SPK_INFO:
    rssi = -10000
    drop = {'OK' : 0 , 'NOK' : 0, 'TOTAL' : 0 }
    wifi = {'OK' : 0 , 'NOK' : 0, 'TOTAL' : 0 }
    srtt = -10000

class S_AUDIO_SOURCE_INFO:
    bit = '-'
    sample = '-'
    ch = '-'

class S_AUDIO_PLAY_INFO:
    tot_ch = '-'
    master_ch = '-'
    slave_ch = '-'

class S_SPK_TABLE:
    ch = '-'
    bit = '-'
    sample = '-'
    vol = '-'

class S_WOW_INFO:
    state = '-'
    play_latency = '-'
    play_drop = '- / - / -'

class S_NW_INFO:
    ch = '-'
    rssi = '- / - / -'
    loss = '- / - / -'

class S_DEV_INFO:
    sel = False
    mac = []
    role =[]
    ch = []
    vol = []

class S_GROUP_INFO:
    group_id = ''
    ch_cfg = ''
    topology = ''
    group_vol = ''
    group_name = ''
    dev_info = {}

group = {}
def update_group_info_cmn(clr_flag=False, gr_id = None,ch_cfg = None, topology = None, group_name = None):
    global group
    # Remove group information
    if clr_flag is True:
        if gr_id is None:
            group = {}
        else:
            if gr_id in group:
                del group[gr_id]
        return

    if gr_id not in group:
        group[gr_id] = {}

    if ch_cfg is not None: group[gr_id]['ch_cfg'] = ch_cfg
    if topology is not None: group[gr_id]['topology'] = topology
    if group_name is not None: group[gr_id]['group_name'] = group_name

def update_group_info_group_vol(gr_id=None, gr_vol=None):
    global group
    #Remove device information
    if gr_id in group:
        group[gr_id]['group_vol'] = gr_vol
    else:
        print("GroupID [%d] is not present", gr_id)

def Update_dev_info_in_group(clr_flag = False, sel_flag=None,gr_id=None,dev_id=None,macAddr=None,role=None,ch=None,vol=None):
    global group
    # Remove device information
    if clr_flag is True:
        if dev_id is None:
            group[gr_id]['dev_info'] = {}
        else:
            if dev_id in group[gr_id].dev_info:
                del group[gr_id]['dev_info'][dev_id]
        return

    if 'dev_info' not in group[gr_id]:
        group[gr_id]['dev_info'] = {}

    if dev_id not in group[gr_id]['dev_info']:
        group[gr_id]['dev_info'][dev_id] = {}

    if sel_flag is not None: group[gr_id]['dev_info'][dev_id]['sel'] = sel_flag
    if macAddr is not None: group[gr_id]['dev_info'][dev_id]['mac'] = macAddr
    if role is not None: group[gr_id]['dev_info'][dev_id]['role'] = role
    if ch is not None:
        group[gr_id]['dev_info'][dev_id]['ch'] = []
        group[gr_id]['dev_info'][dev_id]['ch_x.x.x'] = []
        tmp = [0,0,0]
        group[gr_id]['dev_info'][dev_id]['ch_bitmap'] = ch
        for key in remote_context.CH_BITMAP_TO_STRING.keys():
            if ch & key is not 0:
                group[gr_id]['dev_info'][dev_id]['ch'].append(remote_context.CH_BITMAP_TO_STRING[key])
                for idx in range(0,3):
                    tmp[idx] += remote_context.CH_BITMAP_TO_CONFIG_CH_NUM[key][idx]
                group[gr_id]['dev_info'][dev_id]['ch_x.x.x'] = tmp

    if vol is not None: group[gr_id]['dev_info'][dev_id]['vol'] = vol

meas_info = {}
def Update_active_group_meas_info(clr_flag=False,dev_id=None,rssi=None,nPlayback=None,nDrop=None,nRcv=None,nLoss=None,srtt=None):
    global meas_info
    if clr_flag is True:
        meas_info = {}
        return

    meas_info[dev_id] = {}
    meas_info[dev_id]['rssi'] = rssi

    meas_info[dev_id]['nPlayback'] = nPlayback
    meas_info[dev_id]['nDrop'] = nDrop
    try:
        meas_info[dev_id]['dropRate'] = math.ceil(nDrop / (nPlayback) * 1000) / 10  # Percent
    except:
        meas_info[dev_id]['dropRate'] = -1
        print("drop rate is divided by zero",nDrop,nPlayback)

    meas_info[dev_id]['nRcv'] = nRcv
    meas_info[dev_id]['nLoss'] = nLoss
    try:
        meas_info[dev_id]['lossRate'] = math.ceil(nLoss / (nRcv + nLoss) * 1000) / 10  # Percent
    except:
        print("loss rate is divided by zero", nDrop, nPlayback)
        meas_info[dev_id]['lossRate'] = -1

    meas_info[dev_id]['srtt'] = srtt

    return [meas_info[dev_id]['dropRate'], meas_info[dev_id]['lossRate']]



def Get_active_group_info(gr_id=None):
    global group
    if gr_id in group:
        return group[gr_id]
    else:
        print("GroupID [%d] is not present!!", gr_id)
        return -1

# Play Pause Info
play_status = 0
def update_play_status(status):
    global play_status
    play_status = status

def Get_play_status():
    global play_status
    return play_status

# Mute Unmute Info
mute_status = 0
def update_mute_status(status):
    global mute_status
    mute_status = status

def Get_mute_status():
    global mute_status
    return mute_status


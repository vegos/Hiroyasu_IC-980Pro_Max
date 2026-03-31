#!/usr/bin/env python3

# ---------------------------------
# Copyright ©2026, Antonis Maglaras
# ---------------------------------
# Tool for exporting and importing channel data from Hiroyasu IC-980Pro Max
# to a human-readable CSV file for editing.
#
# It modifies only currently known and validated fields, while preserving all
# unknown/internal data from the original YSF file.
#
# This is a VERY BETA version. Use it at your own risk.
# Always verify the generated file in CPS before writing it to the radio.


import argparse
import csv
import re
from pathlib import Path

RECORD_START = 622
RECORD_SIZE = 85
CHANNEL_COUNT = 500	# This is the total memories for IC-980Pro Max

# main 85-byte channel record offsets
MAIN_FLAGS_OFF = 0
SCRAMBLE_RAW_OFF = 1
MODE_WEATHER_OFF = 2
PTT_PUSH_OFF = 3
PTT_POP_OFF = 4
NAME_OFF = 5
NAME_LEN = 16
RX_OFF = 27
TX_OFF = 41
QT_DQT_ENC_OFF = 55
QT_DQT_DEC_OFF = 68
EXTRA_FLAGS_OFF = 84

# companion per-channel bytes live immediately before the channel table
# one helper byte per channel: busy inhibit + rx signal code
SIG_BUSY_BASE = RECORD_START - CHANNEL_COUNT  # 122 for this layout

REMARKS = {
    "channel_index": "1-based channel number as shown in CPS",
    "name": f"Channel name, up to {NAME_LEN} ASCII characters",
    "rx_mhz": "Receive frequency in MHz, e.g. 145.50000",
    "tx_mhz": "Transmit frequency in MHz, e.g. 145.50000",
    "tx_power": "Low/High",
    "bandwidth": "Narrow/Wide",
    "scan": "ADD/DEL",
    "busy_inhibit": "OFF/DQT/CAT",
    "rx_signal_code": "OFF/DTMF/FSK/FSK DTMF",
    "special_dcs": "OFF/Special DCS 1/Special DCS 2/Special DCS 3/Special DCS 4",
    "fm_am": "FM/AM",
    "weather_alert": "OFF/ON",
    "scramble": "OFF/scramble1..scramble8",
    "vague_subaudio": "OFF/ON",
    "compander": "OFF/ON",
    "ptt_push_code": "OFF/ID/Code form-1..Code form-30",
    "ptt_pop_code": "OFF/ID/Code form-1..Code form-30",
    "qt_dqt_enc": "Off or 67.0 / D023N / D023I / ...",
    "qt_dqt_dec": "Off or 67.0 / D023N / D023I / ...",
    "rx_hz": "Raw receive frequency in Hz; import accepts this too",
    "tx_hz": "Raw transmit frequency in Hz; import accepts this too",
    "offset": "Record start offset in file",
    "main_flags": "Raw main flag byte",
    "sig_busy": "Raw helper byte for busy inhibit and rx signal code",
    "scramble_raw": "Raw scramble/vague subaudio byte",
    "mode_weather": "Raw FM/AM + weather alert byte",
    "ptt_push_raw": "Raw PTT push code byte",
    "ptt_pop_raw": "Raw PTT pop code byte",
    "extra_flags": "Raw final byte of record",
    "qt_dqt_enc_hex": "Raw 3-byte TX QT/DQT field",
    "qt_dqt_dec_hex": "Raw 3-byte RX QT/DQT field",
    "raw_record_hex": f"Entire {RECORD_SIZE}-byte channel record in hex",
}

CTCSS_VALUES = {
    670:"67.0", 693:"69.3", 719:"71.9", 744:"74.4", 770:"77.0",
    797:"79.7", 825:"82.5", 854:"85.4", 885:"88.5", 915:"91.5",
    948:"94.8", 974:"97.4", 1000:"100.0", 1035:"103.5", 1072:"107.2",
    1109:"110.9", 1148:"114.8", 1188:"118.8", 1230:"123.0", 1273:"127.3",
    1318:"131.8", 1365:"136.5", 1413:"141.3", 1462:"146.2", 1514:"151.4",
    1567:"156.7", 1598:"159.8", 1622:"162.2", 1655:"165.5", 1679:"167.9",
    1713:"171.3", 1738:"173.8", 1773:"177.3", 1799:"179.9", 1835:"183.5",
    1862:"186.2", 1899:"189.9", 1928:"192.8", 1966:"196.6", 1995:"199.5",
    2035:"203.5", 2065:"206.5", 2107:"210.7", 2181:"218.1", 2257:"225.7",
    2291:"229.1", 2336:"233.6", 2418:"241.8", 2503:"250.3", 2541:"254.1",
}
CTCSS_ENCODE = {v:k for k,v in CTCSS_VALUES.items()}
DCS_ENCODE = {
    "023":10259,"025":10261,"026":10262,"031":10265,"032":10266,"036":10270,
    "043":10275,"047":10279,"051":10281,"053":10283,"054":10284,"065":10293,
    "071":10297,"072":10298,"073":10299,"074":10300,"114":10316,"115":10317,
    "116":10318,"122":10322,"125":10325,"131":10329,"132":10330,"134":10332,
    "143":10339,"145":10341,"152":10346,"155":10349,"156":10350,"162":10354,
    "165":10357,"172":10362,"174":10364,"205":10373,"212":10378,"223":10387,
    "225":10389,"226":10390,"243":10403,"244":10404,"245":10405,"246":10406,
    "251":10409,"252":10410,"255":10413,"261":10417,"263":10419,"265":10421,
    "266":10422,"271":10425,"274":10428,"306":10438,"311":10441,"315":10445,
    "325":10453,"331":10457,"332":10458,"343":10467,"346":10470,"351":10473,
    "356":10474,"364":10482,"365":10483,"371":10486,"411":10516,"412":10517,
    "413":10518,"423":10520,"431":10521,"432":10522,"445":10534,"446":10535,
    "452":10542,"454":10545,"455":10546,"462":10554,"464":10556,"465":10557,
    "466":10558,"503":10582,"506":10590,"516":10594,"523":10599,"526":10602,
    "532":10606,"546":10618,"565":10633,"606":10640,"612":10643,"624":10652,
    "627":10657,"631":10659,"632":10660,"645":10661,"654":10668,"662":10691,
    "664":10698,"703":10707,"712":10713,"723":10714,"731":10716,"732":10723,
    "734":10724,"743":10731,"754":10732,
}
DCS_DECODE = {v:k for k,v in DCS_ENCODE.items()}
DCS_RE = re.compile(r"^D?(\d{3})([NI])$", re.IGNORECASE)

BUSY_MAP = {0x00:"OFF",0x08:"DQT",0x10:"CAT"}
RX_SIGNAL_MAP = {0x00:"OFF",0x20:"DTMF",0x40:"FSK",0x60:"FSK DTMF"}
SPECIAL_DCS_MAP = {0x00:"OFF",0x02:"Special DCS 1",0x04:"Special DCS 2",0x06:"Special DCS 3",0x08:"Special DCS 4"}

def rec_start(idx:int)->int:
    return RECORD_START + (idx-1)*RECORD_SIZE

def sig_busy_offset(idx:int)->int:
    return SIG_BUSY_BASE + (idx-1)

def decode_name(b:bytes)->str:
    return b.split(b"\x00",1)[0].decode("ascii","ignore").rstrip()

def encode_name(s:str)->bytes:
    raw=(s or "").encode("ascii","ignore")[:NAME_LEN]
    return raw + b"\x00"*(NAME_LEN-len(raw))

def fmt_mhz(hz:int)->str:
    if hz <= 0:
        return ""
    return f"{hz/1_000_000:.5f}"

def parse_freq(row:dict, primary_key:str, secondary_key:str)->int:
    primary=(row.get(primary_key,"") or "").strip()
    secondary=(row.get(secondary_key,"") or "").strip()
    if primary:
        return int(round(float(primary)*1_000_000)) if "." in primary else int(float(primary))
    if secondary:
        return int(round(float(secondary)*1_000_000)) if "." in secondary else int(float(secondary))
    return 0

def decode_tone(raw3:bytes)->str:
    if len(raw3)!=3:
        return ""
    code=int.from_bytes(raw3[:2],"little")
    mode=raw3[2]
    if raw3 in (b"\x00\x00\x00", b"\xff\xff\x00"):
        return "Off"
    if mode==1:
        return CTCSS_VALUES.get(code, raw3.hex().upper())
    if mode==2:
        return f"D{DCS_DECODE.get(code, str(code).zfill(3))}N"
    if mode==3:
        return f"D{DCS_DECODE.get(code, str(code).zfill(3))}I"
    return raw3.hex().upper()

def encode_tone(text:str)->bytes:
    t=(text or "").strip()
    if not t or t.lower()=="off":
        return b"\x00\x00\x00"
    if t in CTCSS_ENCODE:
        return CTCSS_ENCODE[t].to_bytes(2,"little")+b"\x01"
    if re.fullmatch(r"[0-9A-Fa-f]{6}", t):
        return bytes.fromhex(t)
    m=DCS_RE.match(t)
    if m:
        code_txt,pol=m.groups()
        code=DCS_ENCODE.get(code_txt)
        if code is None:
            raise ValueError(f"unknown DCS code: {t}")
        mode=2 if pol.upper()=="N" else 3
        return code.to_bytes(2,"little")+bytes([mode])
    raise ValueError(f"unsupported tone string: {t}")

def decode_busy(v:int)->str:
    return BUSY_MAP.get(v & 0x18, f"0x{v&0x18:02X}")
def encode_busy(text:str, old:int)->int:
    t_raw=(text or "").strip()
    t=t_raw.upper()
    if not t:
        return old
    inv={v:k for k,v in BUSY_MAP.items()}
    if t in inv:
        return (old & ~0x18) | inv[t]
    # Tolerate legacy/debug CSV rows where a raw hex helper byte lands here.
    if t.startswith("0X"):
        try:
            return int(t, 16) & 0xFF
        except ValueError:
            return old
    return old

def decode_rx_signal(v:int)->str:
    return RX_SIGNAL_MAP.get(v & 0x60, f"0x{v&0x60:02X}")
def encode_rx_signal(text:str, old:int)->int:
    t=(text or "").strip().upper().replace("_"," ")
    if not t: return old
    inv={v:k for k,v in RX_SIGNAL_MAP.items()}
    return (old & ~0x60) | inv[t]

def decode_special_dcs(v:int)->str:
    return SPECIAL_DCS_MAP.get(v & 0x0E, f"0x{v&0x0E:02X}")
def encode_special_dcs(text:str, old:int)->int:
    t_raw=(text or "").strip()
    t=t_raw.upper().replace("_"," ")
    if not t:
        return old
    inv={v.upper():k for k,v in SPECIAL_DCS_MAP.items()}
    if t in inv:
        return (old & ~0x0E) | inv[t]
    if t_raw.upper().startswith("0X"):
        try:
            return (old & ~0x0E) | (int(t_raw, 16) & 0x0E)
        except ValueError:
            return old
    return old

def decode_scan(v:int)->str:
    return "ADD" if (v & 0x80) else "DEL"
def encode_scan(text:str, old:int)->int:
    t=(text or "").strip().upper()
    if not t: return old
    if t=="ADD": return old | 0x80
    if t=="DEL": return old & ~0x80
    raise ValueError(f"invalid scan: {text}")

def decode_ptt(v:int)->str:
    if v==0: return "OFF"
    if v==1: return "ID"
    if 2<=v<=31: return f"Code form-{v-1}"
    return str(v)
def encode_ptt(text:str):
    t=(text or "").strip()
    if not t: return None
    u=t.upper()
    if u=="OFF": return 0
    if u=="ID": return 1
    m=re.match(r"^CODE\s*FORM[- ]?(\d+)$", u)
    if m:
        n=int(m.group(1))
        if not (1<=n<=30): raise ValueError(text)
        return n+1
    if t.isdigit():
        n=int(t)
        if not (0<=n<=255): raise ValueError(text)
        return n
    raise ValueError(f"invalid PTT code: {text}")

def decode_scramble(v:int)->str:
    idx=v & 0x0F
    return "OFF" if idx==0 else f"scramble{idx}"
def encode_scramble(text:str, old:int)->int:
    t=(text or "").strip()
    if not t: return old
    u=t.upper()
    if u=="OFF": return old & 0xF0
    m=re.match(r"^SCRAMBLE\s*(\d+)$", u)
    if not m: raise ValueError(f"invalid scramble: {text}")
    n=int(m.group(1))
    if not (1<=n<=8): raise ValueError(text)
    return (old & 0xF0) | n

def decode_vague(v:int)->str:
    return "ON" if (v & 0x10) else "OFF"
def encode_vague(text:str, old:int)->int:
    t=(text or "").strip().upper()
    if not t: return old
    if t=="ON": return old | 0x10
    if t=="OFF": return old & ~0x10
    raise ValueError(f"invalid vague_subaudio: {text}")

def decode_fm_am(v:int)->str:
    return "AM" if (v & 0x04) else "FM"
def encode_fm_am(text:str, old:int)->int:
    t=(text or "").strip().upper()
    if not t: return old
    if t=="AM": return old | 0x04
    if t=="FM": return old & ~0x04
    raise ValueError(f"invalid fm_am: {text}")

def decode_weather(v:int)->str:
    return "ON" if (v & 0x08) else "OFF"
def encode_weather(text:str, old:int)->int:
    t=(text or "").strip().upper()
    if not t: return old
    if t=="ON": return old | 0x08
    if t=="OFF": return old & ~0x08
    raise ValueError(f"invalid weather_alert: {text}")

def is_used(rec:bytes)->bool:
    return bool(decode_name(rec[NAME_OFF:NAME_OFF+NAME_LEN]) or int.from_bytes(rec[RX_OFF:RX_OFF+4],"little") or int.from_bytes(rec[TX_OFF:TX_OFF+4],"little"))

def read_row(blob:bytes, idx:int, debug:bool=False)->dict:
    start=rec_start(idx)
    rec=blob[start:start+RECORD_SIZE]
    sig_busy=blob[sig_busy_offset(idx)]
    main=rec[MAIN_FLAGS_OFF]
    scramble_raw=rec[SCRAMBLE_RAW_OFF]
    mode_weather=rec[MODE_WEATHER_OFF]
    rx=int.from_bytes(rec[RX_OFF:RX_OFF+4],"little")
    tx=int.from_bytes(rec[TX_OFF:TX_OFF+4],"little")
    row={
        "channel_index": idx,
        "name": decode_name(rec[NAME_OFF:NAME_OFF+NAME_LEN]),
        "rx_mhz": fmt_mhz(rx),
        "tx_mhz": fmt_mhz(tx),
        "tx_power": "High" if (main & 0x20) else "Low",
        "bandwidth": "Wide" if (main & 0x10) else "Narrow",
        "scan": decode_scan(main),
        "busy_inhibit": decode_busy(sig_busy),
        "rx_signal_code": decode_rx_signal(sig_busy),
        "special_dcs": decode_special_dcs(main),
        "fm_am": decode_fm_am(mode_weather),
        "weather_alert": decode_weather(mode_weather),
        "scramble": decode_scramble(scramble_raw),
        "vague_subaudio": decode_vague(scramble_raw),
        "compander": "ON" if (main & 0x01) else "OFF",
        "ptt_push_code": decode_ptt(rec[PTT_PUSH_OFF]),
        "ptt_pop_code": decode_ptt(rec[PTT_POP_OFF]),
        "qt_dqt_enc": decode_tone(rec[QT_DQT_ENC_OFF:QT_DQT_ENC_OFF+3]),
        "qt_dqt_dec": decode_tone(rec[QT_DQT_DEC_OFF:QT_DQT_DEC_OFF+3]),
    }
    if debug:
        row.update({
            "offset": start,
            "rx_hz": rx,
            "tx_hz": tx,
            "qt_dqt_enc_hex": rec[QT_DQT_ENC_OFF:QT_DQT_ENC_OFF+3].hex().upper(),
            "qt_dqt_dec_hex": rec[QT_DQT_DEC_OFF:QT_DQT_DEC_OFF+3].hex().upper(),
            "sig_busy": f"0x{sig_busy:02X}",
            "main_flags": f"0x{main:02X}",
            "scramble_raw": f"0x{scramble_raw:02X}",
            "mode_weather": f"0x{mode_weather:02X}",
            "ptt_push_raw": rec[PTT_PUSH_OFF],
            "ptt_pop_raw": rec[PTT_POP_OFF],
            "extra_flags": f"0x{rec[EXTRA_FLAGS_OFF]:02X}",
            "raw_record_hex": rec.hex().upper(),
        })
    return row

CLEAN_FIELDS = [
    "channel_index","name","rx_mhz","tx_mhz","tx_power","bandwidth","scan",
    "busy_inhibit","rx_signal_code","special_dcs","fm_am","weather_alert",
    "scramble","vague_subaudio","compander","ptt_push_code","ptt_pop_code",
    "qt_dqt_enc","qt_dqt_dec",
]
DEBUG_FIELDS = CLEAN_FIELDS + [
    "offset","rx_hz","tx_hz","qt_dqt_enc_hex","qt_dqt_dec_hex","sig_busy",
    "main_flags","scramble_raw","mode_weather","ptt_push_raw","ptt_pop_raw",
    "extra_flags","raw_record_hex"
]

def export_csv(infile:Path,outfile:Path,used_only:bool=False,debug:bool=False):
    blob=infile.read_bytes()
    rows=[]
    for idx in range(1, CHANNEL_COUNT+1):
        start=rec_start(idx)
        if start+RECORD_SIZE > len(blob):
            break
        rec=blob[start:start+RECORD_SIZE]
        if used_only and not is_used(rec):
            continue
        rows.append(read_row(blob, idx, debug))
    fields = DEBUG_FIELDS if debug else CLEAN_FIELDS
    with outfile.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def import_csv(template_file:Path,csv_file:Path,outfile:Path,debug:bool=False):
    blob=bytearray(template_file.read_bytes())
    with csv_file.open("r", newline="", encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    for row in rows:
        if not (row.get("channel_index","") or "").strip():
            continue
        idx=int((row.get("channel_index") or "").strip())
        start=rec_start(idx)
        if start+RECORD_SIZE > len(blob):
            raise ValueError(f"record {idx} out of range")
        rec=bytearray(blob[start:start+RECORD_SIZE])
        sig_busy=blob[sig_busy_offset(idx)]

        # debug/raw overrides first
        if debug:
            for key, off in [("main_flags", MAIN_FLAGS_OFF),("scramble_raw",SCRAMBLE_RAW_OFF),("mode_weather",MODE_WEATHER_OFF),("ptt_push_raw",PTT_PUSH_OFF),("ptt_pop_raw",PTT_POP_OFF)]:
                txt=(row.get(key,"") or "").strip()
                if txt:
                    rec[off]=int(txt,0)
            txt=(row.get("sig_busy","") or "").strip()
            if txt:
                sig_busy=int(txt,0)
            txt=(row.get("extra_flags","") or "").strip()
            if txt:
                rec[EXTRA_FLAGS_OFF]=int(txt,0)

        # human-editable values
        # Only apply a field when the CSV explicitly changes it compared to the template.
        # This keeps full exports/imports safe even when unused rows decode to noisy defaults.
        cur_name = decode_name(rec[NAME_OFF:NAME_OFF+NAME_LEN])
        cur_rx_mhz = fmt_mhz(int.from_bytes(rec[RX_OFF:RX_OFF+4], "little"))
        cur_tx_mhz = fmt_mhz(int.from_bytes(rec[TX_OFF:TX_OFF+4], "little"))
        cur_tx_power = "High" if (rec[MAIN_FLAGS_OFF] & 0x20) else "Low"
        cur_bandwidth = "Wide" if (rec[MAIN_FLAGS_OFF] & 0x10) else "Narrow"
        cur_scan = decode_scan(rec[MAIN_FLAGS_OFF])
        cur_busy = decode_busy(sig_busy)
        cur_rx_signal = decode_rx_signal(sig_busy)
        cur_special_dcs = decode_special_dcs(rec[MAIN_FLAGS_OFF])
        cur_fm_am = decode_fm_am(rec[MODE_WEATHER_OFF])
        cur_weather = decode_weather(rec[MODE_WEATHER_OFF])
        cur_scramble = decode_scramble(rec[SCRAMBLE_RAW_OFF])
        cur_vague = decode_vague(rec[SCRAMBLE_RAW_OFF])
        cur_compander = "ON" if (rec[MAIN_FLAGS_OFF] & 0x01) else "OFF"
        cur_ptt_push = decode_ptt(rec[PTT_PUSH_OFF])
        cur_ptt_pop = decode_ptt(rec[PTT_POP_OFF])
        cur_qt_enc = decode_tone(bytes(rec[QT_DQT_ENC_OFF:QT_DQT_ENC_OFF+3]))
        cur_qt_dec = decode_tone(bytes(rec[QT_DQT_DEC_OFF:QT_DQT_DEC_OFF+3]))

        name = (row.get("name") or "").strip()
        if name and name != cur_name:
            rec[NAME_OFF:NAME_OFF+NAME_LEN] = encode_name(name)

        rx_text = (row.get("rx_mhz") or "").strip()
        tx_text = (row.get("tx_mhz") or "").strip()
        if rx_text and rx_text != cur_rx_mhz:
            rx = parse_freq(row, "rx_mhz", "rx_hz")
            if rx:
                rec[RX_OFF:RX_OFF+4] = rx.to_bytes(4, "little")
        if tx_text and tx_text != cur_tx_mhz:
            tx = parse_freq(row, "tx_mhz", "tx_hz")
            if tx:
                rec[TX_OFF:TX_OFF+4] = tx.to_bytes(4, "little")

        tp = (row.get("tx_power", "") or "").strip()
        if tp and tp != cur_tx_power:
            if tp.lower() == "high":
                rec[MAIN_FLAGS_OFF] |= 0x20
            elif tp.lower() == "low":
                rec[MAIN_FLAGS_OFF] &= ~0x20

        bw = (row.get("bandwidth", "") or "").strip()
        if bw and bw != cur_bandwidth:
            if bw.lower() == "wide":
                rec[MAIN_FLAGS_OFF] |= 0x10
            elif bw.lower() == "narrow":
                rec[MAIN_FLAGS_OFF] &= ~0x10

        comp = (row.get("compander", "") or "").strip().upper()
        if comp and comp != cur_compander:
            if comp == "ON":
                rec[MAIN_FLAGS_OFF] |= 0x01
            elif comp == "OFF":
                rec[MAIN_FLAGS_OFF] &= ~0x01

        if (row.get("scan", "") or "").strip() and (row.get("scan", "") or "").strip() != cur_scan:
            rec[MAIN_FLAGS_OFF] = encode_scan(row.get("scan", ""), rec[MAIN_FLAGS_OFF])
        if (row.get("special_dcs", "") or "").strip() and (row.get("special_dcs", "") or "").strip() != cur_special_dcs:
            rec[MAIN_FLAGS_OFF] = encode_special_dcs(row.get("special_dcs", ""), rec[MAIN_FLAGS_OFF])

        if (row.get("busy_inhibit", "") or "").strip() and (row.get("busy_inhibit", "") or "").strip() != cur_busy:
            sig_busy = encode_busy(row.get("busy_inhibit", ""), sig_busy)
        if (row.get("rx_signal_code", "") or "").strip() and (row.get("rx_signal_code", "") or "").strip() != cur_rx_signal:
            sig_busy = encode_rx_signal(row.get("rx_signal_code", ""), sig_busy)

        if (row.get("fm_am", "") or "").strip() and (row.get("fm_am", "") or "").strip() != cur_fm_am:
            rec[MODE_WEATHER_OFF] = encode_fm_am(row.get("fm_am", ""), rec[MODE_WEATHER_OFF])
        if (row.get("weather_alert", "") or "").strip() and (row.get("weather_alert", "") or "").strip() != cur_weather:
            rec[MODE_WEATHER_OFF] = encode_weather(row.get("weather_alert", ""), rec[MODE_WEATHER_OFF])
        if (row.get("vague_subaudio", "") or "").strip() and (row.get("vague_subaudio", "") or "").strip() != cur_vague:
            rec[SCRAMBLE_RAW_OFF] = encode_vague(row.get("vague_subaudio", ""), rec[SCRAMBLE_RAW_OFF])
        if (row.get("scramble", "") or "").strip() and (row.get("scramble", "") or "").strip() != cur_scramble:
            rec[SCRAMBLE_RAW_OFF] = encode_scramble(row.get("scramble", ""), rec[SCRAMBLE_RAW_OFF])

        p = encode_ptt(row.get("ptt_push_code", ""))
        if p is not None and (row.get("ptt_push_code", "") or "").strip() != cur_ptt_push:
            rec[PTT_PUSH_OFF] = p
        p = encode_ptt(row.get("ptt_pop_code", ""))
        if p is not None and (row.get("ptt_pop_code", "") or "").strip() != cur_ptt_pop:
            rec[PTT_POP_OFF] = p

        enc_hex = (row.get("qt_dqt_enc_hex", "") or "").strip()
        dec_hex = (row.get("qt_dqt_dec_hex", "") or "").strip()
        enc_text = (row.get("qt_dqt_enc", "") or "").strip()
        dec_text = (row.get("qt_dqt_dec", "") or "").strip()
        if enc_hex:
            rec[QT_DQT_ENC_OFF:QT_DQT_ENC_OFF+3] = bytes.fromhex(enc_hex.replace(" ", ""))
        elif enc_text and enc_text != cur_qt_enc:
            rec[QT_DQT_ENC_OFF:QT_DQT_ENC_OFF+3] = encode_tone(enc_text)
        if dec_hex:
            rec[QT_DQT_DEC_OFF:QT_DQT_DEC_OFF+3] = bytes.fromhex(dec_hex.replace(" ", ""))
        elif dec_text and dec_text != cur_qt_dec:
            rec[QT_DQT_DEC_OFF:QT_DQT_DEC_OFF+3] = encode_tone(dec_text)

        blob[start:start+RECORD_SIZE]=rec
        blob[sig_busy_offset(idx)] = sig_busy

    outfile.write_bytes(blob)

def build_parser():
    p=argparse.ArgumentParser(description="Export/import Hiroyasu IC-980Pro Max .Ysf channel data")
    sub=p.add_subparsers(dest="cmd", required=True)
    pe=sub.add_parser("export")
    pe.add_argument("infile", type=Path)
    pe.add_argument("outfile", type=Path)
    pe.add_argument("--used-only", action="store_true")
    pe.add_argument("--debug", action="store_true")
    pi=sub.add_parser("import")
    pi.add_argument("template_file", type=Path, help="Base .Ysf to patch; usually the original file")
    pi.add_argument("csv_file", type=Path)
    pi.add_argument("outfile", type=Path)
    pi.add_argument("--debug", action="store_true")
    return p

def main():
    args=build_parser().parse_args()
    if args.cmd=="export":
        export_csv(args.infile,args.outfile,used_only=args.used_only,debug=args.debug)
        print(f"[OK] exported {args.outfile}")
    else:
        import_csv(args.template_file,args.csv_file,args.outfile,debug=args.debug)
        print(f"[OK] wrote {args.outfile}")

if __name__=="__main__":
    main()

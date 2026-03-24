# Hiroyasu IC-980Pro Max Channels Tool

A (python) tool for exporting, editing, and importing channel data from **Hiroyasu IC-980Pro Max** `.Ysf` files using a human-readable CSV format.

This tool performs safe patching: it modifies **only** currently known and validated fields while preserving all unknown/internal data in the original file.  
It's a work-in-progress, so keep up for updates.  

NOTE: This tool works **ONLY** on IC-980Pro Max and not on IC-980Pro (not Max).  

---

## ⚠️ Disclaimer

This is a **VERY BETA** tool.

- Use it at your own risk
- No warranty is provided
- Always verify the generated `.Ysf` file in CPS before writing it to the radio

---

## Features

- Export channels to human-readable CSV
- Edit only meaningful fields (no binary junk)
- Import changes back safely into `.Ysf`
- Preserves unknown/internal data
- Supports most common channel settings

---

## Basic Usage

### Export channels to CSV

python hiroyasu.py export input.Ysf output.csv

### Import CSV back to YSF

python hiroyasu.py import template.Ysf input.csv output.Ysf

⚠️ NOTE: The template `.Ysf` file is **required**. The tool does NOT rebuild files from scratch.

---

## Editable Fields

### Channel Basics

- channel_index → Channel number (1-based)
- name → Channel name (~10 chars max)

---

### Frequencies

- rx_mhz → Receive frequency (MHz)
- tx_mhz → Transmit frequency (MHz)

Use MHz format. Hz fields are internal/debug only.

---

### RF Settings

- tx_power → High / Low
- bandwidth → Wide / Narrow
- scan → ADD / DEL

---

### Signaling / Access Control

- busy_inhibit → OFF / DQT / CAT
- rx_signal_code → OFF / DTMF / FSK / FSK DTMF
- special_dcs → OFF / Special DCS 1..4

---

### Audio / Modulation

- fm_am → FM / AM
- weather_alert → ON / OFF
- vague_subaudio → ON / OFF
- compander → ON / OFF

---

### Scrambler

- scramble → OFF / scramble1..scramble8

---

### PTT Signaling

- ptt_push_code → OFF / ID / Code form-1..30
- ptt_pop_code → OFF / ID / Code form-1..30

---

### CTCSS / DCS

- qt_dqt_enc → TX tone
- qt_dqt_dec → RX tone

Formats:

- CTCSS: 67.0, 88.5, etc
- DCS: D023N, D023I

---

## Important Behavior

### Partial Updates

Only modified values are written back.

This prevents:
- corruption of unused channels
- overwriting unknown data
- CPS issues

---

### Invalid Values

Invalid values are ignored.

Example:
busy_inhibit = ON → ignored

---

### Frequency Limits

CPS may reject invalid ranges.  
Memories with invalid frequencies may be blank.  

---

### Template File

The tool patches an existing `.Ysf` file.

Unknown data is preserved.

---

## Debug Mode

**python hiroyasu.py export input.Ysf output.csv --debug**  

Includes:
- raw hex
- internal flags

Not for normal editing.

---

## Workflow / Syntax

1. Export:  
**python hiroyasu.py export radio.Ysf channels.csv**  
The tool is exporting the CPS file `radio.Ysf` to a csv file called `channels.csv`  

3. Edit CSV

4. Import:  
**python hiroyasu.py import radio.Ysf channels.csv new.Ysf**  
The tool is creating the `new.Ysf` using the csv file `channels.csv`. The `radio.Ysf` is the "template" used.  

6. Load into CPS

---

## Author

Antonis Maglaras - ©2026

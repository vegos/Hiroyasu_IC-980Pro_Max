# Hiroyasu IC-980Pro Max Channels Tool

A Python tool for exporting, editing, and importing channel data from **Hiroyasu IC-980Pro Max** `.Ysf` files using a human-readable CSV format.

This tool performs safe patching: it modifies **only** currently known and validated fields while preserving all unknown/internal data in the original file.  
It is still a work in progress and will be updated over time.

> **Note:** This tool currently supports **only** the **IC-980Pro Max** and **not** the IC-980Pro.

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
- Preserve unknown/internal data
- Support most common channel settings

---

## Basic Usage

### Export channels to CSV

```bash
python hiroyasu.py export input.Ysf output.csv
```

### Import CSV back to YSF

```bash
python hiroyasu.py import template.Ysf input.csv output.Ysf
```

> **Note:** The template `.Ysf` file is **required**. The tool does **not** rebuild files from scratch.

---

## Editable Fields

### Channel Basics

- `channel_index` → Channel number (1-based)
- `name` → Channel name (~10 chars max)

---

### Frequencies

- `rx_mhz` → Receive frequency (MHz)
- `tx_mhz` → Transmit frequency (MHz)

Use MHz format. Hz fields are internal/debug only.

---

### RF Settings

- `tx_power` → `High` / `Low`
- `bandwidth` → `Wide` / `Narrow`
- `scan` → `ADD` / `DEL`

---

### Signaling / Access Control

- `busy_inhibit` → `OFF` / `DQT` / `CAT`
- `rx_signal_code` → `OFF` / `DTMF` / `FSK` / `FSK DTMF`
- `special_dcs` → `OFF` / `Special DCS 1..4`

---

### Audio / Modulation

- `fm_am` → `FM` / `AM`
- `weather_alert` → `ON` / `OFF`
- `vague_subaudio` → `ON` / `OFF`
- `compander` → `ON` / `OFF`

---

### Scrambler

- `scramble` → `OFF` / `scramble1..scramble8`

---

### PTT Signaling

- `ptt_push_code` → `OFF` / `ID` / `Code form-1..30`
- `ptt_pop_code` → `OFF` / `ID` / `Code form-1..30`

---

### CTCSS / DCS

- `qt_dqt_enc` → TX tone
- `qt_dqt_dec` → RX tone

Formats:

- `CTCSS`: `67.0`, `88.5`, etc.
- `DCS`: `D023N`, `D023I`

---

## Important Behavior

### Partial Updates

Only modified values are written back.

This helps prevent:

- corruption of unused channels
- overwriting unknown data
- CPS compatibility issues

---

### Invalid Values

Invalid values are ignored.

Example:

```
busy_inhibit = ON → ignored
```

---

### Frequency Limits

CPS may reject invalid ranges.  
Memories with invalid frequencies may appear blank.

---

### Template File

The tool patches an existing `.Ysf` file.

Unknown data is preserved.

---

## Debug Mode

```bash
python hiroyasu.py export input.Ysf output.csv --debug
```

Includes:

- raw hex
- internal flags

Not intended for normal editing.

---

## Recommended Workflow

1. Export:

```bash
python hiroyasu.py export radio.Ysf channels.csv
```

2. Edit the CSV file.

3. Import:

```bash
python hiroyasu.py import radio.Ysf channels.csv new.Ysf
```

4. Load `new.Ysf` into CPS.

---

## Author

Antonis Maglaras — ©2026

# Hiroyasu IC-980Pro Max — Specifications & Features

## 🆕 Upgraded Features (IC-980Pro Max)

- FM/AM modulation (AM receive only)
- Electronic relay (silent operation, no clicking in dual watch)
- True dual receive (V/U bands simultaneously)
- Dual band display / watch / receive
- FSK & DTMF signaling support
- FM Radio Resume (FMR)
- Anti-jamming (carrier interference reduction)
- Wireless channel copy (air cloning)
- Wireless clone between same model radios
- Automatic contact (AUC – out-of-range alert)
- Voice menu prompts
- Weather forecast channels (USA/Canada)
- Programmable weather frequencies
- Customizable key combinations (quick menu access)

---

## 🔧 Core Features

- 25W output power
- Compact & lightweight (450g, palm-sized)
- Dual microphone design (main + hand mic)
- Intelligent cooling fan (auto activates on high temperature)
- Compander (compressor/expander - improves long-distance audio clarity)
- 8-level voice scrambler
- VOX (hands-free operation)
- 1750Hz repeater tone
- AI noise reduction (Denoise – background noise suppression)
- Dual band operation (VHF/UHF simultaneous receive)
- Built-in FM broadcast radio reception (76–108 MHz)
- FM Radio Resume (returns after transmission ends)

---

## 📡 Advanced Features

### Wireless Clone / Copy Modes

- Full clone (all data)
- Channel-only clone
- Send / Receive modes between radios
- Works only between identical models

---

### Quick Key Assignment

- User-defined key combinations (FUN + number)
- Allows fast access to menu items (e.g. squelch)

---

### Anti-Jamming

- Reduces interference from strong nearby carriers
- Helps in noisy RF environments

---

### Automatic Contact (AUC)

- Alerts when radios go out of range
- Useful for team coordination

---

## 📊 General Specifications

- Frequency Range (EU): VHF 144–146 MHz, UHF 430–440 MHz  
  (Note: it can be expanded)
- Frequency Range (USA): VHF 144–148 MHz, UHF 420–450 MHz  
  (Note: it can be expanded)
- Channels: 500  
- Channel Spacing: 25 kHz (Wide), 12.5 kHz (Narrow)  
- Step Size: 2.5 / 5 / 6.25 / 10 / 12.5 / 20 / 25 / 30 / 50 kHz  
- Voltage: 13.8V DC ±15%  
- Noise Suppression: Carrier / CTCSS / DCS / Custom  
- Frequency Stability: ±2.5 ppm  
- Operating Temperature: -20°C to +60°C  
- Dimensions: 108 × 40 × 102 mm  
- Weight: 450 g  

---

## 📡 Receiver Specifications

- Sensitivity: ≥0.2 µV (Wide), ≥0.14 µV (Narrow)  
- Adjacent Channel Selectivity: ≥70 dB / ≥60 dB  
- Intermodulation: ≥65 dB / ≥60 dB  
- Spurious Response: ≥70 dB  
- Signal-to-noise ratio: ≥45 dB / ≥40 dB  
- Audio distortion: ≤5%  
- Audio Output: ≥2W ±10%  

---

## 📶 Transmission Specifications

- Output Power: 25W / 20W (VHF/UHF)  
- Modulation: 16KΦF3E (Wide), 11KΦF3E (Narrow)  
- Adjacent Channel Power: ≥70 dB / ≥60 dB  
- Signal-to-noise ratio: ≥40 dB  
- Spurious & Harmonics: ≥60 dB  
- Audio distortion: ≤5%  

---

## ⚠️ Known Limitations

### AM Mode

- AM is receive-only and not a true hardware demodulator  
- Likely implemented via DSP/software processing  
- Audio quality is **very poor**

---

### Dual Watch Issues

- If both A and B receive simultaneously (channel mode):
  - **Audio is completely muted**

- If:
  - A = channel mode  
  - B = VFO mode  

  and both receive:

  - B side **does not show any signal**

---

### Signal Strength Indicator

- Works only as:
  - OFF or FULL
- Does not show real RSSI levels

---

## 🧠 Notes

- AM mode is not suitable for serious use (e.g. airband)
- Weather channels are region-dependent (mainly US/Canada)
- Some features require identical radios (clone/AUC)

---

## Tool for Memory Management

You can use the Python script:  
https://github.com/vegos/Hiroyasu_IC-980Pro_Max/tree/main/Import-Export_Script

- Export to CSV  
- Import channel memories  
- Edit and clone configurations easily  

---

## Adjustment Menu

CPS adjustment menu documentation (translated, explained):  
https://github.com/vegos/Hiroyasu_IC-980Pro_Max/tree/main/CPS_Explained

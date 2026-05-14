# GEE-Downloader

โปรเจกต์สำหรับดาวน์โหลดภาพถ่ายดาวเทียม Sentinel-1 (Multi-Temporal) ผ่าน Google Earth Engine (GEE) แบบอัตโนมัติ และบันทึกลงในเครื่องท้องถิ่นสำหรับการวิเคราะห์ความเปลี่ยนแปลงของพื้นที่ (เช่น ในตัวอย่างคือ จังหวัดระยอง)

## ความต้องการของระบบ (Prerequisites)
- Python 3.9+ (แนะนำ 3.11)
- บัญชี Google Earth Engine (GEE)
- Google Cloud Project ID สำหรับเชื่อมต่อ API (ต้องเปิดใช้งาน Earth Engine API ใน Google Cloud Console)

## การติดตั้ง (Installation)

1. **โคลนโปรเจกต์**
   ```bash
   git clone https://github.com/Knight60/GEE-Downloader.git
   cd GEE-Downloader
   ```

2. **สร้าง Virtual Environment (แนะนำ)**
   ```bash
   python -m venv .venv
   ```
   **วิธีเปิดใช้งาน Virtual Environment:**
   - **Windows (Command Prompt):** `.venv\Scripts\activate`
   - **Windows (PowerShell):** `.\.venv\Scripts\Activate.ps1`
   - **macOS/Linux:** `source .venv/bin/activate`

3. **ติดตั้งแพ็กเกจที่จำเป็น**
   ```bash
   pip install -r requirements.txt
   ```
   *(หมายเหตุ: หากต้องการเปิดไฟล์ `display_s1.ipynb` เพื่อแสดงผลภาพ แนะนำให้ติดตั้ง `rasterio` เพิ่มเติมด้วยคำสั่ง `pip install rasterio`)*

## การตั้งค่า (Configuration)

ก่อนเริ่มต้นใช้งาน คุณจำเป็นต้องกำหนด Project ID ของ Google Cloud ในไฟล์ `config.json` (ตัวสคริปต์จะมองหาโปรเจกต์ ID จากตรงนี้เพื่อเชื่อมต่อ API):
```json
{
    "project_id": "ee-yourprojectid"
}
```
หากไม่ได้กำหนดไว้ใน `config.json` สคริปต์จะถามหา Project ID ของคุณเมื่อเริ่มต้นทำงานครั้งแรก และจะบันทึกเก็บไว้ให้โดยอัตโนมัติ

## การใช้งาน (Usage)

### 1. การดาวน์โหลดภาพดาวเทียม Sentinel-1
รันสคริปต์ `download_s1.py` เพื่อให้ระบบไปดึงข้อมูลจาก GEE และดาวน์โหลดภาพมายังเครื่อง
```bash
python download_s1.py
```
- ระบบจะให้คุณทำการยืนยันตัวตนกับ Google Earth Engine (Authenticate) ผ่านเบราว์เซอร์อัตโนมัติ (หากยังไม่เคยล็อกอิน)
- สคริปต์จะกรองข้อมูลภาพ Sentinel-1 (VV) โดยลดขอบภาพที่ผิดปกติ นำมาหาค่าเฉลี่ยในช่วงเวลา Spring, Late Spring และ Summer
- ไฟล์ภาพผลลัพธ์ (`desc_change.tif` และ `asc_change.tif`) จะถูกบันทึกไว้ในโฟลเดอร์ `download/`

### 2. การแสดงผลและตรวจสอบภาพดาวเทียม
หากต้องการแสดงผลภาพที่ดาวน์โหลดมา ให้ใช้ไฟล์ `display_s1.ipynb`
- เปิดไฟล์ `display_s1.ipynb` ในโปรแกรมที่รองรับ Jupyter (เช่น VSCode)
- เลือก Kernel เป็น Python ใน `.venv`
- รันโค้ดเพื่ออ่านไฟล์ด้วย `rasterio` และแสดงผลภาพเป็นสี (RGB Composite) ผ่าน `matplotlib` ทำให้เห็นความเปลี่ยนแปลงของพื้นที่ได้อย่างชัดเจน

## โครงสร้างโปรเจกต์ (Project Structure)
- `download_s1.py` : สคริปต์หลักสำหรับประมวลผลและดาวน์โหลดภาพจาก Google Earth Engine
- `display_s1.ipynb` : Jupyter Notebook สำหรับพล็อตและแสดงผลภาพผลลัพธ์
- `config.json` : ไฟล์เก็บการตั้งค่า Project ID (สร้างเองหรือให้ระบบสร้างให้)
- `requirements.txt` : รายการ Library หรือ Dependencies ที่โปรเจกต์ต้องการ

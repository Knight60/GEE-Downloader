import os

# แก้ปัญหาข้อขัดแย้งของ PROJ library กับ PostgreSQL/PostGIS ในเครื่อง
if 'PROJ_LIB' in os.environ:
    del os.environ['PROJ_LIB']
if 'PROJ_DATA' in os.environ:
    del os.environ['PROJ_DATA']

import ee
import geemap
import json

config_path = os.path.join(os.path.dirname(__file__), 'config.json')

# โหลด config
if os.path.exists(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
else:
    config = {}

project_id = config.get("project_id", "")

# Initialize Earth Engine
try:
    if project_id:
        ee.Initialize(project=project_id)
    else:
        ee.Initialize()
except Exception as e:
    print("ไม่พบ Project หรือยังไม่ได้ล็อกอิน Earth Engine")
    if not project_id:
        project_id = input("กรุณาใส่ Google Cloud Project ID ของคุณ (เช่น 'ee-yourname'): ")
        config["project_id"] = project_id
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
            print("บันทึก Project ID ลงใน config.json เรียบร้อยแล้ว")
            
    ee.Authenticate(project=project_id)
    ee.Initialize(project=project_id)

# 1. กำหนดพื้นที่สนใจ (ROI) เป็นจังหวัดระยอง ประเทศไทย
roi = ee.FeatureCollection("FAO/GAUL/2015/level1") \
    .filter(ee.Filter.eq('ADM0_NAME', 'Thailand')) \
    .filter(ee.Filter.eq('ADM1_NAME', 'Rayong')) \
    .geometry()

def mask_edge(image):
    edge = image.lt(-30.0)
    masked_image = image.mask().And(edge.Not())
    return image.updateMask(masked_image)

# 2. ดึงข้อมูลภาพ Sentinel-1 และกรองด้วย ROI เพื่อลดปริมาณการประมวลผล
img_vv = (
    ee.ImageCollection('COPERNICUS/S1_GRD')
    .filterBounds(roi)
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
    .filter(ee.Filter.eq('instrumentMode', 'IW'))
    .select('VV')
    .map(mask_edge)
)

desc = img_vv.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
asc = img_vv.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))

# กำหนดช่วงเวลา
spring = ee.Filter.date('2015-03-01', '2015-04-20')
late_spring = ee.Filter.date('2015-04-21', '2015-06-10')
summer = ee.Filter.date('2015-06-11', '2015-08-31')

# 3. สร้างภาพประกอบ (Composite) และตัดภาพตามขอบเขตจังหวัดระยอง (clip)
desc_change = ee.Image.cat(
    desc.filter(spring).mean(),
    desc.filter(late_spring).mean(),
    desc.filter(summer).mean(),
).clip(roi)

asc_change = ee.Image.cat(
    asc.filter(spring).mean(),
    asc.filter(late_spring).mean(),
    asc.filter(summer).mean(),
).clip(roi)

# 4. สร้างโฟลเดอร์สำหรับเก็บภาพ (ถ้ายังไม่มี)
out_dir = os.path.join(os.getcwd(), 'download')
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

print(f"เตรียมดาวน์โหลดภาพไปยังโฟลเดอร์: {out_dir}")

# กำหนดชื่อไฟล์ผลลัพธ์
out_desc = os.path.join(out_dir, 'desc_change.tif')
out_asc = os.path.join(out_dir, 'asc_change.tif')

# 5. สั่งดาวน์โหลดภาพ (ตั้งค่า scale=10 สำหรับ Sentinel-1, แต่อาจปรับเป็น 30 หากไฟล์ใหญ่หรือโหลดช้า)
print("กำลังดาวน์โหลดภาพ DESCENDING (กรุณารอสักครู่ พื้นที่ระดับจังหวัดอาจใช้เวลาสักพัก)...")
geemap.download_ee_image(desc_change, out_desc, region=roi, scale=10, crs='EPSG:4326')

print("กำลังดาวน์โหลดภาพ ASCENDING...")
geemap.download_ee_image(asc_change, out_asc, region=roi, scale=10, crs='EPSG:4326')

print("ดาวน์โหลดเสร็จสมบูรณ์!")

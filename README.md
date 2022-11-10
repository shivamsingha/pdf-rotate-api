# REST API for PDF rotation

Rotate a page of uploaded PDF.

## Install Dependencies

```pip install -r req.txt```

## Usage
```python pdf_rotate_api/app.py```

This starts the Flask HTTP server on port 5000.

## API

### **POST** /
```/```

#### Description
Takes angle_of_rotation, page_number & file as form inputs. Returns JSON with status & download URL.

#### Request Params
Key|Example Value|Description
---|---|---
angle_of_rotation|180|Angle of Rotation (90, 180 or 270)
page_number|7|Number of page to rotate
#### Example
**curl**
```bash
curl -X POST \
  'localhost:5000' \
  --form 'angle_of_rotation="180"' \
  --form 'page_number="7"' \
  --form 'file=@test.pdf'
```
**Result**
```json
{
  "status": "processing",
  "downloadURL": "/output_fbc8baa6e7a1bf0f95c5f7b5783d7ea37d5f09a874c037bdc1373d10c12df29dtest.pdf"
}
``` 

### **GET** /
```/:filename```

#### Description
If process has successfully finished the modified file is returned. If process failed JSON is returned with error. 

#### Example
**curl**
```bash
curl -X GET 'localhost:5000/output_fbc8baa6e7a1bf0f95c5f7b5783d7ea37d5f09a874c037bdc1373d10c12df29dtest.pdf'
```
**Result**
Modified file gets downloaded as attachment. 

## Configs

Change the value of `UPLOAD_FOLDER` in `constants.py` to where you want your uploaded files to be saved.
from datetime import date, datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from db import get_connection, init_tables, next_id

app = FastAPI(title="COVID Vaccination API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_tables()


def serialize_value(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


def rows_to_dicts(cursor, rows):
    columns = [col[0] for col in cursor.description]
    result = []
    for row in rows:
        result.append({col: serialize_value(val) for col, val in zip(columns, row)})
    return result


def row_to_dict(cursor, row):
    if row is None:
        return None
    return rows_to_dicts(cursor, [row])[0]


class UserCreate(BaseModel):
    adharno: int
    name: str
    age: int
    phone: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None


class HospitalCreate(BaseModel):
    hospital_name: str
    address: str
    pincode: int
    phone: int
    dr_name: str


class HospitalUpdate(BaseModel):
    phone: Optional[int] = None
    dr_name: Optional[str] = None


class DoseCreate(BaseModel):
    hid: Optional[int] = None
    dose_name: str
    price: int
    dose_date: str = Field(description="YYYY-MM-DD")
    slot1: int
    slot2: int
    slot3: int
    slot4: int


class BookVaccine(BaseModel):
    adharno: int
    hid: int
    slot: int = Field(ge=1, le=4)
    dose_date: str = Field(description="YYYY-MM-DD")
    amt2: Optional[int] = None


@app.get("/")
def home():
    return {
        "message": "COVID Vaccination API is running",
        "docs": "/docs",
    }


@app.get("/hospitals")
def list_hospitals():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hospital")
    data = rows_to_dicts(cursor, cursor.fetchall())
    cursor.close()
    conn.close()
    return data


@app.post("/hospitals")
def add_hospital(body: HospitalCreate):
    conn = get_connection()
    cursor = conn.cursor()
    h_id = next_id(cursor, "hospital", "h_id")
    cursor.execute(
        "INSERT INTO hospital VALUES (%s, %s, %s, %s, %s, %s)",
        (h_id, body.hospital_name, body.address, body.pincode, body.phone, body.dr_name),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Hospital added", "h_id": h_id}


@app.put("/hospitals/{h_id}")
def update_hospital(h_id: int, body: HospitalUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hospital WHERE h_id=%s", (h_id,))
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Hospital not found")

    if body.phone is not None and body.dr_name is not None:
        cursor.execute(
            "UPDATE hospital SET phone=%s, dr_name=%s WHERE h_id=%s",
            (body.phone, body.dr_name, h_id),
        )
    elif body.phone is not None:
        cursor.execute("UPDATE hospital SET phone=%s WHERE h_id=%s", (body.phone, h_id))
    elif body.dr_name is not None:
        cursor.execute("UPDATE hospital SET dr_name=%s WHERE h_id=%s", (body.dr_name, h_id))
    else:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Provide phone and/or dr_name")

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Hospital updated"}


@app.post("/hospitals/dummy")
def insert_dummy_hospitals():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM hospital")
    count = cursor.fetchone()[0]
    if count:
        cursor.close()
        conn.close()
        return {"message": "Hospitals already exist; dummy records not inserted"}

    rows = [
        (1, "aiims", "basni industrial area", 342005, 29156894, "Dr. Abz"),
        (2, "MdM", "sector-H Shastri nagar,jodhpur", 342003, 29195618, "Dr. mvn"),
        (3, "MGM", "jalori gate,jodhpur", 342001, 29156481, "Dr. ytu"),
        (4, "choupasni satt", "choupasni jodhpur", 342003, 29189451, "Dr. erp"),
        (5, "pratap nagar SH-2", "pratap nagar jodhpur", 342003, 29189417, "Dr. opt"),
    ]
    cursor.executemany("INSERT INTO hospital VALUES (%s, %s, %s, %s, %s, %s)", rows)
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Dummy hospital records inserted", "count": len(rows)}


@app.get("/doses")
def list_doses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dose_details")
    data = rows_to_dicts(cursor, cursor.fetchall())
    cursor.close()
    conn.close()
    return data


@app.get("/doses/slots")
def available_slots():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT hid, dose_name, dose_date,
               slot1 - slot1_used AS slot1_left,
               slot2 - slot2_used AS slot2_left,
               slot3 - slot3_used AS slot3_left,
               slot4 - slot4_used AS slot4_left
        FROM dose_details
        """
    )
    data = rows_to_dicts(cursor, cursor.fetchall())
    cursor.close()
    conn.close()
    return data


@app.post("/doses")
def add_dose(body: DoseCreate):
    conn = get_connection()
    cursor = conn.cursor()
    did = next_id(cursor, "dose_details", "did")
    hid = body.hid if body.hid is not None else next_id(cursor, "dose_details", "hid")
    cursor.execute(
        """
        INSERT INTO dose_details
            (did, hid, dose_name, price, dose_date, slot1, slot2, slot3, slot4)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            did,
            hid,
            body.dose_name,
            body.price,
            body.dose_date,
            body.slot1,
            body.slot2,
            body.slot3,
            body.slot4,
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Dose added", "did": did, "hid": hid}


@app.get("/users")
def list_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_register")
    data = rows_to_dicts(cursor, cursor.fetchall())
    cursor.close()
    conn.close()
    return data


@app.get("/users/phone/{phone}")
def get_user_by_phone(phone: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_register WHERE phone=%s", (phone,))
    row = cursor.fetchone()
    data = row_to_dict(cursor, row)
    cursor.close()
    conn.close()
    if data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return data


@app.post("/users")
def register_user(body: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT adharno FROM user_register WHERE adharno=%s", (body.adharno,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(status_code=409, detail="User already registered")

    cursor.execute(
        "INSERT INTO user_register VALUES (%s, %s, %s, %s)",
        (body.adharno, body.name, body.age, body.phone),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User registered"}


@app.put("/users/{adharno}")
def update_user(adharno: int, body: UserUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_register WHERE adharno=%s", (adharno,))
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    name = body.name if body.name is not None else row[1]
    age = body.age if body.age is not None else row[2]
    phone = body.phone if body.phone is not None else row[3]
    cursor.execute(
        "UPDATE user_register SET name=%s, age=%s, phone=%s WHERE adharno=%s",
        (name, age, phone, adharno),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User updated"}


@app.delete("/users/{adharno}")
def delete_user(adharno: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_register WHERE adharno=%s", (adharno,))
    conn.commit()
    deleted = cursor.rowcount
    cursor.close()
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}


@app.post("/vaccines/book")
def book_vaccine(body: BookVaccine):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT adharno FROM user_register WHERE adharno=%s", (body.adharno,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="New users must register first")

    slot_col = f"slot{body.slot}"
    used_col = f"slot{body.slot}_used"
    cursor.execute(
        f"SELECT {slot_col}, {used_col} FROM dose_details WHERE hid=%s",
        (body.hid,),
    )
    slot_row = cursor.fetchone()
    if slot_row is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="No dose slot found for this hospital")

    capacity, used = int(slot_row[0]), int(slot_row[1])
    if used >= capacity:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=409, detail="Selected slot is full")

    cursor.execute(
        f"UPDATE dose_details SET {used_col}=%s WHERE hid=%s",
        (used + 1, body.hid),
    )

    cursor.execute(
        "SELECT adharno FROM register_vaccine WHERE adharno=%s",
        (body.adharno,),
    )
    existing = cursor.fetchone()

    if existing is None:
        cursor.execute(
            "SELECT price FROM dose_details WHERE hid=%s AND dose_date=%s",
            (body.hid, body.dose_date),
        )
        price_row = cursor.fetchone()
        if price_row is None:
            conn.rollback()
            cursor.close()
            conn.close()
            raise HTTPException(
                status_code=404,
                detail="No dose found for this hospital ID and date",
            )
        amt = price_row[0]
        regid = next_id(cursor, "register_vaccine", "regid")
        cursor.execute(
            """
            INSERT INTO register_vaccine (regid, adharno, DOA1, ndose, h_id1, amt1)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (regid, body.adharno, body.dose_date, 1, body.hid, amt),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Dose 1 booked successfully", "regid": regid, "amount": amt}

    if body.amt2 is None:
        conn.rollback()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="amt2 is required for dose 2")

    cursor.execute(
        """
        UPDATE register_vaccine
        SET DOA2=%s, ndose=%s, h_id2=%s, amt2=%s
        WHERE adharno=%s
        """,
        (body.dose_date, 2, body.hid, body.amt2, body.adharno),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Dose 2 booked successfully"}


@app.put("/certificates/{adharno}")
def mark_vaccinated(adharno: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT marker1, marker2 FROM register_vaccine WHERE adharno=%s",
        (adharno,),
    )
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="No vaccine booking found")

    if row[0] == "n":
        cursor.execute(
            "UPDATE register_vaccine SET marker1=%s WHERE adharno=%s",
            ("y", adharno),
        )
        dose = 1
    else:
        cursor.execute(
            "UPDATE register_vaccine SET marker2=%s WHERE adharno=%s",
            ("y", adharno),
        )
        dose = 2
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"Vaccinated successfully with dose {dose}"}


@app.get("/certificates/{adharno}")
def get_certificate(adharno: int, dose: int = 1):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT marker1, marker2 FROM register_vaccine WHERE adharno=%s',
        (adharno,),
    )
    markers = cursor.fetchone()
    if markers is None or markers[0] != "y":
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="You are not vaccinated")

    if dose == 1:
        cursor.execute(
            """
            SELECT rv.regid, rv.DOA1, rv.ndose, rv.h_id1, rv.amt1,
                   ur.adharno, ur.name, ur.age, ur.phone
            FROM user_register ur
            JOIN register_vaccine rv ON ur.adharno = rv.adharno
            WHERE ur.adharno=%s AND rv.marker1='y'
            """,
            (adharno,),
        )
        row = cursor.fetchone()
        data = row_to_dict(cursor, row)
        cursor.close()
        conn.close()
        if data is None:
            raise HTTPException(status_code=404, detail="Dose 1 certificate not found")
        return data

    if markers[1] != "y":
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Dose 2 has not been marked as given")

    cursor.execute(
        """
        SELECT ur.adharno, ur.name, ur.age, ur.phone,
               rv.regid, rv.DOA1, rv.DOA2, rv.ndose,
               rv.h_id1, rv.amt1, rv.h_id2, rv.amt2
        FROM user_register ur
        JOIN register_vaccine rv ON ur.adharno = rv.adharno
        WHERE ur.adharno=%s
        """,
        (adharno,),
    )
    row = cursor.fetchone()
    data = row_to_dict(cursor, row)
    cursor.close()
    conn.close()
    if data is None:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return data

// Shapes returned by / sent to the FastAPI backend (../backend/app.py)

export interface User {
  adharno: number;
  name: string;
  age: number;
  phone: string;
}
export type UserCreate = User;
export type UserUpdate = Partial<Omit<User, "adharno">>;

export interface Hospital {
  h_id: number;
  hospital_name: string;
  address: string;
  pincode: number;
  phone: number;
  dr_name: string;
}
export type HospitalCreate = Omit<Hospital, "h_id">;
export type HospitalUpdate = Partial<Pick<Hospital, "phone" | "dr_name">>;

export interface Dose {
  did: number;
  hid: number;
  dose_name: string;
  price: number;
  dose_date: string;
  slot1: number;
  slot2: number;
  slot3: number;
  slot4: number;
  slot1_used: number;
  slot2_used: number;
  slot3_used: number;
  slot4_used: number;
}
export type DoseCreate = Omit<Dose, "did" | "hid" | `slot${1 | 2 | 3 | 4}_used`> & { hid?: number };

export interface SlotAvailability {
  hid: number;
  dose_name: string;
  dose_date: string;
  slot1_left: number;
  slot2_left: number;
  slot3_left: number;
  slot4_left: number;
}

export type SlotNumber = 1 | 2 | 3 | 4;

export interface BookVaccine {
  adharno: number;
  hid: number;
  slot: SlotNumber;
  dose_date: string;
  amt2?: number;
}

export interface Certificate {
  adharno: number;
  name: string;
  age: number;
  phone: string;
  regid: number;
  ndose: number;
  DOA1: string;
  h_id1: number;
  amt1: number;
  DOA2?: string | null;
  h_id2?: number | null;
  amt2?: number | null;
}

export interface Message {
  message: string;
}

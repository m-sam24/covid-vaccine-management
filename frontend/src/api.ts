import type {
  BookVaccine, Certificate, Dose, DoseCreate, Hospital, HospitalCreate, HospitalUpdate,
  Message, SlotAvailability, User, UserCreate, UserUpdate,
} from "./types";

const BASE = (import.meta.env.VITE_API_URL as string | undefined)?.replace(/\/+$/, "") ?? "/api";

export class ApiError extends Error {}

async function request<T>(path: string, method = "GET", body?: unknown): Promise<T> {
  let res: Response;
  try {
    res = await fetch(BASE + path, {
      method,
      headers: body !== undefined ? { "Content-Type": "application/json" } : undefined,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new ApiError("Cannot reach the API. Is the backend running?");
  }
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    let detail = data?.detail ?? `Request failed (${res.status})`;
    // FastAPI validation errors come back as a list
    if (Array.isArray(detail)) {
      detail = detail.map((e: { loc: string[]; msg: string }) => `${e.loc.at(-1)}: ${e.msg}`).join("; ");
    }
    throw new ApiError(detail);
  }
  return data as T;
}

export const api = {
  health: () => request<Message>("/"),

  listUsers: () => request<User[]>("/users"),
  getUserByPhone: (phone: string) => request<User>(`/users/phone/${encodeURIComponent(phone)}`),
  registerUser: (body: UserCreate) => request<Message>("/users", "POST", body),
  updateUser: (adharno: number, body: UserUpdate) => request<Message>(`/users/${adharno}`, "PUT", body),
  deleteUser: (adharno: number) => request<Message>(`/users/${adharno}`, "DELETE"),

  listHospitals: () => request<Hospital[]>("/hospitals"),
  addHospital: (body: HospitalCreate) => request<Message & { h_id: number }>("/hospitals", "POST", body),
  updateHospital: (h_id: number, body: HospitalUpdate) => request<Message>(`/hospitals/${h_id}`, "PUT", body),
  insertDummyHospitals: () => request<Message>("/hospitals/dummy", "POST"),

  listDoses: () => request<Dose[]>("/doses"),
  availableSlots: () => request<SlotAvailability[]>("/doses/slots"),
  addDose: (body: DoseCreate) => request<Message & { did: number; hid: number }>("/doses", "POST", body),

  bookVaccine: (body: BookVaccine) =>
    request<Message & { regid?: number; amount?: number }>("/vaccines/book", "POST", body),

  markVaccinated: (adharno: number) => request<Message>(`/certificates/${adharno}`, "PUT"),
  getCertificate: (adharno: number, dose: 1 | 2) => request<Certificate>(`/certificates/${adharno}?dose=${dose}`),
};

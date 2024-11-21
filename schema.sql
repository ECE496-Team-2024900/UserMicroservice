CREATE TABLE "clinicians" (
  "medical_ref_number" integer PRIMARY KEY,
  "first_name" varchar NOT NULL,
  "last_name" varchar NOT NULL,
  "email" varchar NOT NULL
);

CREATE TABLE "patients" (
  "medical_ref_number" integer PRIMARY KEY,
  "first_name" varchar NOT NULL,
  "last_name" varchar NOT NULL,
  "phone_num" integer NOT NULL,
  "medical_device_id" varchar NOT NULL,
  "email" varchar NOT NULL,
  "date_of_birth" date NOT NULL
);

CREATE TABLE "available_slots" (
  "id" SERIAL PRIMARY KEY,
  "clinician_id" integer NOT NULL,
  "start_time_of_availability" varchar NOT NULL,
  "end_time_of_availability" varchar NOT NULL,
  "date" date NOT NULL
);

ALTER TABLE "available_slots" ADD FOREIGN KEY ("clinician_id") REFERENCES "clinicians" ("medical_ref_number");

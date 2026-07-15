import { sql } from "drizzle-orm";
import { integer, sqliteTable, text } from "drizzle-orm/sqlite-core";

export const bookings = sqliteTable("bookings", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  reference: text("reference").notNull().unique(),
  course: text("course").notNull(),
  name: text("name").notNull(),
  organization: text("organization").notNull().default(""),
  email: text("email").notNull(),
  phone: text("phone").notNull().default(""),
  preferredDate: text("preferred_date").notNull().default(""),
  participants: integer("participants").notNull().default(1),
  location: text("location").notNull().default(""),
  message: text("message").notNull().default(""),
  integrationStatus: text("integration_status").notNull().default("pending"),
  createdAt: text("created_at").notNull().default(sql`CURRENT_TIMESTAMP`),
});

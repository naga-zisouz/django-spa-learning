import type { CreateTaskPayload, Task, TaskStatusFilter } from "../types/task";
import { apiFetch } from "./client";

export function fetchTasks(status: TaskStatusFilter): Promise<Task[]> {
  const query = new URLSearchParams({ status });
  return apiFetch<Task[]>(`/api/tasks/?${query.toString()}`);
}

export function createTask(payload: CreateTaskPayload): Promise<Task> {
  return apiFetch<Task>("/api/tasks/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function toggleTask(id: number): Promise<Task> {
  return apiFetch<Task>(`/api/tasks/${id}/toggle/`, { method: "POST" });
}

export function deleteTask(id: number): Promise<void> {
  return apiFetch<void>(`/api/tasks/${id}/`, { method: "DELETE" });
}

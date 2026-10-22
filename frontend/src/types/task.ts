export type TaskStatusFilter = "all" | "open" | "done";

export interface Task {
  id: number;
  title: string;
  description: string;
  is_done: boolean;
  created_at: string;
}

export interface CreateTaskPayload {
  title: string;
  description?: string;
}

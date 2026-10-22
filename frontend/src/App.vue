<script setup lang="ts">
import { onMounted, ref } from "vue";
import {
  createTask,
  deleteTask,
  fetchTasks,
  toggleTask,
} from "./api/tasks";
import type { Task, TaskStatusFilter } from "./types/task";
import { ApiError } from "./api/client";

const tasks = ref<Task[]>([]);
const statusFilter = ref<TaskStatusFilter>("open");
const title = ref("");
const description = ref("");
const loading = ref(false);
const errorMessage = ref<string | null>(null);

const filters: { value: TaskStatusFilter; label: string }[] = [
  { value: "open", label: "未完了" },
  { value: "done", label: "完了" },
  { value: "all", label: "すべて" },
];

async function loadTasks() {
  loading.value = true;
  errorMessage.value = null;
  try {
    tasks.value = await fetchTasks(statusFilter.value);
  } catch (err) {
    errorMessage.value =
      err instanceof ApiError ? err.message : "一覧の取得に失敗しました。";
  } finally {
    loading.value = false;
  }
}

async function onSubmit() {
  const trimmed = title.value.trim();
  if (!trimmed) return;

  errorMessage.value = null;
  try {
    await createTask({ title: trimmed, description: description.value });
    title.value = "";
    description.value = "";
    await loadTasks();
  } catch (err) {
    errorMessage.value =
      err instanceof ApiError ? err.message : "登録に失敗しました。";
  }
}

async function onToggle(task: Task) {
  errorMessage.value = null;
  try {
    await toggleTask(task.id);
    await loadTasks();
  } catch {
    errorMessage.value = "完了状態の更新に失敗しました。";
  }
}

async function onDelete(task: Task) {
  errorMessage.value = null;
  try {
    await deleteTask(task.id);
    await loadTasks();
  } catch {
    errorMessage.value = "削除に失敗しました。";
  }
}

function setFilter(value: TaskStatusFilter) {
  statusFilter.value = value;
  loadTasks();
}

onMounted(() => {
  loadTasks();
});
</script>

<template>
  <h1>ToDo（SPA 学習）</h1>
  <p class="muted">
    バックエンドは Django API、画面は Vue が描画します。教材はリポジトリの
    TEXTBOOK.md を参照してください。
  </p>

  <div class="card">
    <form class="task-form" @submit.prevent="onSubmit">
      <label>
        タイトル
        <input v-model="title" type="text" maxlength="100" required />
      </label>
      <label>
        メモ（任意）
        <textarea v-model="description" rows="2" />
      </label>
      <button type="submit">追加</button>
    </form>
  </div>

  <div class="filters">
    <button
      v-for="f in filters"
      :key="f.value"
      type="button"
      :class="{ active: statusFilter === f.value }"
      @click="setFilter(f.value)"
    >
      {{ f.label }}
    </button>
  </div>

  <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  <p v-if="loading" class="muted">読み込み中…</p>

  <div v-else class="card">
    <ul v-if="tasks.length" class="tasks">
      <li v-for="task in tasks" :key="task.id" :class="{ done: task.is_done }">
        <div>
          <div class="title">{{ task.title }}</div>
          <div v-if="task.description" class="description">
            {{ task.description }}
          </div>
        </div>
        <div class="actions">
          <button type="button" @click="onToggle(task)">
            {{ task.is_done ? "未完了に戻す" : "完了" }}
          </button>
          <button type="button" class="delete" @click="onDelete(task)">
            削除
          </button>
        </div>
      </li>
    </ul>
    <p v-else class="muted">タスクがありません。</p>
  </div>
</template>

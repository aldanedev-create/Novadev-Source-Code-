<script setup>
import { reactive, watchEffect } from 'vue'

const props = defineProps({
  title: { type: String, default: 'Form' },
  fields: { type: Array, default: () => [] },
  submitLabel: { type: String, default: 'Save' }
})
const emit = defineEmits(['submit'])
const form = reactive({})

watchEffect(() => {
  props.fields.forEach((field) => {
    if (!(field in form)) form[field] = ''
  })
})

function submit() {
  emit('submit', { ...form })
  Object.keys(form).forEach((key) => {
    form[key] = ''
  })
}
</script>

<template>
  <form class="panel form-grid" @submit.prevent="submit">
    <div class="panel-heading">
      <h2>{{ title }}</h2>
      <span>{{ fields.length }} fields</span>
    </div>
    <label v-for="field in fields" :key="field">
      <span>{{ field }}</span>
      <input v-model="form[field]" :name="field" />
    </label>
    <button class="primary-button" type="submit">{{ submitLabel }}</button>
  </form>
</template>

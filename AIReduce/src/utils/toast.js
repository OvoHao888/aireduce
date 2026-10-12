import { ref } from 'vue'

const toasts = ref([])
let toastId = 0
let timeouts = {}

const show = (message, type = 'info', duration = 3000) => {
  const id = ++toastId
  const toast = { id, message, type, enter: true, leave: false }
  toasts.value.push(toast)

  timeouts[id] = setTimeout(() => {
    removeToast(id)
  }, duration)

  return id
}

const success = (message, duration = 3000) => show(message, 'success', duration)
const error = (message, duration = 4000) => show(message, 'error', duration)
const warning = (message, duration = 3500) => show(message, 'warning', duration)
const info = (message, duration = 3000) => show(message, 'info', duration)

const removeToast = (id) => {
  if (timeouts[id]) {
    clearTimeout(timeouts[id])
    delete timeouts[id]
  }

  const index = toasts.value.findIndex(t => t.id === id)
  if (index > -1) {
    toasts.value[index].leave = true
    toasts.value[index].enter = false
    setTimeout(() => {
      const idx = toasts.value.findIndex(t => t.id === id)
      if (idx > -1) {
        toasts.value.splice(idx, 1)
      }
    }, 300)
  }
}

const getIcon = (type) => {
  const icons = {
    success: '✅',
    error: '❌',
    warning: '⚠️',
    info: 'ℹ️'
  }
  return icons[type] || icons.info
}

const cleanup = () => {
  Object.keys(timeouts).forEach(id => {
    clearTimeout(timeouts[id])
  })
}

export { toasts, show as showToast, show, success, error, warning, info, removeToast, getIcon, cleanup }

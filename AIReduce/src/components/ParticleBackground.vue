<template>
  <canvas ref="canvas" class="particle-background"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
let ctx = null
let particles = []
let animationId = null

class Particle {
  constructor(canvas) {
    this.x = Math.random() * canvas.width
    this.y = Math.random() * canvas.height
    this.size = Math.random() * 3 + 1
    this.speedX = Math.random() * 0.5 - 0.25
    this.speedY = Math.random() * 0.5 - 0.25
    this.opacity = Math.random() * 0.5 + 0.2

    // 暖色调颜色：橙色、珊瑚色、金色
    const colors = [
      'rgba(230, 126, 34, ',   // 橙色
      'rgba(243, 156, 18, ',   // 金色
      'rgba(231, 76, 60, ',    // 珊瑚红
      'rgba(253, 121, 168, ',  // 粉色
      'rgba(255, 183, 77, '    // 浅橙色
    ]
    this.color = colors[Math.floor(Math.random() * colors.length)]
  }

  update() {
    this.x += this.speedX
    this.y += this.speedY

    // 边界处理
    if (this.x > canvas.value.width) this.x = 0
    if (this.x < 0) this.x = canvas.value.width
    if (this.y > canvas.value.height) this.y = 0
    if (this.y < 0) this.y = canvas.value.height
  }

  draw() {
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
    ctx.fillStyle = this.color + this.opacity + ')'
    ctx.fill()

    // 绘制光晕效果
    ctx.shadowBlur = 15
    ctx.shadowColor = this.color + '0.5)'
  }
}

const initParticles = () => {
  const canvasEl = canvas.value
  canvasEl.width = window.innerWidth
  canvasEl.height = window.innerHeight

  particles = []
  const particleCount = Math.min(100, Math.floor((canvasEl.width * canvasEl.height) / 15000))

  for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle(canvasEl))
  }
}

const animate = () => {
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)

  particles.forEach(particle => {
    particle.update()
    particle.draw()
  })

  // 绘制粒子连线
  drawConnections()

  animationId = requestAnimationFrame(animate)
}

const drawConnections = () => {
  const maxDistance = 150

  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x
      const dy = particles[i].y - particles[j].y
      const distance = Math.sqrt(dx * dx + dy * dy)

      if (distance < maxDistance) {
        const opacity = (1 - distance / maxDistance) * 0.3
        ctx.beginPath()
        ctx.moveTo(particles[i].x, particles[i].y)
        ctx.lineTo(particles[j].x, particles[j].y)
        ctx.strokeStyle = `rgba(230, 126, 34, ${opacity})`
        ctx.lineWidth = 0.5
        ctx.stroke()
      }
    }
  }
}

const handleResize = () => {
  initParticles()
}

onMounted(() => {
  ctx = canvas.value.getContext('2d')
  initParticles()
  animate()

  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.particle-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}
</style>

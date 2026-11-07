import { useEffect, useRef } from 'react'

/**
 * A slow, quiet animation behind the sign-in card: points drifting across the page and
 * joining into edges when they come close — the knowledge-graph idea behind the retrieval.
 * Pure canvas, no library; a static frame when the user asks for reduced motion, and
 * nothing at all under jsdom (tests).
 */
export function GraphBackdrop() {
  const ref = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = ref.current
    if (!canvas || /jsdom/i.test(navigator.userAgent)) return
    const context = canvas.getContext('2d')
    if (!context) return
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const accent = getComputedStyle(document.documentElement).getPropertyValue('--color-accent').trim() || '#1a5fd6'
    const nodes = Array.from({ length: 70 }, () => ({
      x: Math.random(),
      y: Math.random(),
      dx: (Math.random() - 0.5) * 0.00035,
      dy: (Math.random() - 0.5) * 0.00035,
      r: 1.5 + Math.random() * 2,
    }))
    let frame = 0
    let width = 0
    let height = 0

    function resize() {
      if (!canvas) return
      const scale = window.devicePixelRatio || 1
      width = canvas.clientWidth
      height = canvas.clientHeight
      canvas.width = width * scale
      canvas.height = height * scale
      context?.setTransform(scale, 0, 0, scale, 0, 0)
    }

    function draw() {
      if (!context) return
      context.clearRect(0, 0, width, height)
      const reach = Math.min(width, height) * 0.16
      for (const node of nodes) {
        if (!reduced) {
          node.x += node.dx
          node.y += node.dy
          if (node.x < 0 || node.x > 1) node.dx *= -1
          if (node.y < 0 || node.y > 1) node.dy *= -1
        }
      }
      context.lineWidth = 1
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const ax = nodes[i].x * width
          const ay = nodes[i].y * height
          const bx = nodes[j].x * width
          const by = nodes[j].y * height
          const distance = Math.hypot(ax - bx, ay - by)
          if (distance < reach) {
            context.strokeStyle = accent
            context.globalAlpha = 0.18 * (1 - distance / reach)
            context.beginPath()
            context.moveTo(ax, ay)
            context.lineTo(bx, by)
            context.stroke()
          }
        }
      }
      context.globalAlpha = 0.55
      context.fillStyle = accent
      for (const node of nodes) {
        context.beginPath()
        context.arc(node.x * width, node.y * height, node.r, 0, Math.PI * 2)
        context.fill()
      }
      context.globalAlpha = 1
      if (!reduced) frame = window.requestAnimationFrame(draw)
    }

    resize()
    draw()
    window.addEventListener('resize', resize)
    return () => {
      window.removeEventListener('resize', resize)
      window.cancelAnimationFrame(frame)
    }
  }, [])

  return (
    <canvas
      ref={ref}
      aria-hidden="true"
      className="pointer-events-none absolute inset-0 h-full w-full"
    />
  )
}

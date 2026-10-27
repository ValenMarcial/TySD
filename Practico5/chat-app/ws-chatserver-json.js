const express = require('express')
const webserver = express()
  .use((req, res) =>
    res.sendFile('/wsclient-json.html', { root: __dirname })
  )
  .listen(8080, () => console.log(`Listening on ${8080}`))

const { WebSocketServer } = require('ws')
const sockserver = new WebSocketServer({ port: 8000 })

const clients = new Map()

function send(ws, data) {
  ws.send(JSON.stringify(data))
}

sockserver.on('connection', ws => {
  console.log('New client connected!')

  ws.on('message', raw => {
    let data
    try {
      data = JSON.parse(raw)
    } catch {
      return send(ws, { error: 'JSON inválido' })
    }

    if (data.join !== undefined) {
      const userId = String(data.join).trim()
      if (!userId) {
        return send(ws, { error: 'join inválido' })
      }

      if (ws.userId && clients.get(ws.userId) === ws) {
        clients.delete(ws.userId)
      }

      const previous = clients.get(userId)
      ws.userId = userId
      clients.set(userId, ws)

      if (previous && previous !== ws) {
        previous.close()
      }

      return send(ws, { joined: userId })
    }

    if (
      data.from !== undefined &&
      data.to !== undefined &&
      data.msg !== undefined
    ) {
      if (!ws.userId || String(data.from) !== ws.userId) {
        return send(ws, { error: 'usuario no registrado' })
      }

      const message = {
        from: ws.userId,
        to: String(data.to),
        msg: String(data.msg)
      }

      if (message.to === 'all') {
        clients.forEach(client => send(client, message))
      } else {
        const target = clients.get(message.to)
        if (!target) {
          return send(ws, { error: 'usuario no encontrado' })
        }

        send(target, message)
        if (target !== ws) {
          send(ws, message)
        }
      }
      return
    }

    send(ws, { error: 'comando desconocido' })
  })

  ws.on('close', () => {
    if (ws.userId && clients.get(ws.userId) === ws) {
      clients.delete(ws.userId)
    }
    console.log('Client has disconnected!')
  })

  ws.on('error', () => {
    console.log('websocket error')
  })
})
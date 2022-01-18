export default async function handler(req, res) {
  const delay = req.query.delay || 5
  await sleep(delay * 1000)
  res.json({ foo: 'bar' })
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

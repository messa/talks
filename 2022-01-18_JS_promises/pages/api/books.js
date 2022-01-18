const items = [
  {title: 'Malibu Rising', author: 'Taylor Jenkins Reid'},
  {title: 'A Court of Silver Flames', author: 'Sarah J. Maas'},
  {title: 'People We Meet on Vacation', author: 'Emily Henry'},
  {title: 'Project Hail Mary', author: 'Andy Weir'},
  {title: 'The Final Girl Support Group', author: 'Grady Hendrix'},
  {title: 'Broken (in the best possible way)', author: 'Jenny Lawson'},
  {title: 'The Anthropocene Reviewed', author: 'John Green'},
  {title: 'Crying in H Mart', author: 'Michelle Zauner'},
  {title: 'Empire of Pain: The Secret History of the Sackler Dynasty', author: 'Patrick Radden Keefe'},
  {title: 'Lore Olympus: Volume One', author: 'Rachel Smythe'},
  {title: 'The Hill We Climb: An Inaugural Poem for the Country', author: 'Amanda Gorman'},
  {title: 'The Spanish Love Deception', author: 'Elena Armas'},
  {title: 'Firekeeper\’s Daughter', author: 'Angeline Boulley'},
  {title: 'Rule of Wolves', author: 'Leigh Bardugo'},
  {title: 'Daughter of the Deep', author: 'Rick Riordan'},
]

export default async function handler(req, res) {
  const cursor = req.query.cursor
  const offset = cursor ? parseInt(fromBase64(fromBase64(cursor)), 10) : 0
  await sleep(2 * 1000)
  return res.json({
    items: items.slice(offset, offset + 3),
    nextCursor: toBase64(toBase64((offset + 3).toString().padStart(9, '0'))),
  })
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

function toBase64(s) {
  return Buffer.from(s).toString('base64')
}

function fromBase64(s) {
  return Buffer.from(s, 'base64').toString('ascii')
}
